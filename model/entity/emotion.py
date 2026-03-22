import json
from sqlmodel import SQLModel, Field, Column, String, Integer

from model import Reddit, Comment, EmotionResult


class Emotion(SQLModel, table=True):
    reddit_id: str | None = Field(sa_column=Column("reddit_id", String, primary_key=True, nullable=False))
    comment_id: str | None = Field(sa_column=Column("comment_id", String, primary_key=True, nullable=False))
    phrase: str = Field(sa_column=Column("phrase", String, primary_key=True, nullable=False))
    num_happy: int = Field(sa_column=Column("num_happy", Integer, nullable=False))
    num_angry: int = Field(sa_column=Column("num_angry", Integer, nullable=False))
    num_surprise: int = Field(sa_column=Column("num_surprise", Integer, nullable=False))
    num_sad: int = Field(sa_column=Column("num_sad", Integer, nullable=False))
    num_fear: int = Field(sa_column=Column("num_fear", Integer, nullable=False))
    total_words: int = Field(sa_column=Column("total_words", Integer, nullable=False))
    emotion_classes: str = Field(sa_column=Column("emotion_classes", String, nullable=False))
    file_date: str = Field(sa_column=Column("file_date", String, nullable=False))

    __tablename__ = "emotions"
    __table_args__ = (
        {'schema': "reddit"}
    )

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "reddit_id": "ekqlk6",
                "comment_id": "fdd5fo1",
                "phrase": "corgi",
                "num_happy": 4,
                "num_angry": 0,
                "num_surprise": 1,
                "num_sad": 3,
                "num_fear": 0,
                "total_words": 10,
                "emotion_classes": "[HAPPY, SAD]",
                "file_date": "2020-01-01"
            }
        }

    @staticmethod
    def blank(phrase: str, file_date: str) -> 'Emotion':
        return Emotion(
            reddit_id=f"N/A_{file_date}",
            comment_id=f"N/A_{file_date}",
            phrase=phrase,
            num_happy=0,
            num_angry=0,
            num_surprise=0,
            num_sad=0,
            num_fear=0,
            total_words=0,
            emotion_classes="[]",
            file_date=file_date
        )

    @staticmethod
    def from_reddit(reddit: Reddit, emotion_result: EmotionResult) -> 'Emotion':
        return Emotion(
            reddit_id=reddit.reddit_id,
            comment_id="N/A",
            phrase=reddit.phrase,
            num_happy=emotion_result.num_happy,
            num_angry=emotion_result.num_angry,
            num_surprise=emotion_result.num_surprise,
            num_sad=emotion_result.num_sad,
            num_fear=emotion_result.num_fear,
            total_words=emotion_result.total_words,
            emotion_classes=json.dumps(emotion_result.emotion_classes),
            file_date=reddit.start_file_date
        )

    @staticmethod
    def from_comment(comment: Comment, emotion_result: EmotionResult) -> 'Emotion':
        return Emotion(
            reddit_id="N/A",
            comment_id=comment.comment_id,
            phrase=comment.phrase,
            num_happy=emotion_result.num_happy,
            num_angry=emotion_result.num_angry,
            num_surprise=emotion_result.num_surprise,
            num_sad=emotion_result.num_sad,
            num_fear=emotion_result.num_fear,
            total_words=emotion_result.total_words,
            emotion_classes=json.dumps(emotion_result.emotion_classes),
            file_date=comment.start_file_date
        )
