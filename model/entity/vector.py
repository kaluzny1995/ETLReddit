import json
from typing import List
from sqlmodel import SQLModel, Field, Column, String

import error
from model import Reddit, Comment


class Vector(SQLModel, table=True):
    reddit_id: str | None = Field(sa_column=Column("reddit_id", String, primary_key=True, nullable=False))
    comment_id: str | None = Field(sa_column=Column("comment_id", String, primary_key=True, nullable=False))
    phrase: str = Field(sa_column=Column("phrase", String, primary_key=True, nullable=False))
    embeddings: str = Field(sa_column=Column("embeddings", String, nullable=False))
    file_date: str = Field(sa_column=Column("file_date", String, nullable=False))

    __tablename__ = "vectors"
    __table_args__ = (
        {'schema': "reddit"}
    )

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "reddit_id": "ekqlk6",
                "comment_id": "fdd5fo1",
                "phrase": "corgi",
                "embeddings": "[0.13623,0.64211,-0.23134,0.32411]",
                "file_date": "2020-01-01"
            }
        }

    @staticmethod
    def blank(phrase: str, file_date: str) -> 'Vector':
        return Vector(
            reddit_id=f"N/A_{file_date}",
            comment_id=f"N/A_{file_date}",
            phrase=phrase,
            embeddings=f"[{'0.,'*384}]",
            file_date=file_date
        )

    @staticmethod
    def from_reddit(reddit: Reddit, embeddings: List[float]) -> 'Vector':
        return Vector(
            reddit_id=reddit.reddit_id,
            comment_id="N/A",
            phrase=reddit.phrase,
            embeddings=json.dumps(embeddings),
            file_date=reddit.start_file_date
        )

    @staticmethod
    def from_comment(comment: Comment, embeddings: List[float]) -> 'Vector':
        return Vector(
            reddit_id="N/A",
            comment_id=comment.comment_id,
            phrase=comment.phrase,
            embeddings=json.dumps(embeddings),
            file_date=comment.start_file_date
        )

    @staticmethod
    def get_entry_texts(entries: List[Reddit | Comment]) -> List[str]:
        texts = list([])
        for entry in entries:
            if isinstance(entry, Reddit):
                texts.append(f"{entry.title} {entry.body}" if entry.body is not None else entry.title)
            elif isinstance(entry, Comment):
                texts.append(entry.body if entry.body is not None else "")
            else:
                raise error.WrongEntityError(f"Wrong entity type: {type(entry)}. Should be Reddit or Comment.")
        return texts
