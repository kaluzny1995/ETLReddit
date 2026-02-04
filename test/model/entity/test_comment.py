import pytest
from typing import Dict, Any

from model import Comment

from test.model.entity.fixtures_test_cases import test_comment_from_raw_json_cases


@pytest.mark.parametrize("json_object, reddit_id, phrase, start_file_date, end_file_date, expected_comment", test_comment_from_raw_json_cases)
def test_from_raw_json(json_object: Dict[str, Any], reddit_id: str, phrase: str, start_file_date: str, end_file_date: str, expected_comment: Comment) -> None:
    # Arrange
    # Act
    comment = Comment.from_raw_json(json_object, reddit_id, phrase, start_file_date, end_file_date)

    # Assert
    assert comment.comment_id == expected_comment.comment_id
    assert comment.reddit_id == expected_comment.reddit_id
    assert comment.parent_comment_id == expected_comment.parent_comment_id
    assert comment.name == expected_comment.name
    assert comment.permalink == expected_comment.permalink
    assert comment.phrase == expected_comment.phrase
    assert comment.author == expected_comment.author
    assert comment.body == expected_comment.body
    assert comment.datetime_created == expected_comment.datetime_created
    assert comment.datetime_created_utc == expected_comment.datetime_created_utc
    assert comment.depth_level == expected_comment.depth_level
    assert comment.controversiality == expected_comment.controversiality
    assert comment.likes == expected_comment.likes
    assert comment.ups == expected_comment.ups
    assert comment.downs == expected_comment.downs
    assert comment.score == expected_comment.score
    assert comment.upvote_ratio == expected_comment.upvote_ratio
    assert comment.gilded_number == expected_comment.gilded_number
    assert comment.number_of_replies == expected_comment.number_of_replies
    assert comment.start_file_date == expected_comment.start_file_date
    assert comment.end_file_date == expected_comment.end_file_date
