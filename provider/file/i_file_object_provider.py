from abc import ABC, abstractmethod
from typing import List


class IFileObjectProvider(ABC):
    """ FileObjectProvider interface (for JSON, CSV, etc. files) """

    @abstractmethod
    def get_file_names(self, file_dates: List[str] = None) -> List[str]:
        """ Returns the names of the files with the given file dates """
        pass

    @abstractmethod
    def get_file_name(self, file_date: str) -> str:
        """ Returns the name of the file of given file date """
        pass
