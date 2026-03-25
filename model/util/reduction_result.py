from pydantic import BaseModel


class ReductionResult(BaseModel):
    pca2_0: float
    pca2_1: float
    pca3_0: float
    pca3_1: float
    pca3_2: float
    iso2_0: float
    iso2_1: float
    iso3_0: float
    iso3_1: float
    iso3_2: float

    class ConfigDict:
        frozen = True
