import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sqlmodel import SQLModel
from textblob import TextBlob
from autocorrect import Speller
from typing import List

from model.util.sentiment import TextblobSentiment, NLTKSentiment
from service import ISentimentAnalysisService


class SentimentAnalysisServiceStub(ISentimentAnalysisService):
    """ SentimentAnalysis service class """
    speller: Speller
    nltk_sentiment_analyzer: SentimentIntensityAnalyzer

    def __init__(self) -> None:
        nltk.download("vader_lexicon")

        self.speller = Speller()
        self.nltk_sentiment_analyzer = SentimentIntensityAnalyzer()

    def get_autocorrected_text(self, text: str | None) -> str | None:
        """ Returns the autocorrected text """
        return None if text is None else self.speller(text)

    def get_nltk_sentiment(self, text: str | None) -> NLTKSentiment:
        """ Returns the NLTK sentiment """
        if text is None:
            return NLTKSentiment()
        else:
            sentiments = self.nltk_sentiment_analyzer.polarity_scores(text)
            return NLTKSentiment(negative=sentiments['neg'], neutral=sentiments['neu'],
                                 positive=sentiments['pos'], compound=sentiments['compound'])

    def get_textblob_sentiment(self, text: str | None) -> TextblobSentiment:
        """ Returns the textblob sentiment """
        if text is None:
            return TextblobSentiment()
        else:
            sentiments = TextBlob(text).sentiment
            return TextblobSentiment(polarity=sentiments.polarity, subjectivity=sentiments.subjectivity)

    def run_etl(self, entries: List[SQLModel]) -> List[SQLModel]:
        """ Returns a list of sentiment analysis objects according to the provided reddits and comments """
        pass