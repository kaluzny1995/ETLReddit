import sqlalchemy
from sqlmodel import create_engine, Session, SQLModel

import util
from model import SupabaseConnectionConfig, Comment
from provider import ICommentProvider


class SupabasePostgresCommentProvider(ICommentProvider):
    """ Comments provider from Postgres Supabase database """

    connection_string: str
    db_engine: sqlalchemy.engine.Engine

    def __init__(self, connection_string: str | None = None, db_engine: sqlalchemy.engine.Engine | None = None):
        super(SupabasePostgresCommentProvider, self).__init__()
        self.connection_string = connection_string or SupabaseConnectionConfig.get_db_connection_string()
        self.db_engine = db_engine or create_engine(self.connection_string)

    def _create_if_not_exists(self) -> None:
        """ Creates 'comments' database if not exists """
        if not sqlalchemy.inspect(self.db_engine).has_table(table_name="comments", schema="reddit"):
            SQLModel.metadata.create_all(self.db_engine, tables=[Comment.__table__])

    def insert_comments(self, comments: list[Comment], batch_size: int = 100) -> None:
        """ Inserts the comments into database """
        self._create_if_not_exists()

        comment_chunks = util.chunk_list(comments, batch_size)
        with Session(self.db_engine) as db_session:
            num_inserted = 0
            print("Inserting comments:")
            for chunk in comment_chunks:
                db_session.add_all(chunk)
                db_session.commit()
                num_inserted += len(chunk)
                print(f"{num_inserted} out of {len(comments)}")
            print("Comments inserted.")

