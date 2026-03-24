from typing import List

from model import Vector
from provider import IDbVectorProvider


class SupabasePostgresVectorProviderStub(IDbVectorProvider):
    """ Vectors provider stub for testing """

    data: List[Vector]

    def __init__(self, data: List[Vector]):
        self.data = data

    def create_if_not_exists(self) -> None:
        """ Creates 'vectors' table if not exists """
        pass

    def get_file_dates(self, phrase: str) -> List[str]:
        """ Returns the file dates of vector of given phrase """
        return list(map(lambda x: x.file_date, self.data))

    def get_vectors(self, phrase: str | None = None) -> List[Vector]:
        """ Returns the vectors of given phrase """
        return self.data

    def insert_vectors(self, vectors: List[Vector], batch_size: int = 10000) -> None:
        """ Inserts the vectors into database """
        pass
