from typing import List

from autocorrect import Speller

import text2emotion
from model import ETLParams, EEmotionClass, EmotionResult, Reddit, Comment, Emotion
from service import IEmotionService


class EmotionServiceStub(IEmotionService):
    """ Emotion service class """
    speller: Speller

    def __init__(self):

        self.speller = Speller()

    def get_autocorrected_text(self, text: str | None) -> str | None:
        """ Returns the autocorrected text """
        return None if text is None else self.speller(text)

    def get_text2emotion(self, text: str | None) -> EmotionResult:
        """ Returns the emotion result from given text """
        text2emotion_result, total_words = text2emotion.get_emotion(text)
        dominant_emotions = text2emotion.get_emotions(text2emotion_result, total_words)
        return EmotionResult(
            num_happy=text2emotion_result['Happy'],
            num_angry=text2emotion_result['Angry'],
            num_surprise=text2emotion_result['Surprise'],
            num_sad=text2emotion_result['Sad'],
            num_fear=text2emotion_result['Fear'],
            total_words=total_words,
            emotion_classes=list(map(lambda emotion: EEmotionClass(emotion.upper()), dominant_emotions)),
        )

    def get_emotions(self, entries: List[Reddit | Comment], params: ETLParams) -> List[Emotion]:
        """ Returns the processed emotions from given entries """
        pass

    def run_etl(self, **etl_params) -> None:
        """ Returns a list of emotion objects according to the provided reddits and comments """
        pass