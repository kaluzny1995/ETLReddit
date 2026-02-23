from typing import List

from model.entity.comment import Comment
from model.enum.e_file_date_type import EFileDateType
from provider import IDbCommentProvider


class SupabasePostgresCommentProviderStub(IDbCommentProvider):
    """ Comments provider stub for testing """

    data: List[Comment]

    def __init__(self, data: List[Comment]):
        self.data = data

    def create_if_not_exists(self) -> None:
        """ Creates 'comments' table if not exists """
        pass

    def get_comments(self, phrase: str, file_dates: List[str], which: EFileDateType = EFileDateType.START) -> List[Comment]:
        """ Returns the comments of given phrase for given list of file dates """
        return self.data

    def insert_comments(self, comments: List[Comment], batch_size: int = 10000) -> None:
        """ Inserts the comments into database """
        pass
