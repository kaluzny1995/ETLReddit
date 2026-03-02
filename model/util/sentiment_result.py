from pydantic import BaseModel

from model import ESentimentClass


class NLTKSentiment(BaseModel):
    negative: float = 0.
    neutral: float = 0.
    positive: float = 0.
    compound: float = 0.

    class ConfigDict:
        frozen = True


class TextblobSentiment(BaseModel):

    polarity: float = 0.
    subjectivity: float = 0.

    class ConfigDict:
        frozen = True


class SentimentResult(NLTKSentiment, TextblobSentiment):
    sentiment_class: ESentimentClass

    class ConfigDict:
        frozen = True

    @staticmethod
    def from_ntlk_and_textblob(nltk_sentiment: NLTKSentiment, textblob_sentiment: TextblobSentiment) -> 'SentimentResult':
        sentiment_class = ESentimentClass.NEGATIVE if -1. <= nltk_sentiment.compound < -0.33 \
            else ESentimentClass.POSITIVE if 0.33 < nltk_sentiment.compound <= 1. else ESentimentClass.NEUTRAL
        sentiment_dict = dict(nltk_sentiment.model_dump() | textblob_sentiment.model_dump() | dict(sentiment_class=sentiment_class))
        return SentimentResult(**sentiment_dict)

