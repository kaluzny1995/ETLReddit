import sqlalchemy
from sqlmodel import create_engine, Session, select, SQLModel
from typing import List

import util
from model import SupabaseConnectionConfig, SentimentAnalysis
from provider import ISentimentAnalysisProvider


class SupabasePostgresSentimentAnalysisProvider(ISentimentAnalysisProvider):
    """ Sentiment analyses provider from Postgres Supabase database """

    connection_string: str
    db_engine: sqlalchemy.engine.Engine

    def __init__(self, connection_string: str | None = None, db_engine: sqlalchemy.engine.Engine | None = None):
        super(SupabasePostgresSentimentAnalysisProvider, self).__init__()
        self.connection_string = connection_string or SupabaseConnectionConfig.get_db_connection_string()
        self.db_engine = db_engine or create_engine(self.connection_string)

    def _create_if_not_exists(self) -> None:
        """ Creates 'sentiment analyses' table if not exists """
        if not sqlalchemy.inspect(self.db_engine).has_table(table_name="sentiment_analyses", schema="reddit"):
            SQLModel.metadata.create_all(self.db_engine, tables=[SentimentAnalysis.__table__])

    def get_file_dates(self, phrase: str) -> List[str]:
        """ Returns the file dates of sentiment analysis of given phrase """
        self._create_if_not_exists()

        with Session(self.db_engine) as db_session:
            statement = select(SentimentAnalysis.file_date)
            statement = statement.where(SentimentAnalysis.phrase == phrase).distinct()
            file_dates = db_session.exec(statement).all()
        return list(file_dates)

    def get_sentiment_analyses(self, phrase: str) -> List[SentimentAnalysis]:
        """ Returns the sentiment analyses of given phrase """
        self._create_if_not_exists()

        with Session(self.db_engine) as db_session:
            statement = select(SentimentAnalysis).where(SentimentAnalysis.phrase == phrase)
            sentiment_analyses = db_session.exec(statement).all()
        sentiment_analyses = list(map(lambda p: p[0], sentiment_analyses))
        return sentiment_analyses

    def insert_sentiment_analyses(self, sentiment_analyses: List[SentimentAnalysis], batch_size: int = 100) -> None:
        """ Inserts the sentiment analyses into database """
        self._create_if_not_exists()

        sentiment_analysis_chunks = util.chunk_list_equal_size(sentiment_analyses, batch_size)
        with Session(self.db_engine) as db_session:
            num_inserted = 0
            print("Inserting sentiment analyses:")
            for chunk in sentiment_analysis_chunks:
                db_session.add_all(chunk)
                db_session.commit()
                num_inserted += len(chunk)
                print(f"{num_inserted} out of {len(sentiment_analyses)}")
            print("Sentiment analyses inserted.")

