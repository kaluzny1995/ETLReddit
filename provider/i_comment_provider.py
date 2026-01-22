from abc import ABC, abstractmethod
from typing import List

from model import Comment


class ICommentProvider(ABC):
    """ Comments provider interface """

    @abstractmethod
    def insert_comments(self, comments: List[Comment], batch_size: int = 100) -> None:
        """ Inserts the comments into database """
        pass
