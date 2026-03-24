from abc import ABC, abstractmethod
from typing import List

from model import Vector


class IDbVectorProvider(ABC):
    """ Vector provider interface """

    @abstractmethod
    def create_if_not_exists(self) -> None:
        """ Creates 'vectors' table if not exists """
        pass

    @abstractmethod
    def get_file_dates(self, phrase: str) -> List[str]:
        """ Returns the file dates of vector of given phrase """
        pass

    @abstractmethod
    def get_vectors(self, phrase: str | None = None) -> List[Vector]:
        """ Returns the vectors of given phrase """
        pass

    @abstractmethod
    def insert_vectors(self, vectors: List[Vector], batch_size: int = 10000) -> None:
        """ Inserts the vectors into database """
        pass