import sqlalchemy
from sqlmodel import create_engine, Session, select, SQLModel
from typing import List

import util
from model import SupabaseConnectionConfig, Analysis
from provider import IAnalysisProvider


class SupabasePostgresAnalysisProvider(IAnalysisProvider):
    """ Analyses provider from Postgres Supabase database """

    connection_string: str
    db_engine: sqlalchemy.engine.Engine

    def __init__(self, connection_string: str | None = None, db_engine: sqlalchemy.engine.Engine | None = None):
        super(SupabasePostgresAnalysisProvider, self).__init__()
        self.connection_string = connection_string or SupabaseConnectionConfig.get_db_connection_string()
        self.db_engine = db_engine or create_engine(self.connection_string)

    def _create_if_not_exists(self) -> None:
        """ Creates 'analyses' database if not exists """
        if not sqlalchemy.inspect(self.db_engine).has_table(table_name="analyses", schema="reddit"):
            SQLModel.metadata.create_all(self.db_engine, tables=[Analysis.__table__])

    def get_file_dates(self, phrase: str) -> List[str]:
        """ Returns the file dates of analysis of given phrase """
        self._create_if_not_exists()

        with Session(self.db_engine) as db_session:
            statement = select(Analysis.file_date)
            statement = statement.where(Analysis.phrase == phrase).distinct()
            file_dates = db_session.exec(statement).all()
        return list(file_dates)

    def get_analyses(self, phrase: str) -> List[Analysis]:
        """ Returns the analyses of given phrase """
        self._create_if_not_exists()

        with Session(self.db_engine) as db_session:
            statement = select(Analysis).where(Analysis.phrase == phrase)
            analyses = db_session.exec(statement).all()
        analyses = list(map(lambda p: p[0], analyses))
        return analyses

    def insert_analyses(self, analyses: List[Analysis], batch_size: int = 100) -> None:
        """ Inserts the analyses into database """
        self._create_if_not_exists()

        analysis_chunks = util.chunk_list_equal_size(analyses, batch_size)
        with Session(self.db_engine) as db_session:
            num_inserted = 0
            print("Inserting analyses:")
            for chunk in analysis_chunks:
                db_session.add_all(chunk)
                db_session.commit()
                num_inserted += len(chunk)
                print(f"{num_inserted} out of {len(analyses)}")
            print("Analyses inserted.")

