import pymongo
import logging
from typing import List, Any

from sqlmodel import SQLModel, Sequence
from sqlmodel.sql._expression_select_cls import Select, SelectOfScalar

import util
from model import MongoConnectionConfig
from provider import IDbProvider


class MongoProvider(IDbProvider):
    """ Supabase Postgres database provider class """

    connection_string: str
    db_engine: pymongo.MongoClient
    logger: logging.Logger

    def __init__(self, connection_string: str | None = None,
                 db_engine: pymongo.MongoClient | None = None,
                 logger: logging.Logger | None = None):
        super(IDbProvider, self).__init__()
        self.connection_string = connection_string or MongoConnectionConfig.get_db_connection_string()
        self.db_engine = db_engine or pymongo.MongoClient(self.connection_string)
        self.logger = logger or util.setup_logger(name="m_provider",
                                                  log_file=f"logs/other/m_provider.log")

    def connect(self) -> None:
        """ Connects to the database """
        pass

    def get_logger(self):
        """ Returns the providers logger """
        return self.logger

    def get_db_engine(self) -> pymongo.MongoClient:
        """ Returns the database engine """
        return self.db_engine

    def create_table_if_not_exists(self, entity: SQLModel, table: str, schema: str) -> None:
        """ Creates collection if not exists """
        mcc = MongoConnectionConfig.from_json()
        databases_list = list(map(lambda db: db['name'], self.db_engine.list_databases()))
        if mcc.database not in databases_list:
            self.db_engine.get_database(mcc.database)
            print(f"Mongo database {mcc.database} created.")
            self.logger.info(f"Mongo database {mcc.database} created.")

        collections_list = list(map(lambda col: col['name'], self.db_engine.get_database(mcc.database).list_collections()))
        if table not in collections_list:
            self.db_engine.get_database(mcc.database).get_collection(table)
            print(f"Mongo collection {table} created.")
            self.logger.info(f"Mongo collection {table} created.")

    def run_select_statement(self, statement: Select | SelectOfScalar) -> Sequence[Any]:
        """ Executes select statement and returns results """
        # No need of run select statement method implementation, as it is already run at the object instance level
        pass

    def run_insert_statement(self, entities: List[SQLModel], batch_size: int, num_entities: int = 10000,
                             name: str = "entities") -> None:
        """ Executes insert statement """
        # No need of run insert statement method implementation, as it is already run at the object instance level
        pass