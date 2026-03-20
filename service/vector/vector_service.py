import logging
from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np

import error
import util
from model import ETLParams, Reddit, Comment, Vector
from provider import IDbRedditProvider, IDbCommentProvider, IDbVectorProvider, \
    SupabasePostgresProvider, SupabasePostgresDbRedditProvider, \
    SupabasePostgresDbCommentProvider, SupabasePostgresDbVectorProvider
from service import IVectorService


class VectorService(IVectorService):
    """ Vector service class """

    logger: logging.Logger
    reddit_provider: IDbRedditProvider
    comment_provider: IDbCommentProvider
    vector_provider: IDbVectorProvider

    sentence_transformer: SentenceTransformer

    def __init__(self, logger: logging.Logger | None = None,
                 reddit_provider: IDbRedditProvider | None = None,
                 comment_provider: IDbCommentProvider | None = None,
                 vector_provider: IDbVectorProvider | None = None) -> None:
        self.logger = logger or util.setup_logger(name="vector_service",
                                                  log_file=f"logs/other/vector_service.log")

        supabase_postgres_provider = SupabasePostgresProvider(logger=self.logger)
        self.reddit_provider = reddit_provider or SupabasePostgresDbRedditProvider(supabase_postgres_provider)
        self.comment_provider = comment_provider or SupabasePostgresDbCommentProvider(supabase_postgres_provider)
        self.vector_provider = vector_provider or SupabasePostgresDbVectorProvider(supabase_postgres_provider)

        self.sentence_transformer = SentenceTransformer("all-MiniLM-L6-v2")

    def get_vectors(self, entries: List[Reddit | Comment], params: ETLParams) -> List[Vector]:
        """ Returns the processed vectors from given entries """
        results = list([])
        entry_texts = Vector.get_entry_texts(entries)
        embeddings_list = self._multiprocess_texts(entry_texts, params) if params.is_multiprocessing_used \
            else self._process_texts(entry_texts)

        for entry, embeddings in zip(entries, embeddings_list):
            if isinstance(entry, Reddit):
                results.append(Vector.from_reddit(entry, embeddings))
            elif isinstance(entry, Comment):
                results.append(Vector.from_comment(entry, embeddings))
            else:
                raise error.WrongEntityError(f"Wrong entity type: {type(entry)}. Should be Reddit or Comment.")
        return results

    def _process_texts(self, texts: List[str]) -> List[List[float]]:
        """ Processes texts and returns its vector embeddings """
        return self.sentence_transformer.encode(texts).tolist()

    def _multiprocess_texts(self, texts: List[str], params: ETLParams) -> List[List[float]]:
        """ Processes texts and returns its vector embeddings using multiprocess approach"""
        pool = self.sentence_transformer.start_multi_process_pool(["cpu"]*params.num_processes)
        embeddings = self.sentence_transformer.encode(texts, pool=pool,
                                                      chunk_size=int(np.ceil(len(texts) / params.num_processes)))
        self.sentence_transformer.stop_multi_process_pool(pool)
        return embeddings.tolist()

    def run_etl(self, **etl_params_dict) -> None:
        """ Runs ETL process loading expected reddits and comments, processing and persisting expected vectors """
        etl_params = ETLParams(**etl_params_dict)

        print("Starting vectorization ETL process.")
        self.logger.info("Starting vectorization ETL process.")

        # load source file dates
        source_file_dates = sorted(self.reddit_provider.get_file_dates(phrase=etl_params.phrase))
        print("Source file dates:\n", source_file_dates)
        self.logger.info(f"Source file dates: {source_file_dates}")

        # load target files dates
        target_file_dates = sorted(self.vector_provider.get_file_dates(phrase=etl_params.phrase))
        print("Target file dates:\n", target_file_dates)
        self.logger.info(f"Target file dates: {target_file_dates}")
        recent_target_file_date = None if len(target_file_dates) == 0 else target_file_dates[-1]
        print("Recent target file date:", recent_target_file_date)
        self.logger.info(f"Recent target file date: {recent_target_file_date}")
        print()

        # determine the missing file dates to load the data for
        missing_file_dates = source_file_dates if recent_target_file_date is None \
            else list(filter(lambda fd: fd > recent_target_file_date, source_file_dates))
        if not etl_params.is_filled_missing_dates and len(missing_file_dates) == 0:
            print("No new data available. Finishing.")
            self.logger.info(f"No new data available. Finishing.")
            raise error.NoNewDataError("No new data available for ETL.")
        print(f"\nLoading data for the following dates:\n{missing_file_dates}\n")
        self.logger.info(f"Loading data for the following dates: {missing_file_dates}")

        # get reddit and comment texts
        reddits = self.reddit_provider.get_reddits(phrase=etl_params.phrase, file_dates=missing_file_dates)
        comments = self.comment_provider.get_comments(phrase=etl_params.phrase, file_dates=missing_file_dates)
        entries = reddits + comments

        print("Reddit and comment entries loaded:", len(entries))
        self.logger.info(f"Reddit and comment entries loaded: {len(entries)}")

        # process reddit and comment entries
        print("Processing reddits and comments...")
        self.logger.info("Processing reddits and comments.")

        vectors = self.get_vectors(entries, etl_params)

        print(f"Vectors processed: {len(vectors)}.\n")
        self.logger.info(f"Vectors processed: {len(vectors)}.")

        # file date gaps detection and filling in with blank records
        if etl_params.is_filled_missing_dates:
            print("Warning. Filling in for missing dates not supported for vectorization ETL process.")
            self.logger.warning("Warning. Filling in for missing dates not supported for vectorization ETL process.")

        # insert vectors
        self.vector_provider.insert_vectors(vectors, batch_size=etl_params.batch_size)

        print("Vectorization ETL process finished.")
        self.logger.info("Vectorization ETL process finished.")
