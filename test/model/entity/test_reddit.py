import pytest
from typing import Dict, Any

from model import Reddit

from test.model.entity.fixtures_test_cases import test_reddit_from_raw_json_cases


@pytest.mark.parametrize("json_object, phrase, start_file_date, end_file_date, expected_reddit", test_reddit_from_raw_json_cases)
def test_from_raw_json(json_object: Dict[str, Any], phrase: str, start_file_date: str, end_file_date: str, expected_reddit: Reddit) -> None:
    # Arrange
    # Act
    reddit = Reddit.from_raw_json(json_object, phrase, start_file_date, end_file_date)

    # Assert
    reddit.reddit_id = expected_reddit.reddit_id
    reddit.name = expected_reddit.name
    reddit.permalink = expected_reddit.permalink
    reddit.phrase = expected_reddit.phrase
    reddit.author = expected_reddit.author
    reddit.title = expected_reddit.title
    reddit.body = expected_reddit.body
    reddit.datetime_created = expected_reddit.datetime_created
    reddit.datetime_created_utc = expected_reddit.datetime_created_utc
    reddit.likes = expected_reddit.likes
    reddit.ups = expected_reddit.ups
    reddit.downs = expected_reddit.downs
    reddit.score = expected_reddit.score
    reddit.upvote_ratio = expected_reddit.upvote_ratio
    reddit.gilded_number = expected_reddit.gilded_number
    reddit.number_of_comments = expected_reddit.number_of_comments
    reddit.start_file_date = expected_reddit.start_file_date
    reddit.end_file_date = expected_reddit.end_file_date
