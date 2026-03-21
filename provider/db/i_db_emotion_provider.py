from abc import ABC, abstractmethod
from typing import List

from model import Emotion


class IDbEmotionProvider(ABC):
    """ Emotion provider interface """

    @abstractmethod
    def create_if_not_exists(self) -> None:
        """ Creates 'emotions' table if not exists """
        pass

    @abstractmethod
    def get_file_dates(self, phrase: str) -> List[str]:
        """ Returns the file dates of emotion of given phrase """
        pass

    @abstractmethod
    def get_emotions(self, phrase: str) -> List[Emotion]:
        """ Returns the emotions of given phrase """
        pass

    @abstractmethod
    def insert_emotions(self, emotions: List[Emotion], batch_size: int = 10000) -> None:
        """ Inserts the emotions into database """
        pass