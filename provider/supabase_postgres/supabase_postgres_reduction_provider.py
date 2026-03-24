from sqlmodel import select
from typing import List

from model import Reduction
from provider import IDbProvider, IDbReductionProvider, SupabasePostgresProvider


class SupabasePostgresDbReductionProvider(IDbReductionProvider):
    """ Reductions provider from Postgres Supabase database """

    supabase_postgres_provider: IDbProvider

    def __init__(self, supabase_postgres_provider: IDbProvider | None = None):
        super(SupabasePostgresDbReductionProvider, self).__init__()
        self.supabase_postgres_provider = supabase_postgres_provider or SupabasePostgresProvider()

    def create_if_not_exists(self) -> None:
        """ Creates 'reductions' table if not exists """
        self.supabase_postgres_provider.create_table_if_not_exists(Reduction, table="reductions", schema="reddit")

    def get_file_dates(self, phrase: str) -> List[str]:
        """ Returns the file dates of reduction of given phrase """
        self.create_if_not_exists()

        statement = select(Reduction.file_date).where(Reduction.phrase == phrase).distinct()
        file_dates = self.supabase_postgres_provider.run_select_statement(statement)
        return list(file_dates)

    def get_reductions(self, phrase: str) -> List[Reduction]:
        """ Returns the reductions of given phrase """
        self.create_if_not_exists()

        statement = select(Reduction).where(Reduction.phrase == phrase)
        reductions = self.supabase_postgres_provider.run_select_statement(statement)
        return reductions

    def insert_reductions(self, reductions: List[Reduction], batch_size: int = 100) -> None:
        """ Inserts the reductions into database """
        self.create_if_not_exists()
        self.supabase_postgres_provider.run_insert_statement(reductions, batch_size, num_entities=len(reductions), name="reductions")
