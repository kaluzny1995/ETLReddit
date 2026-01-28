from abc import ABC, abstractmethod
from typing import List

from model import Reddit


class IRedditProvider(ABC):
    """ Reddits provider interface """

    @abstractmethod
    def _create_if_not_exists(self) -> None:
        """ Creates 'reddits' table if not exists """
        pass

    @abstractmethod
    def get_file_dates(self, phrase: str, which: str = "start") -> List[str]:
        """ Returns the file dates of reddits of given phrase """
        pass

    @abstractmethod
    def insert_reddits(self, reddits: List[Reddit], batch_size: int = 100) -> None:
        """ Inserts the reddits into database """
        pass
