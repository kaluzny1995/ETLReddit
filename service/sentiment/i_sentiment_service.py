from abc import abstractmethod
from typing import List

from model import ETLParams, NLTKSentiment, TextblobSentiment, Reddit, Comment, Sentiment
from service import IETLService


class ISentimentService(IETLService):
    """ Sentiment service interface """

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

    @abstractmethod
    def get_sentiments(self, entries: List[Reddit | Comment], params: ETLParams) -> List[Sentiment]:
        """ Returns the processed sentiments from given entries """
        pass
