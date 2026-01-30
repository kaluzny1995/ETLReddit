import sqlalchemy
from sqlmodel import create_engine, Session, select, SQLModel
from typing import List

import util
from model import SupabaseConnectionConfig, Author
from provider.i_author_provider import IAuthorProvider


class SupabasePostgresAuthorProvider(IAuthorProvider):
    """ Authors provider from Postgres Supabase database """

    connection_string: str
    db_engine: sqlalchemy.engine.Engine

    def __init__(self, connection_string: str | None = None, db_engine: sqlalchemy.engine.Engine | None = None):
        super(SupabasePostgresAuthorProvider, self).__init__()
        self.connection_string = connection_string or SupabaseConnectionConfig.get_db_connection_string()
        self.db_engine = db_engine or create_engine(self.connection_string)

    def _create_if_not_exists(self) -> None:
        """ Creates 'authors' database if not exists """
        if not sqlalchemy.inspect(self.db_engine).has_table(table_name="authors", schema="reddit"):
            SQLModel.metadata.create_all(self.db_engine, tables=[Author.__table__])

    def get_names(self) -> List[str]:
        """ Return a list of authors names """
        self._create_if_not_exists()

        with Session(self.db_engine) as db_session:
            statement = select(Author.name).distinct()
            names = db_session.exec(statement).all()
        return list(names)

    def insert_authors(self, authors: List[Author], batch_size: int = 100) -> None:
        """ Inserts the authors into database """
        self._create_if_not_exists()

        author_chunks = util.chunk_list_equal_size(authors, batch_size)
        with Session(self.db_engine) as db_session:
            num_inserted = 0
            print("Inserting authors:")
            for chunk in author_chunks:
                db_session.add_all(chunk)
                db_session.commit()
                num_inserted += len(chunk)
                print(f"{num_inserted} out of {len(authors)}")
            print("Authors inserted.")
