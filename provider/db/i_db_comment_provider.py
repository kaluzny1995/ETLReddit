from abc import ABC, abstractmethod
from typing import List

from model import EFileDateType, Comment


class IDbCommentProvider(ABC):
    """ Comments provider interface """

    @abstractmethod
    def create_if_not_exists(self) -> None:
        """ Creates 'comments' table if not exists """
        pass

    @abstractmethod
    def get_comments(self, phrase: str, file_dates: List[str], which: EFileDateType = EFileDateType.START) -> List[Comment]:
        """ Returns the comments of given phrase for given list of file dates """
        pass

    @abstractmethod
    def insert_comments(self, comments: List[Comment], batch_size: int = 10000) -> None:
        """ Inserts the comments into database """
        pass
