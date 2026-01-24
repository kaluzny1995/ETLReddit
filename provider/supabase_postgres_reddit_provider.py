import sqlalchemy
from sqlmodel import create_engine, Session, select, SQLModel
from typing import List

import util
from model import SupabaseConnectionConfig, EFileDateType, Reddit
from provider import IRedditProvider


class SupabasePostgresRedditProvider(IRedditProvider):
    """ Reddits provider from Postgres Supabase database """

    connection_string: str
    db_engine: sqlalchemy.engine.Engine

    def __init__(self, connection_string: str | None = None, db_engine: sqlalchemy.engine.Engine | None = None):
        super(SupabasePostgresRedditProvider, self).__init__()
        self.connection_string = connection_string or SupabaseConnectionConfig.get_db_connection_string()
        self.db_engine = db_engine or create_engine(self.connection_string)

    def _create_if_not_exists(self) -> None:
        """ Creates 'reddits' database if not exists """
        if not sqlalchemy.inspect(self.db_engine).has_table(table_name="reddits", schema="reddit"):
            SQLModel.metadata.create_all(self.db_engine, tables=[Reddit.__table__])

    def get_file_dates(self, phrase: str, which: EFileDateType = EFileDateType.START) -> List[str]:
        """ Returns the file dates of reddits of given phrase """
        self._create_if_not_exists()

        with Session(self.db_engine) as db_session:
            statement = select(Reddit.start_file_date) if which == EFileDateType.START else select(Reddit.end_file_date)
            statement = statement.where(Reddit.phrase == phrase).distinct()
            file_dates = db_session.exec(statement).all()
        return list(file_dates)

    def insert_reddits(self, reddits: list[Reddit], batch_size: int = 100) -> None:
        """ Inserts the reddits into database """
        self._create_if_not_exists()

        reddit_chunks = util.chunk_list(reddits, batch_size)
        with Session(self.db_engine) as db_session:
            num_inserted = 0
            print("Inserting reddits:")
            for chunk in reddit_chunks:
                db_session.add_all(chunk)
                db_session.commit()
                num_inserted += len(chunk)
                print(f"{num_inserted} out of {len(reddits)}")
            print("Reddits inserted.")
