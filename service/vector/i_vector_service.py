from abc import abstractmethod
from typing import List

from model import ETLParams, Reddit, Comment, Vector
from service import IETLService


class IVectorService(IETLService):
    """ Vector Service interface """

    @abstractmethod
    def get_vectors(self, entries: List[Reddit | Comment], params: ETLParams) -> List[Vector]:
        """ Returns the processed vectors from given entries """
        pass
