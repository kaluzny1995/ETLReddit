from abc import ABC, abstractmethod
from typing import List

from model import Reddit


class IFileRedditProvider(ABC):
    """ FileRedditProvider interface """

    @abstractmethod
    def get_reddits(self, file_dates: List[str], phrase: str) -> List[Reddit]:
        """ Returns a list of Reddit objects """
        pass
