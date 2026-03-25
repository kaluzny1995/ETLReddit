from abc import abstractmethod
from typing import List

from model import ETLParams, ReductionResult, Vector, Reduction
from service import IETLService


class IReductionService(IETLService):
    """ Reduction Service interface """

    def get_reduction_result(self, vector: Vector) -> ReductionResult:
        """ Returns the reduction result from given vectors """
        pass

    @abstractmethod
    def get_reductions(self, entries: List[Vector], params: ETLParams) -> List[Reduction]:
        """ Returns the processed reductions from given vectors """
        pass
