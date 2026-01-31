from abc import ABC, abstractmethod
from typing import List

from model import SentimentAnalysis


class ISentimentAnalysisProvider(ABC):
    """ SentimentAnalysis provider interface """

    @abstractmethod
    def _create_if_not_exists(self) -> None:
        """ Creates 'sentiment_analyses' table if not exists """
        pass

    @abstractmethod
    def get_file_dates(self, phrase: str) -> List[str]:
        """ Returns the file dates of sentiment analysis of given phrase """
        pass

    @abstractmethod
    def get_sentiment_analyses(self, phrase: str) -> List[SentimentAnalysis]:
        """ Returns the sentiment analyses of given phrase """
        pass

    @abstractmethod
    def insert_sentiment_analyses(self, sentiment_analyses: List[SentimentAnalysis], batch_size: int = 100) -> None:
        """ Inserts the sentiment analyses into database """
        pass
