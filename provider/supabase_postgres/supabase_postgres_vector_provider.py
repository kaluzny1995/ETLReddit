from sqlmodel import select
from typing import List

from model import Vector
from provider import IDbProvider, IDbVectorProvider, SupabasePostgresProvider


class SupabasePostgresDbVectorProvider(IDbVectorProvider):
    """ Vectors provider from Postgres Supabase database """

    supabase_postgres_provider: IDbProvider

    def __init__(self, supabase_postgres_provider: IDbProvider | None = None):
        super(SupabasePostgresDbVectorProvider, self).__init__()
        self.supabase_postgres_provider = supabase_postgres_provider or SupabasePostgresProvider()

    def create_if_not_exists(self) -> None:
        """ Creates 'vectors' table if not exists """
        self.supabase_postgres_provider.create_table_if_not_exists(Vector, table="vectors", schema="reddit")

    def get_file_dates(self, phrase: str) -> List[str]:
        """ Returns the file dates of vector of given phrase """
        self.create_if_not_exists()

        statement = select(Vector.file_date).where(Vector.phrase == phrase).distinct()
        file_dates = self.supabase_postgres_provider.run_select_statement(statement)
        return list(file_dates)

    def get_vectors(self, phrase: str | None = None) -> List[Vector]:
        """ Returns the vectors of given phrase """
        self.create_if_not_exists()

        statement = select(Vector)
        if phrase is not None:
            statement = statement.where(Vector.phrase == phrase)
        vectors = self.supabase_postgres_provider.run_select_statement(statement)
        return vectors

    def insert_vectors(self, vectors: List[Vector], batch_size: int = 100) -> None:
        """ Inserts the vectors into database """
        self.create_if_not_exists()
        self.supabase_postgres_provider.run_insert_statement(vectors, batch_size, num_entities=len(vectors), name="vectors")
