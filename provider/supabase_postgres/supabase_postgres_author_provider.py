from sqlmodel import select
from typing import List

from model import Author
from provider import IDbProvider, IDbAuthorProvider, SupabasePostgresProvider


class SupabasePostgresDbAuthorProvider(IDbAuthorProvider):
    """ Authors provider from Postgres Supabase database """

    supabase_postgres_provider: IDbProvider

    def __init__(self, supabase_postgres_provider: IDbProvider | None = None) -> None:
        super(SupabasePostgresDbAuthorProvider, self).__init__()
        self.supabase_postgres_provider = supabase_postgres_provider or SupabasePostgresProvider()

    def create_if_not_exists(self) -> None:
        """ Creates 'authors' table if not exists """
        self.supabase_postgres_provider.create_table_if_not_exists(Author, table="authors", schema="reddit")

    def get_names(self) -> List[str]:
        """ Return a list of authors names """
        self.create_if_not_exists()

        statement = select(Author.name).distinct()
        names = self.supabase_postgres_provider.run_select_statement(statement)
        return list(names)

    def insert_authors(self, authors: List[Author], batch_size: int = 10000) -> None:
        """ Inserts the authors into database """
        self.create_if_not_exists()
        self.supabase_postgres_provider.run_insert_statement(authors, batch_size, num_entities=len(authors), name="authors")
