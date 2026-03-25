from enum import Enum


class EETLScript(Enum):
    POPULARITY = "popularity"
    SENTIMENT = "sentiment"
    EMOTION = "emotion"
    VECTORIZATION = "vectorization"
    REDUCTION = "reduction"
