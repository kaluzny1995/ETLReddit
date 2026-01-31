import datetime as dt
from typing import Dict, Any

from sqlmodel import SQLModel, Field, Column, Integer, String, DateTime, Float, Boolean, ForeignKeyConstraint

from model import Reddit


class Comment(SQLModel, table=True):
    comment_id: str = Field(sa_column=Column("comment_id", String, primary_key=True, nullable=False))
    phrase: str = Field(sa_column=Column("phrase", String, primary_key=True, nullable=False))
    reddit_id: str = Field(sa_column=Column("reddit_id", String, nullable=False))
    parent_comment_id: str | None = Field(sa_column=Column("parent_comment_id", String, nullable=True))
    name: str = Field(sa_column=Column("name", String, nullable=False))
    permalink: str = Field(sa_column=Column("permalink", String, nullable=False))
    author: str | None = Field(sa_column=Column("author", String, nullable=True))
    body: str | None = Field(sa_column=Column("body", String, nullable=True))
    datetime_created: dt.datetime = Field(sa_column=Column("datetime_created", DateTime, nullable=False))
    datetime_created_utc: dt.datetime = Field(sa_column=Column("datetime_created_utc", DateTime, nullable=False))
    depth_level: int = Field(sa_column=Column("depth_level", Integer, nullable=False))
    controversiality: bool = Field(sa_column=Column("controversiality", Boolean, nullable=False))
    likes: int = Field(sa_column=Column("likes", Integer, nullable=False))
    ups: int = Field(sa_column=Column("ups", Integer, nullable=False))
    downs: int = Field(sa_column=Column("downs", Integer, nullable=False))
    score: int = Field(sa_column=Column("score", Integer, nullable=False))
    upvote_ratio: float = Field(sa_column=Column("upvote_ratio", Float, nullable=False))
    gilded: bool = Field(sa_column=Column("gilded", Boolean, nullable=False))
    start_file_date: str = Field(sa_column=Column("start_file_date", String, nullable=False))
    end_file_date: str = Field(sa_column=Column("end_file_date", String, nullable=False))

    __tablename__ = "comments"
    __table_args__ = (
        ForeignKeyConstraint(["reddit_id", "phrase"], [Reddit.reddit_id, Reddit.phrase]),
        {'schema': "reddit"}
    )


    class Config:
        json_schema_extra = {
            "example": {
                "comment_id": "nyql127",
                "reddit_id": "1q8vj2v",
                "parent_comment_id": "t3_1q8vj2v",
                "name": "t1_nyql127",
                "permalink": "/r/Weird/comments/1q8vj2v/woman_discovers_that_the_neighbors_corgi_was/nyql127/",
                "phrase": "corgi",
                "author": "WestTransportation12",
                "body": "That is a symbiotic relationship if I have ever seen one.",
                "datetime_created": dt.datetime(2026, 1, 19, 17, 52 , 47),
                "datetime_created_utc": dt.datetime(2026, 1, 19, 17, 52 , 47),
                "depth_level": 0,
                "controversiality": False,
                "likes": 0,
                "ups": 1983,
                "downs": 0,
                "score": 1983,
                "upvote_ratio": 1.0,
                "gilded": False,
                "start_file_date": "2026-01-01T00:00:00",
                "start_end_date": "2027-01-01T00:00:00"
            }
        }

    @staticmethod
    def from_raw_json(json_object: Dict[str, Any], reddit_id: str, phrase: str,
                      start_file_date: str, end_file_date: str) -> 'Comment':
        return Comment(
            comment_id=json_object["id"],
            reddit_id=reddit_id,
            parent_comment_id=json_object["parent_id"].split("_")[-1] if json_object["depth_level"] > 0 else None,
            name=json_object["name"],
            permalink=json_object['permalink'],
            phrase=phrase,
            author=json_object['author'] if json_object['author'] != "[deleted]" else None,
            body=json_object['body'] if json_object['body'] not in ["", "[deleted]", "[removed]"] else None,
            datetime_created=dt.datetime.fromtimestamp(json_object['created']),
            datetime_created_utc=dt.datetime.fromtimestamp(json_object['created_utc']),
            depth_level=json_object['depth_level'],
            controversiality=bool(json_object['controversiality']),
            likes=json_object['likes'] if json_object['likes'] is not None else 0,
            ups=json_object['ups'],
            downs=json_object['downs'],
            score=json_object['score'],
            upvote_ratio=json_object['upvote_ratio'],
            gilded=bool(json_object['gilded']),
            start_file_date=start_file_date,
            end_file_date=end_file_date
        )
