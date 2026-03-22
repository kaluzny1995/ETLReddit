from enum import Enum


class EEmotionClass(str, Enum):
    HAPPY = "HAPPY"
    ANGRY = "ANGRY"
    SURPRISE = "SURPRISE"
    SAD = "SAD"
    FEAR = "FEAR"
