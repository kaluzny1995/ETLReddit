import os
import logging
import pickle
from typing import List
from sklearn.decomposition import PCA
from sklearn.manifold import Isomap
import numpy as np
import multiprocessing

import error
import util
from model import EReductionModel, ETLParams, ReductionResult, Vector, Reduction
from provider import IDbVectorProvider, IDbReductionProvider, \
    MongoProvider, MongoDbVectorProvider, SupabasePostgresProvider, SupabasePostgresDbReductionProvider
from service import IReductionService


class ReductionService(IReductionService):
    """ Reduction service class """

    logger: logging.Logger
    vector_provider: IDbVectorProvider
    reduction_provider: IDbReductionProvider

    pca2: PCA
    pca3: PCA
    iso2: Isomap
    iso3: Isomap

    def __init__(self, logger: logging.Logger | None = None,
                 vector_provider: IDbVectorProvider | None = None,
                 reduction_provider: IDbReductionProvider | None = None) -> None:
        self.logger = logger or util.setup_logger(name="reduction_service",
                                                  log_file=f"logs/other/reduction_service.log")

        supabase_postgres_provider = SupabasePostgresProvider(logger=self.logger)
        mongo_provider = MongoProvider(logger=self.logger)
        self.vector_provider = vector_provider or MongoDbVectorProvider(mongo_provider)
        self.reduction_provider = reduction_provider or SupabasePostgresDbReductionProvider(supabase_postgres_provider)

        self.pca2 = self._load_reduction_model(reduction_model=EReductionModel.PCA2)
        self.pca3 = self._load_reduction_model(reduction_model=EReductionModel.PCA3)
        self.iso2 = self._load_reduction_model(reduction_model=EReductionModel.ISO2, max_vectors=30000)
        self.iso3 = self._load_reduction_model(reduction_model=EReductionModel.ISO3, max_vectors=30000)

    def _load_reduction_model(self, reduction_model: EReductionModel, max_vectors: int | None = None) -> PCA | Isomap:
        """ Loads the dimensionality reduction model or trains if such not exist """
        model_path = f"stored_pkls/{reduction_model.value.lower()}.pkl"
        model = None
        if not os.path.exists(model_path):
            print(f"Model '{reduction_model.value.lower()}' not found. Training using existing vector embeddings.")
            self.logger.info(f"Model '{reduction_model.value.lower()}' not found. Training using existing vector embeddings.")

            vectors = self.vector_provider.get_vectors()
            embeddings = Reduction.get_embeddings(vectors)
            if max_vectors is not None:
                embeddings = embeddings[:max_vectors]

            if reduction_model == EReductionModel.PCA2:
                model = PCA(n_components=2)
            elif reduction_model == EReductionModel.PCA3:
                model = PCA(n_components=3)
            elif reduction_model == EReductionModel.ISO2:
                model = Isomap(n_components=2)
            elif reduction_model == EReductionModel.ISO3:
                model = Isomap(n_components=3)
            else:
                self.logger.error(f"Unknown reduction model: {reduction_model}. Should be from set: {list(map(lambda v: v.lower(), EReductionModel.__members__))}")
                raise ValueError(f"Unknown reduction model: {reduction_model}. Should be from set: {list(map(lambda v: v.lower(), EReductionModel.__members__))}")

            print(f"Starting model {reduction_model.value.lower()} training.")
            self.logger.info(f"Starting model {reduction_model.value.lower()} training.")
            model.fit(np.array(embeddings))

            with open(model_path, "wb") as f:
                pickle.dump(model, f)
            print(f"Training finished. Model {reduction_model.value.lower()} saved.")
            self.logger.info(f"Training finished. Model {reduction_model.value.lower()} saved.")
        else:
            with open(model_path, "rb") as f:
                model = pickle.load(f)
            print(f"Model '{reduction_model.value.lower()}' loaded.")
            self.logger.info(f"Model '{reduction_model.value.lower()}' loaded.")
        return model

    def get_reductions(self, vectors: List[Vector], params: ETLParams) -> List[Reduction]:
        """ Returns the processed reductions from given vectors """
        results = list([])
        if params.is_multiprocessing_used and len(vectors) > params.num_processes ** 2:
            queue = multiprocessing.Queue()
            for i, vectors_chunk in enumerate(util.chunk_list_n_elements(vectors, params.num_processes)):
                p = multiprocessing.Process(target=self._multiprocess_vectors, args=(vectors_chunk, i, queue))
                p.start()

            for i in range(params.num_processes):
                reductions_chunk, num = queue.get()
                results.extend(reductions_chunk)
        else:
            results.extend(self._process_vectors(vectors))
        return results

    def _process_vectors(self, vectors: List[Vector]) -> List[Reduction]:
        """ Processes vectors and returns their reductions (reduced vectors) """
        embeddings = Reduction.get_embeddings(vectors)
        reductions = list([])

        if len(reductions) > 0:
            pca2_out = self.pca2.transform(np.array(embeddings)).tolist()
            pca3_out = self.pca3.transform(np.array(embeddings)).tolist()
            iso2_out = self.iso2.transform(np.array(embeddings)).tolist()
            iso3_out = self.iso3.transform(np.array(embeddings)).tolist()

            for vector, pca2, pca3, iso2, iso3 in zip(vectors, pca2_out, pca3_out, iso2_out, iso3_out):
                reduction_result = ReductionResult(
                    pca2_0=pca2[0], pca2_1=pca2[1], pca3_0=pca3[0], pca3_1=pca3[1], pca3_2=pca3[2],
                    iso2_0=iso2[0], iso2_1=iso2[1], iso3_0=iso3[0], iso3_1=iso3[1], iso3_2=iso3[2]
                )
                reductions.append(Reduction.from_vector(vector, reduction_result))

        return reductions

    def _multiprocess_vectors(self, vectors: List[Vector], num: int, queue: multiprocessing.Queue) -> None:
        """ Processes vectors and returns their reductions (reduced vectors) using multiprocess approach"""
        print(f"P{num + 1}: Starting processing vectors.")
        self.logger.info(f"P{num + 1}: Starting processing vectors.")

        processed_reductions = self._process_vectors(vectors)

        print(f"P{num + 1}: Finished processing. Processed out reductions: {len(processed_reductions)}.")
        self.logger.info(f"P{num + 1}: Finished processing. Processed out reductions: {len(processed_reductions)}.")

        queue.put((processed_reductions, num))
        pass

    def run_etl(self, **etl_params_dict) -> None:
        """ Runs ETL process loading expected vectors, processing and persisting expected reductions """
        etl_params = ETLParams(**etl_params_dict)

        print("Starting reduction ETL process.")
        self.logger.info("Starting reduction ETL process.")

        # load source file dates
        source_file_dates = sorted(self.vector_provider.get_file_dates(phrase=etl_params.phrase))
        print("Source file dates:\n", source_file_dates)
        self.logger.info(f"Source file dates: {source_file_dates}")

        # load target files dates
        target_file_dates = sorted(self.reduction_provider.get_file_dates(phrase=etl_params.phrase))
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

        # get vectors
        vectors = self.vector_provider.get_vectors(phrase=etl_params.phrase, file_dates=missing_file_dates)

        print("Vectors loaded:", len(vectors))
        self.logger.info(f"Vectors loaded: {len(vectors)}")

        # process vectors
        print("Processing reddits and comments...")
        self.logger.info("Processing reddits and comments.")

        reductions = self.get_reductions(vectors, etl_params)

        print(f"Reductions processed: {len(reductions)}.\n")
        self.logger.info(f"Reductions processed: {len(reductions)}.")

        # file date gaps detection and filling in with blank records
        if etl_params.is_filled_missing_dates:
            print("Warning. Filling in for missing dates not supported for reduction ETL process.")
            self.logger.warning("Warning. Filling in for missing dates not supported for reduction ETL process.")

        # insert reductions
        self.reduction_provider.insert_reductions(reductions, batch_size=etl_params.batch_size)

        print("Reduction ETL process finished.")
        self.logger.info("Reduction ETL process finished.")
