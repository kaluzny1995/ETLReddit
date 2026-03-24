from pydantic import BaseModel


class ReductionResult(BaseModel):
    pca2_0: float
    pca2_1: float
    pca3_0: float
    pca3_1: float
    pca3_2: float
    sne2_0: float
    sne2_1: float
    sne3_0: float
    sne3_1: float
    sne3_2: float

    class ConfigDict:
        frozen = True
