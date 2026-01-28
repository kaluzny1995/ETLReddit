from abc import ABC, abstractmethod

from model import NLTKSentiment, TextblobSentiment


class IAnalysisService(ABC):
    """ Analysis service interface """

    @abstractmethod
    def get_autocorrected_text(self, text: str) -> str:
        """ Returns the autocorrected text """
        pass

    @abstractmethod
    def get_nltk_setiment(self, text: str) -> NLTKSentiment:
        """ Returns the NLTK sentiment """
        pass

    @abstractmethod
    def get_textblob_setiment(self, text: str) -> TextblobSentiment:
        """ Returns the textblob sentiment """
        pass
