from pydantic import BaseModel


class EmotionResult(BaseModel):
    num_happy: float
    num_angry: float
    num_surprise: float
    num_sad: float
    num_fear: float
    total_words: float

    class ConfigDict:
        frozen = True
