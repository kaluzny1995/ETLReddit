from typing import List

from model import ETLParams, Reddit, Comment, Vector
from service import IVectorService


class VectorServiceStub(IVectorService):
    """ Vector service class """

    def __init__(self):
        pass

    def get_vectors(self, entries: List[Reddit | Comment], params: ETLParams) -> List[Vector]:
        """ Returns the processed vectors from given entries """
        pass

    def run_etl(self, **etl_params_dict) -> None:
        """ Runs ETL process loading expected reddits and comments, processing and persisting expected vectors """
        pass