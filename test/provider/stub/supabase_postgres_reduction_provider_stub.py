from typing import List

from model import Reduction
from provider import IDbReductionProvider


class SupabasePostgresReductionProviderStub(IDbReductionProvider):
    """ Reductions provider stub for testing """

    data: List[Reduction]

    def __init__(self, data: List[Reduction]):
        self.data = data

    def create_if_not_exists(self) -> None:
        """ Creates 'reductions' table if not exists """
        pass

    def get_file_dates(self, phrase: str) -> List[str]:
        """ Returns the file dates of reduction of given phrase """
        return list(map(lambda x: x.file_date, self.data))

    def get_reductions(self, phrase: str) -> List[Reduction]:
        """ Returns the reductions of given phrase """
        return self.data

    def insert_reductions(self, reductions: List[Reduction], batch_size: int = 10000) -> None:
        """ Inserts the reductions into database """
        pass
