from abc import ABC, abstractmethod
from typing import List

from model import Comment


class ICommentProvider(ABC):
    """ Comments provider interface """

    @abstractmethod
    def _create_if_not_exists(self) -> None:
        """ Creates 'comments' table if not exists """
        pass

    @abstractmethod
    def insert_comments(self, comments: List[Comment], batch_size: int = 100) -> None:
        """ Inserts the comments into database """
        pass
