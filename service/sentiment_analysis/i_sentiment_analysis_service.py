from abc import abstractmethod

from model import NLTKSentiment, TextblobSentiment
from service import IETLService


class ISentimentAnalysisService(IETLService):
    """ SentimentAnalysis service interface """

    @abstractmethod
    def get_autocorrected_text(self, text: str | None) -> str | None:
        """ Returns the autocorrected text """
        pass

    @abstractmethod
    def get_nltk_sentiment(self, text: str | None) -> NLTKSentiment:
        """ Returns the NLTK sentiment """
        pass

    @abstractmethod
    def get_textblob_sentiment(self, text: str | None) -> TextblobSentiment:
        """ Returns the textblob sentiment """
        pass
