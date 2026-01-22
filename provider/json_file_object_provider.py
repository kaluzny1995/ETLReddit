import os
import json
from typing import List, Dict, Any

from error import JsonFileNotFoundError
from util import get_start_date_string_from_filename


class JsonFileObjectProvider:
    """ Provides JSON objects (reddits, authors, etc.) from files """

    source_folder: str

    def __init__(self, source_folder):
        self.source_folder = source_folder

    def get_file_names(self, file_dates: List[str] = None) -> List[str]:
        """ Returns the names of the JSON files """
        file_names = os.listdir(self.source_folder)
        if file_dates is not None:
            file_names = list(filter(lambda file_name: get_start_date_string_from_filename(file_name) in file_dates, file_names))
        if len(file_names) == 0:
            raise JsonFileNotFoundError("JSON files of given file dates not found.")

        return file_names

    def get_file_name(self, file_date: str) -> str:
        """ Returns the name of the JSON file """
        file_names = list(filter(lambda fn: get_start_date_string_from_filename(fn) == file_date, os.listdir(self.source_folder)))
        if len(file_names) == 0:
            raise JsonFileNotFoundError("JSON file of given file date does not exist.")

        return file_names[0]

    def get_json_objects(self, file_dates: List[str]) -> List[List[Dict[str, Any] | List[Any]]]:
        """ Returns a list of JSON objects lists which creation dates match the provided dates """
        json_files = list(filter(lambda f: f.split("_")[-2] in file_dates, self.get_file_names()))
        json_objects = list([])
        for json_file in json_files:
            with open(os.path.join(self.source_folder, json_file), "r") as jf:
                json_objects.append(json.load(jf))

        return json_objects

    def get_json_object(self, file_date: str) -> Dict[str, Any]:
        """ Returns a JSON object which creation dates match the provided date """
        file_name = self.get_file_name(file_date)
        with open(os.path.join(self.source_folder, file_name), "r") as jf:
            return json.load(jf)
