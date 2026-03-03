from abc import abstractmethod
from typing import List

from model import ETLParams, Reddit, Comment, Popularity
from service import IETLService


class IPopularityService(IETLService):
    """ Popularity Service interface """

    @abstractmethod
    def get_popularities(self, entries: List[Reddit | Comment], params: ETLParams) -> List[Popularity]:
        """ Returns the processed popularities from given entries """
        pass
