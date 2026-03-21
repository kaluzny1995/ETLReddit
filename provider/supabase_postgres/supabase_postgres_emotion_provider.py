from sqlmodel import select
from typing import List

from model import Emotion
from provider import IDbProvider, IDbEmotionProvider, SupabasePostgresProvider


class SupabasePostgresDbEmotionProvider(IDbEmotionProvider):
    """ Emotions provider from Postgres Supabase database """

    supabase_postgres_provider: IDbProvider

    def __init__(self, supabase_postgres_provider: IDbProvider | None = None):
        super(SupabasePostgresDbEmotionProvider, self).__init__()
        self.supabase_postgres_provider = supabase_postgres_provider or SupabasePostgresProvider()

    def create_if_not_exists(self) -> None:
        """ Creates 'emotions' table if not exists """
        self.supabase_postgres_provider.create_table_if_not_exists(Emotion, table="emotions", schema="reddit")

    def get_file_dates(self, phrase: str) -> List[str]:
        """ Returns the file dates of emotion of given phrase """
        self.create_if_not_exists()

        statement = select(Emotion.file_date).where(Emotion.phrase == phrase).distinct()
        file_dates = self.supabase_postgres_provider.run_select_statement(statement)
        return list(file_dates)

    def get_emotions(self, phrase: str) -> List[Emotion]:
        """ Returns the emotions of given phrase """
        self.create_if_not_exists()

        statement = select(Emotion).where(Emotion.phrase == phrase)
        emotions = self.supabase_postgres_provider.run_select_statement(statement)
        return emotions

    def insert_emotions(self, emotions: List[Emotion], batch_size: int = 100) -> None:
        """ Inserts the emotions into database """
        self.create_if_not_exists()
        self.supabase_postgres_provider.run_insert_statement(emotions, batch_size, num_entities=len(emotions), name="emotions")
