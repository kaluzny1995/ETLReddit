import datetime as dt

from sqlmodel import SQLModel, Field, Column, String, DateTime, Integer, Float, Boolean, \
    UniqueConstraint, CheckConstraint

from model import Reddit, Comment, Sentiment


class Analysis(SQLModel, table=True):
    reddit_id: str | None = Field(sa_column=Column("reddit_id", String, primary_key=True, nullable=False))
    comment_id: str | None = Field(sa_column=Column("comment_id", String, primary_key=True, nullable=False))
    phrase: str = Field(sa_column=Column("phrase", String, primary_key=True, nullable=False))
    author: str | None = Field(sa_column=Column("author", String, nullable=True))
    text: str | None = Field(sa_column=Column("text", String, nullable=True))
    datetime_created: dt.datetime = Field(sa_column=Column("datetime_created", DateTime, nullable=False))
    score: int = Field(sa_column=Column("score", Integer, nullable=False))
    upvote_ratio: float = Field(sa_column=Column("upvote_ratio", Float, nullable=False))
    gilded: bool = Field(sa_column=Column("gilded", Boolean, nullable=False))
    number_of_comments: int | None = Field(sa_column=Column("number_of_comments", Integer, nullable=True))
    controversiality: bool = Field(sa_column=Column("controversiality", Boolean, nullable=False))
    s_neg: float = Field(sa_column=Column("s_neg", Float, nullable=False))
    s_neu: float = Field(sa_column=Column("s_neu", Float, nullable=False))
    s_pos: float = Field(sa_column=Column("s_pos", Float, nullable=False))
    s_com: float = Field(sa_column=Column("s_com", Float, nullable=False))
    s_pol: float = Field(sa_column=Column("s_pol", Float, nullable=False))
    s_sub: float = Field(sa_column=Column("s_sub", Float, nullable=False))
    file_date: str = Field(sa_column=Column("file_date", String, nullable=False))

    __tablename__ = "analyses"
    __table_args__ = (
        UniqueConstraint("reddit_id", "comment_id", "phrase", name="unique_reddit_comment_phrase"),
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
                "text": "Woman discovers that the neighbor's corgi was sneaking onto her property at night to ride her pony",
                "datetime_created": dt.datetime(2026, 1, 19, 17, 12 , 56),
                "score": 23885,
                "upvote_ratio": 0.98,
                "gilded": False,
                "number_of_comments": 209,
                "controversiality": False,
                "s_neg": 0.,
                "s_neu": 0.572,
                "s_pos": 0.428,
                "s_com": 0.6696,
                "s_pol": 0.625,
                "s_sub": 0.6,
                "file_date": "2026-01-01T00:00:00"
            }
        }

    @staticmethod
    def from_reddit(reddit: Reddit, text: str, sentiment: Sentiment) -> 'Analysis':
        return Analysis(
            reddit_id=reddit.reddit_id,
            comment_id="N/A",
            phrase=reddit.phrase,
            author=reddit.author,
            text=text,
            datetime_created=reddit.datetime_created_utc,
            score=reddit.score,
            upvote_ratio=reddit.upvote_ratio,
            gilded=reddit.gilded,
            number_of_comments=reddit.number_of_comments,
            controversiality=False,
            s_neg=sentiment.negative,
            s_neu=sentiment.neutral,
            s_pos=sentiment.positive,
            s_com=sentiment.compound,
            s_pol=sentiment.polarity,
            s_sub=sentiment.subjectivity,
            file_date=reddit.start_file_date
        )

    @staticmethod
    def from_comment(comment: Comment, text: str, sentiment: Sentiment) -> 'Analysis':
        return Analysis(
            reddit_id="N/A",
            comment_id=comment.comment_id,
            phrase=comment.phrase,
            author=comment.author,
            text=text,
            datetime_created=comment.datetime_created_utc,
            score=comment.score,
            upvote_ratio=comment.upvote_ratio,
            gilded=comment.gilded,
            number_of_comments=None,
            controversiality=comment.controversiality,
            s_neg=sentiment.negative,
            s_neu=sentiment.neutral,
            s_pos=sentiment.positive,
            s_com=sentiment.compound,
            s_pol=sentiment.polarity,
            s_sub=sentiment.subjectivity,
            file_date=comment.start_file_date
        )
