from typing import List

from model import Popularity
from provider import IDbPopularityProvider


class SupabasePostgresPopularityProviderStub(IDbPopularityProvider):
    """ Popularities provider stub for testing """

    data: List[Popularity]

    def __init__(self, data: List[Popularity]):
        self.data = data

    def create_if_not_exists(self) -> None:
        """ Creates 'popularities' table if not exists """
        pass

    def get_file_dates(self, phrase: str) -> List[str]:
        """ Returns the file dates of popularity of given phrase """
        return list(map(lambda x: x.file_date, self.data))

    def get_popularities(self, phrase: str) -> List[Popularity]:
        """ Returns the popularities of given phrase """
        return self.data

    def insert_popularities(self, popularities: List[Popularity], batch_size: int = 10000) -> None:
        """ Inserts the popularities into database """
        pass
