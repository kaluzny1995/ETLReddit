from sqlmodel import SQLModel, Field, Column, String, Enum, Float, CheckConstraint

from model import EEntryType, ESentimentClass, Reddit, Comment, SentimentResult


class Sentiment(SQLModel, table=True):
    reddit_id: str | None = Field(sa_column=Column("reddit_id", String, primary_key=True, nullable=False))
    comment_id: str | None = Field(sa_column=Column("comment_id", String, primary_key=True, nullable=False))
    phrase: str = Field(sa_column=Column("phrase", String, primary_key=True, nullable=False))
    author: str | None = Field(sa_column=Column("author", String, nullable=True))
    entry_type: EEntryType = Field(sa_column=Column("entry_type", Enum(EEntryType), nullable=False))
    clean_text: str | None = Field(sa_column=Column("clean_text", String, nullable=True))
    s_neg: float = Field(sa_column=Column("s_neg", Float, nullable=False))
    s_neu: float = Field(sa_column=Column("s_neu", Float, nullable=False))
    s_pos: float = Field(sa_column=Column("s_pos", Float, nullable=False))
    s_com: float = Field(sa_column=Column("s_com", Float, nullable=False))
    s_pol: float = Field(sa_column=Column("s_pol", Float, nullable=False))
    s_sub: float = Field(sa_column=Column("s_sub", Float, nullable=False))
    s_class: ESentimentClass = Field(sa_column=Column("s_class", Enum(ESentimentClass), nullable=False))
    file_date: str = Field(sa_column=Column("file_date", String, nullable=False))

    __tablename__ = "sentiments"
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
                "clean_text": "Woman discovers that the neighbor's corgi was sneaking onto her property at night to ride her pony",
                "s_neg": 0.,
                "s_neu": 0.572,
                "s_pos": 0.428,
                "s_com": 0.6696,
                "s_pol": 0.625,
                "s_sub": 0.6,
                "s_class": ESentimentClass.POSITIVE,
                "file_date": "2026-01-01T00:00:00"
            }
        }

    @staticmethod
    def blank(phrase: str, file_date: str) -> 'Sentiment':
        return Sentiment(
            reddit_id=f"N/A_{file_date}",
            comment_id=f"N/A_{file_date}",
            phrase=phrase,
            author="N/A",
            entry_type=EEntryType.REDDIT,
            clean_text="N/A",
            s_neg=0.,
            s_neu=0.,
            s_pos=0.,
            s_com=0.,
            s_pol=0.,
            s_sub=0.,
            s_class=ESentimentClass.NEUTRAL,
            file_date=file_date
        )

    @staticmethod
    def from_reddit(reddit: Reddit, clean_text: str, sentiment_result: SentimentResult) -> 'Sentiment':
        return Sentiment(
            reddit_id=reddit.reddit_id,
            comment_id="N/A",
            phrase=reddit.phrase,
            author=reddit.author,
            entry_type=EEntryType.REDDIT,
            clean_text=clean_text,
            s_neg=sentiment_result.negative,
            s_neu=sentiment_result.neutral,
            s_pos=sentiment_result.positive,
            s_com=sentiment_result.compound,
            s_pol=sentiment_result.polarity,
            s_sub=sentiment_result.subjectivity,
            s_class=sentiment_result.sentiment_class,
            file_date=reddit.start_file_date
        )

    @staticmethod
    def from_comment(comment: Comment, clean_text: str, sentiment_result: SentimentResult) -> 'Sentiment':
        return Sentiment(
            reddit_id="N/A",
            comment_id=comment.comment_id,
            phrase=comment.phrase,
            author=comment.author,
            entry_type=EEntryType.COMMENT,
            clean_text=clean_text,
            s_neg=sentiment_result.negative,
            s_neu=sentiment_result.neutral,
            s_pos=sentiment_result.positive,
            s_com=sentiment_result.compound,
            s_pol=sentiment_result.polarity,
            s_sub=sentiment_result.subjectivity,
            s_class=sentiment_result.sentiment_class,
            file_date=comment.start_file_date
        )
