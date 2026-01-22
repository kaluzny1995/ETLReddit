from typing import List, Dict, Any

from model import Comment
from provider import JsonFileObjectProvider

import util


class JsonCommentProvider:
    """ Provides comments data based on JSON objects """
    json_file_object_provider: JsonFileObjectProvider

    def __init__(self, json_file_object_provider: JsonFileObjectProvider):
        self.json_file_object_provider = json_file_object_provider

    def _get_comment_replies(self, comments_json: List[Dict[str, Any]], reddit_id: str, phrase: str,
                             star_file_date: str, end_file_date: str) -> List[Comment]:
        """ Returns a list of all levels comments replies """
        comments = list([])

        for comment_json in comments_json:
            comments.append(Comment.from_raw_json(comment_json, reddit_id, phrase, star_file_date, end_file_date))
            if comment_json.get("replies", None) is not None and len(comment_json["replies"]) > 0:
                comments.extend(self._get_comment_replies(comment_json["replies"], reddit_id, phrase,
                                                          star_file_date, end_file_date))

        return comments

    def get_comments(self, file_dates: List[str], phrase: str) -> List[Comment]:
        """ Returns a list of Comment objects """
        file_names = self.json_file_object_provider.get_file_names(file_dates)
        reddits_jsons = self.json_file_object_provider.get_json_objects(file_dates)
        comments = list([])

        for file_name, reddits_json in zip(file_names, reddits_jsons):
            start_file_date = util.get_start_date_string_from_filename(file_name)
            end_file_date = util.get_end_date_string_from_filename(file_name)

            for reddit_json in reddits_json:
                reddit_id = reddit_json['id']
                if reddit_json.get("comments", None) is not None and len(reddit_json["comments"]) > 0:
                    comments.extend(self._get_comment_replies(reddit_json["comments"], reddit_id, phrase,
                                                              start_file_date, end_file_date))

        return comments
