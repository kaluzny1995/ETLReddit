import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from autocorrect import Speller

from model import NLTKSentiment, TextblobSentiment
from service import IAnalysisService


class AnalysisService(IAnalysisService):
    """ Analysis service class """
    speller: Speller
    nltk_sentiment_analyzer: SentimentIntensityAnalyzer

    def __init__(self):
        nltk.download("vader_lexicon")

        self.speller = Speller()
        self.nltk_sentiment_analyzer = SentimentIntensityAnalyzer()

    def get_autocorrected_text(self, text: str) -> str:
        """ Returns the autocorrected text """
        return self.speller(text)

    def get_nltk_setiment(self, text: str) -> NLTKSentiment:
        """ Returns the NLTK sentiment """
        sentiments = self.nltk_sentiment_analyzer.polarity_scores(text)
        return NLTKSentiment(negative=sentiments['neg'], neutral=sentiments['neu'],
                             positive=sentiments['pos'], compound=sentiments['compound'])

    def get_textblob_setiment(self, text: str) -> TextblobSentiment:
        """ Returns the textblob sentiment """
        sentiments = TextBlob(text).sentiment
        return TextblobSentiment(polarity=sentiments.polarity, subjectivity=sentiments.subjectivity)
