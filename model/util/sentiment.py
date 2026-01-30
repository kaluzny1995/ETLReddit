from pydantic import BaseModel


class NLTKSentiment(BaseModel):
    negative: float = 0.
    neutral: float = 0.
    positive: float = 0.
    compound: float = 0.

    class Config:
        frozen = True


class TextblobSentiment(BaseModel):

    polarity: float = 0.
    subjectivity: float = 0.

    class Config:
        frozen = True


class Sentiment(NLTKSentiment, TextblobSentiment):

    class Config:
        frozen = True

    @staticmethod
    def from_ntlk_and_textblob(nltk_sentiment: NLTKSentiment, textblob_sentiment: TextblobSentiment) -> 'Sentiment':
        return Sentiment(**dict(nltk_sentiment.model_dump() | textblob_sentiment.model_dump()))

