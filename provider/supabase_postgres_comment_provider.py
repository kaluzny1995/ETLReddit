from sqlmodel import select
from typing import List

from model import EFileDateType, Comment
from provider import IDbProvider, IDbCommentProvider, SupabasePostgresProvider


class SupabasePostgresDbCommentProvider(IDbCommentProvider):
    """ Comments provider from Postgres Supabase database """

    supabase_postgres_provider: IDbProvider

    def __init__(self, supabase_postgres_provider: IDbProvider | None = None):
        super(SupabasePostgresDbCommentProvider, self).__init__()
        self.supabase_postgres_provider = supabase_postgres_provider or SupabasePostgresProvider()

    def create_if_not_exists(self) -> None:
        """ Creates 'comments' table if not exists """
        self.supabase_postgres_provider.create_table_if_not_exists(Comment, table="comments", schema="reddit")

    def get_comments(self, phrase: str, file_dates: List[str], which: EFileDateType = EFileDateType.START) -> List[Comment]:
        """ Returns the comments of given phrase for given list of file dates """
        self.create_if_not_exists()

        statement = select(Comment).where(Comment.phrase == phrase)
        statement = statement.where(Comment.start_file_date.in_(file_dates)) \
            if which == EFileDateType.START else statement.where(Comment.end_file_date.in_(file_dates))
        comments = self.supabase_postgres_provider.run_select_statement(statement)
        return list(comments)

    def insert_comments(self, comments: list[Comment], batch_size: int = 100) -> None:
        """ Inserts the comments into database """
        self.create_if_not_exists()
        self.supabase_postgres_provider.run_insert_statement(comments, batch_size, num_entities=len(comments), name="comments")
