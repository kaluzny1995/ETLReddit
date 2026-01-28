from pydantic import BaseModel


class NLTKSentiment(BaseModel):
    negative: float
    neutral: float
    positive: float
    compound: float

    class Config:
        frozen = True


class TextblobSentiment(BaseModel):

    polarity: float
    subjectivity: float

    class Config:
        frozen = True


class Sentiment(NLTKSentiment, TextblobSentiment):

    class Config:
        frozen = True

    @staticmethod
    def from_ntlk_and_textblob(nltk_sentiment: NLTKSentiment, textblob_sentiment: TextblobSentiment) -> 'Sentiment':
        return Sentiment(**dict(nltk_sentiment.model_dump() | textblob_sentiment.model_dump()))

