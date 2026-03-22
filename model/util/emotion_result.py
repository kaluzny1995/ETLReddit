from typing import List
from pydantic import BaseModel

from model import EEmotionClass


class EmotionResult(BaseModel):
    num_happy: int
    num_angry: int
    num_surprise: int
    num_sad: int
    num_fear: int
    total_words: int
    emotion_classes: List[EEmotionClass]

    class ConfigDict:
        frozen = True
