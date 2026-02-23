import sqlalchemy
import logging
from typing import List, Any

from sqlmodel import create_engine, Session, SQLModel, Sequence
from sqlmodel.sql._expression_select_cls import Select, SelectOfScalar

import error
import util
from model.config.supabase_connection_config import SupabaseConnectionConfig
from provider import IDbProvider


class SupabasePostgresProvider(IDbProvider):
    """ Supabase Postgres database provider class """

    connection_string: str
    db_engine: sqlalchemy.engine.Engine
    logger: logging.Logger

    def __init__(self, connection_string: str | None = None,
                 db_engine: sqlalchemy.engine.Engine | None = None,
                 logger: logging.Logger | None = None):
        super(IDbProvider, self).__init__()
        self.connection_string = connection_string or SupabaseConnectionConfig.get_db_connection_string()
        self.db_engine = db_engine or create_engine(self.connection_string)
        self.logger = logger or util.setup_logger(name="sp_provider",
                                                  log_file=f"logs/other/sp_provider.log")

    def connect(self) -> None:
        """ Connects to the database """
        pass

    def create_table_if_not_exists(self, entity: SQLModel, table: str, schema: str) -> None:
        """ Creates table if not exists """
        try:
            if not sqlalchemy.inspect(self.db_engine).has_table(table_name=table, schema=schema):
                SQLModel.metadata.create_all(self.db_engine, tables=[entity.__table__])
                print(f"Table {table} created.")
                self.logger.info(f"Table {table} created.")
        except sqlalchemy.exc.OperationalError as e:
            print(f"Supabase Postgres DB server is down.")
            self.logger.error(f"Supabase Postgres DB server is down.")
            raise error.SupabaseServerDownError(f"Supabase Postgres DB server is down. Message: {e}")

    def run_select_statement(self, statement: Select | SelectOfScalar) -> Sequence[Any]:
        """ Executes select statement and returns results """
        with Session(self.db_engine) as db_session:
            results = db_session.exec(statement).all()
        return results

    def run_insert_statement(self, entities: List[SQLModel], batch_size: int,
                             num_entities: int = 10000, name: str = "entities") -> None:
        """ Executes insert statement """
        entity_chunks = util.chunk_list_equal_size(entities, batch_size)
        with Session(self.db_engine) as db_session:
            num_inserted = 0
            print(f"Inserting {name}:")
            self.logger.info(f"Inserting {name}:")
            for chunk in entity_chunks:
                db_session.add_all(chunk)
                db_session.commit()
                num_inserted += len(chunk)
                print(f"{num_inserted} out of {num_entities}")
                self.logger.info(f"{num_inserted} out of {num_entities}")
            print(f"{name.capitalize()} inserted.")
            self.logger.info(f"{name.capitalize()} inserted.")
