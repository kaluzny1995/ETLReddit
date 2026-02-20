import json
from pydantic import BaseModel


class AppConfig(BaseModel):
    """ App settings config """
    batch_size: int
    is_author_loaded: bool
    files_reddit_source_folder_pattern: str
    files_author_source_folder_pattern: str
    is_multiprocessing_used: bool
    num_processes: int

    class ConfigDict:
        frozen = True

    @staticmethod
    def from_json() -> 'AppConfig':
        with open("config.json", "r") as f:
            config = AppConfig(**json.load(f))
        return config
