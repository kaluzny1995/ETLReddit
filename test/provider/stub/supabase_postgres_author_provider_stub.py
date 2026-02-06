from typing import List

from model.entity.author import Author
from provider import IDbAuthorProvider


class SupabasePostgresDbAuthorProviderStub(IDbAuthorProvider):
    """ Authors provider stub for testing """

    data: List[Author]

    def __init__(self, data: List[Author]):
        self.data = data

    def create_if_not_exists(self) -> None:
        """ Creates 'authors' table if not exists """
        pass

    def get_names(self) -> List[str]:
        """ Return a list of authors names """
        return list(set(map(lambda x: x.name, self.data)))

    def insert_authors(self, authors: List[Author], batch_size: int = 10000) -> None:
        """ Inserts the authors into database """
        pass
