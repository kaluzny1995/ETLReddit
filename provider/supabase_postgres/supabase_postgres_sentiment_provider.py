from sqlmodel import select
from typing import List

from model import Sentiment
from provider import IDbProvider, IDbSentimentProvider, SupabasePostgresProvider


class SupabasePostgresDbSentimentProvider(IDbSentimentProvider):
    """ Sentiments provider from Postgres Supabase database """

    supabase_postgres_provider: IDbProvider

    def __init__(self, supabase_postgres_provider: IDbProvider | None = None):
        super(SupabasePostgresDbSentimentProvider, self).__init__()
        self.supabase_postgres_provider = supabase_postgres_provider or SupabasePostgresProvider()

    def create_if_not_exists(self) -> None:
        """ Creates 'sentiments' table if not exists """
        self.supabase_postgres_provider.create_table_if_not_exists(Sentiment, table="sentiments", schema="reddit")

    def get_file_dates(self, phrase: str) -> List[str]:
        """ Returns the file dates of sentiment of given phrase """
        self.create_if_not_exists()

        statement = select(Sentiment.file_date).where(Sentiment.phrase == phrase).distinct()
        file_dates = self.supabase_postgres_provider.run_select_statement(statement)
        return list(file_dates)

    def get_sentiments(self, phrase: str) -> List[Sentiment]:
        """ Returns the sentiments of given phrase """
        self.create_if_not_exists()

        statement = select(Sentiment).where(Sentiment.phrase == phrase)
        sentiments = self.supabase_postgres_provider.run_select_statement(statement)
        return sentiments

    def insert_sentiments(self, sentiments: List[Sentiment], batch_size: int = 100) -> None:
        """ Inserts the sentiments into database """
        self.create_if_not_exists()
        self.supabase_postgres_provider.run_insert_statement(sentiments, batch_size, num_entities=len(sentiments), name="sentiments")
