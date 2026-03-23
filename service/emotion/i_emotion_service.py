from abc import abstractmethod
from typing import List

from model import ETLParams, EmotionResult, Reddit, Comment, Emotion
from service import IETLService


class IEmotionService(IETLService):
    """ Emotion Service interface """

    def get_autocorrected_text(self, text: str | None) -> str | None:
        """ Returns the autocorrected text """
        pass

    def get_text2emotion(self, text: str | None) -> EmotionResult:
        """ Returns the emotion result from given text """
        pass

    @abstractmethod
    def get_emotions(self, entries: List[Reddit | Comment], params: ETLParams) -> List[Emotion]:
        """ Returns the processed emotions from given entries """
        pass
