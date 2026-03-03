from abc import ABC, abstractmethod
from typing import List

from model import Sentiment


class IDbSentimentProvider(ABC):
    """ Sentiment provider interface """

    @abstractmethod
    def create_if_not_exists(self) -> None:
        """ Creates 'sentiments' table if not exists """
        pass

    @abstractmethod
    def get_file_dates(self, phrase: str) -> List[str]:
        """ Returns the file dates of sentiment of given phrase """
        pass

    @abstractmethod
    def get_sentiments(self, phrase: str) -> List[Sentiment]:
        """ Returns the sentiments of given phrase """
        pass

    @abstractmethod
    def insert_sentiments(self, sentiments: List[Sentiment], batch_size: int = 10000) -> None:
        """ Inserts the sentiments into database """
        pass
