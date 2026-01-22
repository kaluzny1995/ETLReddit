from abc import ABC, abstractmethod
from typing import List

from model import Author


class IAuthorProvider(ABC):
    """ Reddits provider interface """

    @abstractmethod
    def get_names(self) -> List[str]:
        """ Return a list of authors names """
        pass

    @abstractmethod
    def insert_authors(self, authors: List[Author], batch_size: int = 100) -> None:
        """ Inserts the authors into database """
        pass
