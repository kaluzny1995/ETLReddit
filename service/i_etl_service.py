from abc import ABC, abstractmethod
from typing import List

from sqlmodel import SQLModel


class IETLService(ABC):
    """ Interface for all ETL services """

    @abstractmethod
    def run_etl(self, entries: List[SQLModel]) -> List[SQLModel]:
        """ Runs ETL service processing input entries and returning output results """
        pass
