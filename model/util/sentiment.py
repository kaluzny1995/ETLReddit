from pydantic import BaseModel


class Sentiment(BaseModel):
    negative: float
    neutral: float
    positive: float
    compound: float
    polarity: float
    subjectivity: float

    class Config:
        frozen = True
