from sqlmodel import SQLModel, Field, Column, String, Enum, Integer, Float, Boolean, CheckConstraint

from model import EEntryType, Reddit, Comment


class Popularity(SQLModel, table=True):
    reddit_id: str | None = Field(sa_column=Column("reddit_id", String, primary_key=True, nullable=False))
    comment_id: str | None = Field(sa_column=Column("comment_id", String, primary_key=True, nullable=False))
    phrase: str = Field(sa_column=Column("phrase", String, primary_key=True, nullable=False))
    author: str | None = Field(sa_column=Column("author", String, nullable=True))
    entry_type: EEntryType = Field(sa_column=Column("entry_type", Enum(EEntryType), nullable=False))
    entry_level: int = Field(sa_column=Column("entry_level", Integer, nullable=False))
    score: int = Field(sa_column=Column("score", Integer, nullable=False))
    upvote_ratio: float = Field(sa_column=Column("upvote_ratio", Float, nullable=False))
    gilded_count: int = Field(sa_column=Column("gilded_count", Integer, nullable=False))
    comments_count: int = Field(sa_column=Column("comments_count", Integer, nullable=False))
    is_controversial: bool = Field(sa_column=Column("is_controversial", Boolean, nullable=False))
    file_date: str = Field(sa_column=Column("file_date", String, nullable=False))

    __tablename__ = "popularities"
    __table_args__ = (
        CheckConstraint("reddit_id is not null or comment_id is not null", name="reddit_or_comment_not_null"),
        {'schema': "reddit"}
    )

    class Config:
        json_schema_extra = {
            "example": {
                "reddit_id": "ekqlk6",
                "comment_id": "fdd5fo1",
                "phrase": "corgi",
                "author": "goswamitulsidas",
                "entry_type": EEntryType.REDDIT,
                "entry_level": -1,
                "score": 23885,
                "upvote_ratio": 0.98,
                "gilded_count": 1,
                "comments_count": 209,
                "is_controversial": False,
                "file_date": "2026-01-01T00:00:00"
            }
        }

    @staticmethod
    def blank(phrase: str, file_date: str) -> 'Popularity':
        return Popularity(
            reddit_id=f"N/A_{file_date}",
            comment_id=f"N/A_{file_date}",
            phrase=phrase,
            author="N/A",
            entry_type=EEntryType.REDDIT,
            entry_level=-1,
            score=0,
            upvote_ratio=0.,
            gilded_count=0,
            comments_count=0,
            is_controversial=False,
            file_date=file_date
        )

    @staticmethod
    def from_reddit(reddit: Reddit) -> 'Popularity':
        return Popularity(
            reddit_id=reddit.reddit_id,
            comment_id="N/A",
            phrase=reddit.phrase,
            author=reddit.author,
            entry_type=EEntryType.REDDIT,
            entry_level=-1,
            score=reddit.score,
            upvote_ratio=reddit.upvote_ratio,
            gilded_count=reddit.gilded_number,
            comments_count=reddit.number_of_comments,
            is_controversial=False,
            file_date=reddit.start_file_date
        )

    @staticmethod
    def from_comment(comment: Comment) -> 'Popularity':
        return Popularity(
            reddit_id="N/A",
            comment_id=comment.comment_id,
            phrase=comment.phrase,
            author=comment.author,
            entry_type=EEntryType.COMMENT,
            entry_level=comment.depth_level,
            score=comment.score,
            upvote_ratio=comment.upvote_ratio,
            gilded_count=comment.gilded_number,
            comments_count=comment.number_of_replies,
            is_controversial=comment.controversiality,
            file_date=comment.start_file_date
        )
