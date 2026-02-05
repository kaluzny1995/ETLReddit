from abc import ABC, abstractmethod
from typing import List, Any

from sqlmodel import SQLModel, Sequence
from sqlmodel.sql._expression_select_cls import Select, SelectOfScalar


class IDbProvider(ABC):
    """ Database provider interface """

    @abstractmethod
    def connect(self) -> None:
        """ Connects to the database """
        pass

    @abstractmethod
    def create_table_if_not_exists(self, entity: SQLModel, table: str, schema: str) -> None:
        """ Creates table if not exists """
        pass

    @abstractmethod
    def run_select_statement(self, statement: Select | SelectOfScalar) -> Sequence[Any]:
        """ Executes select statement and returns results """
        pass

    @abstractmethod
    def run_insert_statement(self, entities: List[SQLModel], batch_size: int,
                             num_entities: int = 10000, name: str = "entities") -> None:
        """ Executes insert statement """
        pass
