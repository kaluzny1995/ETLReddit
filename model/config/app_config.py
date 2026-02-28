import json
from pydantic import BaseModel


class AppConfig(BaseModel):
    """ App settings config """
    batch_size: int
    is_no_authors_load: bool
    files_reddit_source_folder_pattern: str
    files_author_source_folder_pattern: str
    is_missing_dates_skipped: bool
    date_interval: str
    is_until_today: bool
    is_no_multiprocessing_used: bool
    num_processes: int

    class ConfigDict:
        frozen = True

    @staticmethod
    def from_json() -> 'AppConfig':
        with open("config.json", "r") as f:
            config = AppConfig(**json.load(f))
        return config
