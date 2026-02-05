from abc import abstractmethod
from typing import List, Dict, Any

from provider import IFileObjectProvider


class IJsonFileObjectProvider(IFileObjectProvider):
    """ JsonFileObjectProvider interface """

    @abstractmethod
    def get_json_objects(self, file_dates: List[str]) -> List[List[Dict[str, Any] | List[Any]]]:
        """ Returns a list of JSON objects lists which creation dates match the provided file dates """
        pass

    @abstractmethod
    def get_json_object(self, file_date: str) -> Dict[str, Any]:
        """ Returns a JSON object which creation dates match the provided file date """
        pass
