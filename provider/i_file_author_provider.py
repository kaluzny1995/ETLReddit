from abc import ABC, abstractmethod
from typing import List

from model import Author


class IFileAuthorProvider(ABC):
    """ FileAuthorProvider interface """

    @abstractmethod
    def get_authors(self, file_dates: List[str]) -> List[Author]:
        """ Returns a list of Author objects """
        pass
