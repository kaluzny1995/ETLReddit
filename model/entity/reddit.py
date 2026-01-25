import datetime as dt
from typing import Dict, Any

from sqlmodel import SQLModel, Field, Column, Integer, String, DateTime, Float, Boolean


class Reddit(SQLModel, table=True):
    reddit_id: str = Field(sa_column=Column("reddit_id", String, primary_key=True, nullable=False))
    phrase: str = Field(sa_column=Column("phrase", String, primary_key=True, nullable=False))
    name: str = Field(sa_column=Column("name", String, nullable=False))
    permalink: str = Field(sa_column=Column("permalink", String, nullable=False))
    author: str | None = Field(sa_column=Column("author", String, nullable=True))
    title: str = Field(sa_column=Column("title", String, nullable=False))
    body: str | None = Field(sa_column=Column("body", String, nullable=True))
    datetime_created: dt.datetime = Field(sa_column=Column("datetime_created", DateTime, nullable=False))
    datetime_created_utc: dt.datetime = Field(sa_column=Column("datetime_created_utc", DateTime, nullable=False))
    likes: int = Field(sa_column=Column("likes", Integer, nullable=False))
    ups: int = Field(sa_column=Column("ups", Integer, nullable=False))
    downs: int = Field(sa_column=Column("downs", Integer, nullable=False))
    score: int = Field(sa_column=Column("score", Integer, nullable=False))
    upvote_ratio: float = Field(sa_column=Column("upvote_ratio", Float, nullable=False))
    gilded: bool = Field(sa_column=Column("gilded", Boolean, nullable=False))
    number_of_comments: int = Field(sa_column=Column("number_of_comments", Integer, nullable=False))
    start_file_date: str = Field(sa_column=Column("start_file_date", String, nullable=False))
    end_file_date: str = Field(sa_column=Column("end_file_date", String, nullable=False))

    __tablename__ = "reddits"
    __table_args__ = {'schema': "reddit"}


    class Config:
        json_schema_extra = {
            "example": {
                "reddit_id": "1q8vj2v",
                "name": "t3_1q8vj2v",
                "permalink": "/r/Weird/comments/1q8vj2v/woman_discovers_that_the_neighbors_corgi_was/",
                "phrase": "corgi",
                "author": "goswamitulsidas",
                "title": "Woman discovers that the neighbor's corgi was sneaking onto her property at night to ride her pony",
                "body": "",
                "datetime_created": dt.datetime(2026, 1, 19, 17, 12 , 56),
                "datetime_created_utc": dt.datetime(2026, 1, 19, 17, 12 , 56),
                "likes": 0,
                "ups": 23885,
                "downs": 0,
                "score": 23885,
                "upvote_ratio": 0.98,
                "gilded": False,
                "number_of_comments": 209,
                "start_file_date": "2026-01-01T00:00:00",
                "start_end_date": "2027-01-01T00:00:00"
            }
        }

    @staticmethod
    def from_raw_json(json_object: Dict[str, Any], phrase: str,
                      start_file_date: str, end_file_date: str) -> 'Reddit':
        return Reddit(
            reddit_id=json_object['id'],
            name=json_object['name'],
            permalink=json_object['permalink'],
            phrase=phrase,
            author=json_object['author'] if json_object['author'] != "[deleted]" else None,
            title=json_object['title'],
            body=json_object['body'] if json_object['body'] != "" else None,
            datetime_created=dt.datetime.fromtimestamp(json_object['created']),
            datetime_created_utc=dt.datetime.fromtimestamp(json_object['created_utc']),
            likes=json_object['likes'] if json_object['likes'] is not None else 0,
            ups=json_object['ups'],
            downs=json_object['downs'],
            score=json_object['score'],
            upvote_ratio=json_object['upvote_ratio'],
            gilded=bool(json_object['gilded']),
            number_of_comments=json_object['num_comments'],
            start_file_date=start_file_date,
            end_file_date=end_file_date
        )
