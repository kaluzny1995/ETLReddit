from typing import List

from model import Author
from provider import JsonFileObjectProvider


class JsonAuthorProvider:
    """ Provides authors data based on JSON objects """
    json_file_object_provider: JsonFileObjectProvider

    def __init__(self, json_file_object_provider: JsonFileObjectProvider):
        self.json_file_object_provider = json_file_object_provider

    def get_authors(self, file_dates: List[str]) -> List[Author]:
        """ Returns a list of Author objects """
        authors_jsons = self.json_file_object_provider.get_json_objects(file_dates)

        authors = list([])
        author_names = list([])
        for authors_json in authors_jsons:
            for author_json in authors_json:
                if len(author_json) > 0:
                    author = Author.from_raw_json(author_json[0])
                    if author.name not in author_names:
                        authors.append(author)
                        author_names.append(author.name)



        return authors
