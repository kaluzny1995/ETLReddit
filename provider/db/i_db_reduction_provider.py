from abc import ABC, abstractmethod
from typing import List

from model import Reduction


class IDbReductionProvider(ABC):
    """ Reduction provider interface """

    @abstractmethod
    def create_if_not_exists(self) -> None:
        """ Creates 'reductions' table if not exists """
        pass

    @abstractmethod
    def get_file_dates(self, phrase: str) -> List[str]:
        """ Returns the file dates of reduction of given phrase """
        pass

    @abstractmethod
    def get_reductions(self, phrase: str) -> List[Reduction]:
        """ Returns the reductions of given phrase """
        pass

    @abstractmethod
    def insert_reductions(self, reductions: List[Reduction], batch_size: int = 10000) -> None:
        """ Inserts the reductions into database """
        pass