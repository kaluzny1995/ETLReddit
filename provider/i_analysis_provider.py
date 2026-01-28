from abc import ABC, abstractmethod
from typing import List

from model import Analysis


class IAnalysisProvider(ABC):
    """ Analysis provider interface """

    @abstractmethod
    def _create_if_not_exists(self) -> None:
        """ Creates 'analyses' table if not exists """
        pass

    @abstractmethod
    def get_file_dates(self, phrase: str) -> List[str]:
        """ Returns the file dates of analysis of given phrase """
        pass

    @abstractmethod
    def get_analyses(self, phrase: str) -> List[Analysis]:
        """ Returns the analyses of given phrase """
        pass

    @abstractmethod
    def insert_analyses(self, analyses: List[Analysis], batch_size: int = 100) -> None:
        """ Inserts the analyses into database """
        pass
