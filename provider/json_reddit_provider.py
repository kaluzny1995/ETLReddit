from typing import List

from model import Reddit
from provider import IJsonFileObjectProvider, IFileRedditProvider

import util


class JsonRedditProvider(IFileRedditProvider):
    """ Provides reddits data based on JSON objects """

    json_file_object_provider: IJsonFileObjectProvider

    def __init__(self, json_file_object_provider: IJsonFileObjectProvider):
        self.json_file_object_provider = json_file_object_provider

    def get_reddits(self, file_dates: List[str], phrase: str) -> List[Reddit]:
        """ Returns a list of Reddit objects """
        file_names = self.json_file_object_provider.get_file_names(file_dates)
        reddits_jsons = self.json_file_object_provider.get_json_objects(file_dates)
        reddits = list([])

        for file_name, reddits_json in zip(file_names, reddits_jsons):
            start_file_date = util.get_start_date_string_from_filename(file_name)
            end_file_date = util.get_end_date_string_from_filename(file_name)
            reddits.extend(list(map(lambda rj: Reddit.from_raw_json(rj, phrase, start_file_date, end_file_date), reddits_json)))

        return reddits