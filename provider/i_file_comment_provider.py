from abc import ABC, abstractmethod
from typing import List

from model import Comment


class IFileCommentProvider(ABC):
    """ FileCommentProvider interface """

    @abstractmethod
    def get_comments(self, file_dates: List[str], phrase: str) -> List[Comment]:
        """ Returns a list of Comment objects """
        pass
