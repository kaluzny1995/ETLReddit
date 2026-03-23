from typing import List

from model import Emotion
from provider import IDbEmotionProvider


class SupabasePostgresEmotionProviderStub(IDbEmotionProvider):
    """ Emotions provider stub for testing """

    data: List[Emotion]

    def __init__(self, data: List[Emotion]):
        self.data = data

    def create_if_not_exists(self) -> None:
        """ Creates 'emotions' table if not exists """
        pass

    def get_file_dates(self, phrase: str) -> List[str]:
        """ Returns the file dates of emotion of given phrase """
        return list(map(lambda x: x.file_date, self.data))

    def get_emotions(self, phrase: str) -> List[Emotion]:
        """ Returns the emotions of given phrase """
        return self.data

    def insert_emotions(self, emotions: List[Emotion], batch_size: int = 10000) -> None:
        """ Inserts the emotions into database """
        pass
