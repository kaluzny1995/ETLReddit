from sqlmodel import select
from typing import List

from model import Popularity
from provider import IDbProvider, IDbPopularityProvider, SupabasePostgresProvider


class SupabasePostgresDbPopularityProvider(IDbPopularityProvider):
    """ Sentiments provider from Postgres Supabase database """

    supabase_postgres_provider: IDbProvider

    def __init__(self, supabase_postgres_provider: IDbProvider | None = None):
        super(SupabasePostgresDbPopularityProvider, self).__init__()
        self.supabase_postgres_provider = supabase_postgres_provider or SupabasePostgresProvider()
    
    def create_if_not_exists(self) -> None:
        """ Creates 'popularities' table if not exists """
        self.supabase_postgres_provider.create_table_if_not_exists(Popularity, table="popularities", schema="reddit")

    def get_file_dates(self, phrase: str) -> List[str]:
        """ Returns the file dates of popularity of given phrase """
        self.create_if_not_exists()

        statement = select(Popularity.file_date).where(Popularity.phrase == phrase).distinct()
        file_dates = self.supabase_postgres_provider.run_select_statement(statement)
        return list(file_dates)

    def get_popularities(self, phrase: str) -> List[Popularity]:
        """ Returns the popularities of given phrase """
        self.create_if_not_exists()

        statement = select(Popularity).where(Popularity.phrase == phrase)
        sentiments = self.supabase_postgres_provider.run_select_statement(statement)
        return sentiments

    def insert_popularities(self, popularities: List[Popularity], batch_size: int = 10000) -> None:
        """ Inserts the popularities into database """
        self.create_if_not_exists()
        self.supabase_postgres_provider.run_insert_statement(popularities, batch_size, num_entities=len(popularities), name="popularities")
