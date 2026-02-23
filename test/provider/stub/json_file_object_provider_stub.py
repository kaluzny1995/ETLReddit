from typing import List, Dict, Any

import util
import error
from provider import IJsonFileObjectProvider


class JsonFileFileObjectProviderStub(IJsonFileObjectProvider):
    """ JsonFileObjectProvider interface """

    file_names: List[str]
    json_objects: List[List[Dict[str, Any] | List[Any]]]

    def __init__(self, file_names: List[str], json_objects: List[List[Dict[str, Any] | List[Any]]]) -> None:
        self.file_names = file_names
        self.json_objects = json_objects

    def get_file_names(self, file_dates: List[str] = None) -> List[str]:
        """ Returns the names of the files with the given file dates """
        if file_dates is not None:
            found_file_names = list(filter(lambda file_name: util.get_start_date_string_from_filename(file_name)
                                                             in file_dates, self.file_names))
        else:
            found_file_names = list([])
        if len(found_file_names) == 0:
            raise error.JsonFileNotFoundError("JSON files of given file dates not found.")

        return found_file_names

    def get_file_name(self, file_date: str) -> str:
        """ Returns the name of the file of given file date """
        found_file_names = list(filter(lambda fn: util.get_start_date_string_from_filename(fn) == file_date,
                                       self.file_names))
        if len(found_file_names) == 0:
            raise error.JsonFileNotFoundError("JSON file of given file date does not exist.")

        return found_file_names[0]

    def get_json_objects(self, file_dates: List[str]) -> List[List[Dict[str, Any] | List[Any]]]:
        """ Returns a list of JSON objects lists which creation dates match the provided file dates """
        found_file_names = self.get_file_names(file_dates)
        return list(map(lambda ffn: self.json_objects[self.file_names.index(ffn)], found_file_names))

    def get_json_object(self, file_date: str) -> List[Dict[str, Any]]:
        """ Returns a JSON object which creation dates match the provided file date """
        found_file_name = self.get_file_name(file_date)
        return self.json_objects[self.file_names.index(found_file_name)]
