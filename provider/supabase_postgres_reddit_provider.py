import sqlalchemy
import logging
from sqlmodel import create_engine, Session, select, SQLModel
from typing import List

import util
from model import SupabaseConnectionConfig, EFileDateType, Reddit
from provider import IRedditProvider


class SupabasePostgresRedditProvider(IRedditProvider):
    """ Reddits provider from Postgres Supabase database """

    connection_string: str
    db_engine: sqlalchemy.engine.Engine
    logger: logging.Logger

    def __init__(self, connection_string: str | None = None,
                 db_engine: sqlalchemy.engine.Engine | None = None,
                 logger: logging.Logger | None = None):
        super(SupabasePostgresRedditProvider, self).__init__()
        self.connection_string = connection_string or SupabaseConnectionConfig.get_db_connection_string()
        self.db_engine = db_engine or create_engine(self.connection_string)
        self.logger = logger or util.setup_logger(name="sp_reddit_provider",
                                                  log_file=f"logs/other/sp_reddit_provider.log")

    def _create_if_not_exists(self) -> None:
        """ Creates 'reddits' table if not exists """
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

    def get_reddits(self, phrase: str, file_dates: List[str], which: EFileDateType = EFileDateType.START) -> List[Reddit]:
        """ Returns the reddits of given phrase for given list of file dates """
        self._create_if_not_exists()

        with Session(self.db_engine) as db_session:
            statement = select(Reddit).where(Reddit.phrase == phrase)
            statement = statement.where(Reddit.start_file_date.in_(file_dates)) \
                if which == EFileDateType.START else statement.where(Reddit.end_file_date.in_(file_dates))
            reddits = db_session.exec(statement).all()
        return list(reddits)

    def insert_reddits(self, reddits: list[Reddit], batch_size: int = 100) -> None:
        """ Inserts the reddits into database """
        self._create_if_not_exists()

        reddit_chunks = util.chunk_list_equal_size(reddits, batch_size)
        with Session(self.db_engine) as db_session:
            num_inserted = 0
            print("Inserting reddits:")
            self.logger.info("Inserting reddits:")
            for chunk in reddit_chunks:
                db_session.add_all(chunk)
                db_session.commit()
                num_inserted += len(chunk)
                print(f"{num_inserted} out of {len(reddits)}")
                self.looger.info(f"{num_inserted} out of {len(reddits)}")
            print("Reddits inserted.")
            self.logger.info("Reddits inserted.")
