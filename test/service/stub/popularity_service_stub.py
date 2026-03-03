from typing import List

from model import ETLParams, Reddit, Comment, Popularity
from service import IPopularityService


class PopularityServiceStub(IPopularityService):
    """ Popularity service class """

    def __init__(self):
        pass

    def get_popularities(self, entries: List[Reddit | Comment], params: ETLParams) -> List[Popularity]:
        """ Returns the processed popularities from given entries """
        pass

    def run_etl(self, **etl_params_dict) -> None:
        """ Runs ETL process loading expected reddits and comments, processing and persisting expected popularities """
        pass