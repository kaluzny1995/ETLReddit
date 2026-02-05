from sqlmodel import select
from typing import List

from model import SentimentAnalysis
from provider import IDbProvider, IDbSentimentAnalysisProvider, SupabasePostgresProvider


class SupabasePostgresDbSentimentAnalysisProvider(IDbSentimentAnalysisProvider):
    """ Sentiment analyses provider from Postgres Supabase database """

    supabase_postgres_provider: IDbProvider

    def __init__(self, supabase_postgres_provider: IDbProvider | None = None):
        super(SupabasePostgresDbSentimentAnalysisProvider, self).__init__()
        self.supabase_postgres_provider = supabase_postgres_provider or SupabasePostgresProvider()

    def create_if_not_exists(self) -> None:
        """ Creates 'sentiment analyses' table if not exists """
        self.supabase_postgres_provider.create_table_if_not_exists(SentimentAnalysis, table="sentiment_analyses", schema="reddit")

    def get_file_dates(self, phrase: str) -> List[str]:
        """ Returns the file dates of sentiment analysis of given phrase """
        self.create_if_not_exists()

        statement = select(SentimentAnalysis.file_date).where(SentimentAnalysis.phrase == phrase).distinct()
        file_dates = self.supabase_postgres_provider.run_select_statement(statement)
        return list(file_dates)

    def get_sentiment_analyses(self, phrase: str) -> List[SentimentAnalysis]:
        """ Returns the sentiment analyses of given phrase """
        self.create_if_not_exists()

        statement = select(SentimentAnalysis).where(SentimentAnalysis.phrase == phrase)
        sentiment_analyses = self.supabase_postgres_provider.run_select_statement(statement)
        return sentiment_analyses

    def insert_sentiment_analyses(self, sentiment_analyses: List[SentimentAnalysis], batch_size: int = 100) -> None:
        """ Inserts the sentiment analyses into database """
        self.create_if_not_exists()
        self.supabase_postgres_provider.run_insert_statement(sentiment_analyses, batch_size, num_entities=len(sentiment_analyses), name="sentiment analyses")
