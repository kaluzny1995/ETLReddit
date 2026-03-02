from typing import List

from model.entity.sentiment import Sentiment
from provider import IDbSentimentProvider


class SupabasePostgresSentimentProviderStub(IDbSentimentProvider):
    """ Sentiments provider stub for testing """

    data: List[Sentiment]

    def __init__(self, data: List[Sentiment]):
        self.data = data

    def create_if_not_exists(self) -> None:
        """ Creates 'sentiments' table if not exists """
        pass

    def get_file_dates(self, phrase: str) -> List[str]:
        """ Returns the file dates of sentiment of given phrase """
        return list(map(lambda x: x.file_date, self.data))

    def get_sentiments(self, phrase: str) -> List[Sentiment]:
        """ Returns the sentiments of given phrase """
        return self.data

    def insert_sentiments(self, sentiments: List[Sentiment], batch_size: int = 10000) -> None:
        """ Inserts the sentiments into database """
        pass
