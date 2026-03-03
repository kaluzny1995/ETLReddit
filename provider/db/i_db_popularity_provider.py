from abc import ABC, abstractmethod
from typing import List

from model import Popularity


class IDbPopularityProvider(ABC):
    """ Popularity provider interface """

    @abstractmethod
    def create_if_not_exists(self) -> None:
        """ Creates 'popularities' table if not exists """
        pass

    @abstractmethod
    def get_file_dates(self, phrase: str) -> List[str]:
        """ Returns the file dates of popularity of given phrase """
        pass

    @abstractmethod
    def get_popularities(self, phrase: str) -> List[Popularity]:
        """ Returns the popularities of given phrase """
        pass

    @abstractmethod
    def insert_popularities(self, popularities: List[Popularity], batch_size: int = 10000) -> None:
        """ Inserts the popularities into database """
        pass
