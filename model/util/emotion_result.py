from pydantic import BaseModel


class EmotionResult(BaseModel):
    num_happy: int
    num_angry: int
    num_surprise: int
    num_sad: int
    num_fear: int
    total_words: int

    class ConfigDict:
        frozen = True
