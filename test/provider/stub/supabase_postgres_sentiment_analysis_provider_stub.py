from typing import List

from model.entity.sentiment_analysis import SentimentAnalysis
from provider import IDbSentimentAnalysisProvider


class SupabasePostgresSentimentAnalysisProviderStub(IDbSentimentAnalysisProvider):
    """ Sentiment analyses provider stub for testing """

    data: List[SentimentAnalysis]

    def __init__(self, data: List[SentimentAnalysis]):
        self.data = data

    def create_if_not_exists(self) -> None:
        """ Creates 'sentiment_analyses' table if not exists """
        pass

    def get_file_dates(self, phrase: str) -> List[str]:
        """ Returns the file dates of sentiment analysis of given phrase """
        pass

    def get_sentiment_analyses(self, phrase: str) -> List[SentimentAnalysis]:
        """ Returns the sentiment analyses of given phrase """
        pass

    def insert_sentiment_analyses(self, sentiment_analyses: List[SentimentAnalysis], batch_size: int = 10000) -> None:
        """ Inserts the sentiment analyses into database """
        pass
