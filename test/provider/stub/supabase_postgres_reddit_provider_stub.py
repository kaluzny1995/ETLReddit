from typing import List

from model.entity.reddit import Reddit
from model.enum.e_file_date_type import EFileDateType
from provider import IDbRedditProvider


class SupabasePostgresRedditProviderStub(IDbRedditProvider):
    """ Reddits provider stub for testing """

    data: List[Reddit]

    def __init__(self, data: List[Reddit]):
        self.data = data

    def create_if_not_exists(self) -> None:
        """ Creates 'reddits' table if not exists """
        pass

    def get_file_dates(self, phrase: str, which: EFileDateType = EFileDateType.START) -> List[str]:
        """ Returns the file dates of reddits of given phrase """
        return list(map(lambda x: x.start_file_date if which == EFileDateType.START else x.end_file_date, self.data))

    def get_reddits(self, phrase: str, file_dates: List[str], which: EFileDateType = EFileDateType.START) -> List[Reddit]:
        """ Returns the reddits of given phrase for given list of file dates """
        return self.data

    def insert_reddits(self, reddits: List[Reddit], batch_size: int = 10000) -> None:
        """ Inserts the reddits into database """
        pass
