from sqlmodel import select
from typing import List

from model import EFileDateType, Reddit
from provider import IDbProvider, IDbRedditProvider, SupabasePostgresProvider


class SupabasePostgresDbRedditProvider(IDbRedditProvider):
    """ Reddits provider from Postgres Supabase database """

    supabase_postgres_provider: IDbProvider

    def __init__(self, supabase_postgres_provider: IDbProvider | None = None):
        super(SupabasePostgresDbRedditProvider, self).__init__()
        self.supabase_postgres_provider = supabase_postgres_provider or SupabasePostgresProvider()

    def create_if_not_exists(self) -> None:
        """ Creates 'reddits' table if not exists """
        self.supabase_postgres_provider.create_table_if_not_exists(Reddit, table="reddits", schema="reddit")

    def get_file_dates(self, phrase: str, which: EFileDateType = EFileDateType.START) -> List[str]:
        """ Returns the file dates of reddits of given phrase """
        self.create_if_not_exists()

        statement = select(Reddit.start_file_date) if which == EFileDateType.START else select(Reddit.end_file_date)
        statement = statement.where(Reddit.phrase == phrase).distinct()
        file_dates = self.supabase_postgres_provider.run_select_statement(statement)
        return list(file_dates)

    def get_reddits(self, phrase: str, file_dates: List[str], which: EFileDateType = EFileDateType.START) -> List[Reddit]:
        """ Returns the reddits of given phrase for given list of file dates """
        self.create_if_not_exists()

        statement = select(Reddit).where(Reddit.phrase == phrase)
        statement = statement.where(Reddit.start_file_date.in_(file_dates)) \
            if which == EFileDateType.START else statement.where(Reddit.end_file_date.in_(file_dates))
        reddits = self.supabase_postgres_provider.run_select_statement(statement)
        return list(reddits)

    def insert_reddits(self, reddits: list[Reddit], batch_size: int = 100) -> None:
        """ Inserts the reddits into database """
        self.create_if_not_exists()
        self.supabase_postgres_provider.run_insert_statement(reddits, batch_size, num_entities=len(reddits), name="reddits")
