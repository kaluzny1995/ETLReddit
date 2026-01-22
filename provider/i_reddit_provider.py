from abc import ABC, abstractmethod
from typing import List

from model import Reddit


class IRedditProvider(ABC):
    """ Reddits provider interface """

    @abstractmethod
    def get_file_dates(self, which: str = "start") -> List[str]:
        """ Returns the file dates of reddits """
        pass

    @abstractmethod
    def insert_reddits(self, reddits: List[Reddit], batch_size: int = 100) -> None:
        """ Inserts the reddits into database """
        pass
