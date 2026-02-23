from abc import ABC, abstractmethod
from typing import List

from model import Comment


class IJsonCommentProvider(ABC):
    """ JsonCommentProvider interface """

    @abstractmethod
    def get_comments(self, file_dates: List[str], phrase: str) -> List[Comment]:
        """ Returns a list of Comment objects """
        pass
