import multiprocessing
import logging
from typing import List
from tqdm import tqdm

import error
import util
from model import ETLParams, Reddit, Comment, Popularity
from provider import IDbRedditProvider, IDbCommentProvider, IDbPopularityProvider, \
    SupabasePostgresProvider, SupabasePostgresDbRedditProvider, \
    SupabasePostgresDbCommentProvider, SupabasePostgresDbPopularityProvider
from service import IPopularityService


class PopularityService(IPopularityService):
    """ Popularity service class """

    logger: logging.Logger
    reddit_provider: IDbRedditProvider
    comment_provider: IDbCommentProvider
    popularity_provider: IDbPopularityProvider

    def __init__(self, logger: logging.Logger | None = None,
                 reddit_provider: IDbRedditProvider | None = None,
                 comment_provider: IDbCommentProvider | None = None,
                 popularity_provider: IDbPopularityProvider | None = None) -> None:
        self.logger = logger or util.setup_logger(name="popularity_service",
                                                  log_file=f"logs/other/popularity_service.log")

        supabase_postgres_provider = SupabasePostgresProvider(logger=self.logger)
        self.reddit_provider = reddit_provider or SupabasePostgresDbRedditProvider(supabase_postgres_provider)
        self.comment_provider = comment_provider or SupabasePostgresDbCommentProvider(supabase_postgres_provider)
        self.popularity_provider = popularity_provider or SupabasePostgresDbPopularityProvider(supabase_postgres_provider)

    def get_popularities(self, entries: List[Reddit | Comment], params: ETLParams) -> List[Popularity]:
        """ Returns the processed popularities from given entries """
        results = list([])
        if params.is_multiprocessing_used and len(entries) > params.num_processes ** 2:
            queue = multiprocessing.Queue()
            for i, entries_chunk in enumerate(util.chunk_list_n_elements(entries, params.num_processes)):
                p = multiprocessing.Process(target=self._multiprocess_entries, args=(entries_chunk, i, queue))
                p.start()

            for i in range(params.num_processes):
                results_chunk, num = queue.get()
                results.extend(results_chunk)
        else:
            for entry in tqdm(entries):
                results.append(self._process_entry(entry))
        return results

    def _process_entry(self, entry: Reddit | Comment) -> Popularity:
        """ Processes single reddit or comment entry and returns popularity """
        if type(entry) not in [Reddit, Comment]:
            self.logger.error(f"The provided entity for ETL has improper type: {type(entry)}.")
            raise error.WrongEntityError(f"The provided entity for ETL has improper type: {type(entry)}.")

        if isinstance(entry, Reddit):
            return Popularity.from_reddit(entry)
        else:
            return Popularity.from_comment(entry)

    def _multiprocess_entries(self, entries: List[Reddit | Comment], num: int, queue: multiprocessing.Queue) -> None:
        """ Partially processes reddit and comment entries (utilizes multiprocessing) """
        print(f"P{num + 1}: Starting processing reddit and comment entries.")
        self.logger.info(f"P{num + 1}: Starting processing reddit and comment entries.")

        processed_popularities = list([])
        for i, entry in enumerate(entries):
            popularity = self._process_entry(entry)
            processed_popularities.append(popularity)

            if len(processed_popularities) % 100 == 0 and len(processed_popularities) > 0:
                print(f"P{num + 1}: Processed {len(processed_popularities)} out of {len(entries)} entries.")
                self.logger.info(f"P{num + 1}: Processed {len(processed_popularities)} out of {len(entries)} entries.")

        print(f"P{num + 1}: Finished processing entries. Processed: {len(processed_popularities)}.")
        self.logger.info(f"P{num + 1}: Finished processing entries. Processed: {len(processed_popularities)}.")

        queue.put((processed_popularities, num))

    def run_etl(self, **etl_params_dict) -> None:
        """ Runs ETL process loading expected reddits and comments, processing and persisting expected popularities """
        etl_params = ETLParams(**etl_params_dict)

        print("Starting popularity ETL process.")
        self.logger.info("Starting popularity ETL process.")

        # load source file dates
        source_file_dates = sorted(self.reddit_provider.get_file_dates(phrase=etl_params.phrase))
        print("Source file dates:\n", source_file_dates)
        self.logger.info(f"Source file dates: {source_file_dates}")

        # load target files dates
        target_file_dates = sorted(self.popularity_provider.get_file_dates(phrase=etl_params.phrase))
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

        # get reddit and comment entries
        reddits = self.reddit_provider.get_reddits(phrase=etl_params.phrase, file_dates=missing_file_dates)
        comments = self.comment_provider.get_comments(phrase=etl_params.phrase, file_dates=missing_file_dates)
        entries = reddits + comments

        print("Reddit and comment entries loaded:", len(entries))
        self.logger.info(f"Reddit and comment entries loaded: {len(entries)}")

        # process reddit and comment entries
        print("Processing reddits and comments:")
        self.logger.info("Processing reddits and comments.")

        popularities = self.get_popularities(entries, etl_params)

        print(f"Popularities processed: {len(popularities)}.\n")
        self.logger.info(f"Popularities processed: {len(popularities)}.")

        # file date gaps detection and filling in with blank records
        if etl_params.is_filled_missing_dates:
            print("Warning. Filling in for missing dates not supported for popularity ETL process.")
            self.logger.warning("Warning. Filling in for missing dates not supported for popularity ETL process.")

        # insert popularities
        self.popularity_provider.insert_popularities(popularities, batch_size=etl_params.batch_size)

        print("Popularity ETL process finished.")
        self.logger.info("Popularity ETL process finished.")
