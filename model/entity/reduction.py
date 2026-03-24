import json
from typing import List
from sqlmodel import SQLModel, Field, Column, String, Float

import error
from model import ReductionResult, Vector


class Reduction(SQLModel, table=True):
    reddit_id: str | None = Field(sa_column=Column("reddit_id", String, primary_key=True, nullable=False))
    comment_id: str | None = Field(sa_column=Column("comment_id", String, primary_key=True, nullable=False))
    phrase: str = Field(sa_column=Column("phrase", String, primary_key=True, nullable=False))
    pca2_0: float = Field(sa_column=Column("pca2_0", Float, nullable=False))
    pca2_1: float = Field(sa_column=Column("pca2_1", Float, nullable=False))
    pca3_0: float = Field(sa_column=Column("pca3_0", Float, nullable=False))
    pca3_1: float = Field(sa_column=Column("pca3_1", Float, nullable=False))
    pca3_2: float = Field(sa_column=Column("pca3_2", Float, nullable=False))
    sne2_0: float = Field(sa_column=Column("sne2_0", Float, nullable=False))
    sne2_1: float = Field(sa_column=Column("sne2_1", Float, nullable=False))
    sne3_0: float = Field(sa_column=Column("sne3_0", Float, nullable=False))
    sne3_1: float = Field(sa_column=Column("sne3_1", Float, nullable=False))
    sne3_2: float = Field(sa_column=Column("sne3_2", Float, nullable=False))
    file_date: str = Field(sa_column=Column("file_date", String, nullable=False))

    __tablename__ = "reduction"
    __table_args__ = (
        {'schema': "reddit"}
    )

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "reddit_id": "ekqlk6",
                "comment_id": "fdd5fo1",
                "phrase": "corgi",
                "pca2_0": 0.13623,
                "pca2_1": -0.31832,
                "pca3_0": 0.64211,
                "pca3_1": -0.87232,
                "pca3_2": 0.32411,
                "sne2_0": 0.43398,
                "sne2_1": -0.21388,
                "sne3_0": 0.32411,
                "sne3_1": -0.47382,
                "sne3_2": -0.03923,
                "file_date": "2020-01-01"
            }
        }

    @staticmethod
    def blank(phrase: str, file_date: str) -> 'Reduction':
        return Reduction(
            reddit_id=f"N/A_{file_date}",
            comment_id=f"N/A_{file_date}",
            phrase=phrase,
            pca2_0=0.,
            pca2_1=0.,
            pca3_0=0.,
            pca3_1=0.,
            pca3_2=0.,
            sne2_0=0.,
            sne2_1=0.,
            sne3_0=0.,
            sne3_1=0.,
            sne3_2=0.,
            file_date=file_date
        )

    @staticmethod
    def from_vector(vector: Vector, reduction_result: ReductionResult) -> 'Reduction':
        return Reduction(
            reddit_id=vector.reddit_id,
            comment_id=vector.comment_id,
            phrase=vector.phrase,
            pca2_0=reduction_result.pca2_0,
            pca2_1=reduction_result.pca2_1,
            pca3_0=reduction_result.pca3_0,
            pca3_1=reduction_result.pca3_1,
            pca3_2=reduction_result.pca3_2,
            sne2_0=reduction_result.sne2_0,
            sne2_1=reduction_result.sne2_1,
            sne3_0=reduction_result.sne3_0,
            sne3_1=reduction_result.sne3_1,
            sne3_2=reduction_result.sne3_2,
            file_date=vector.file_date
        )
