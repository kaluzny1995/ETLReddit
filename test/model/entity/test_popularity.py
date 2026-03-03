import pytest

from model import Reddit, Comment, Popularity

from test.model.entity.fixtures_test_cases import (test_popularity_from_reddit_cases,
                                                   test_popularity_from_comment_cases)


@pytest.mark.parametrize("reddit, expected_popularity", test_popularity_from_reddit_cases)
def test_from_reddit(reddit: Reddit, expected_popularity: Popularity) -> None:
    # Arrange
    # Act
    popularity = Popularity.from_reddit(reddit)

    # Assert
    assert popularity.reddit_id == expected_popularity.reddit_id
    assert popularity.comment_id == expected_popularity.comment_id
    assert popularity.phrase == expected_popularity.phrase
    assert popularity.author == expected_popularity.author
    assert popularity.entry_type == expected_popularity.entry_type
    assert popularity.entry_level == expected_popularity.entry_level
    assert popularity.score == expected_popularity.score
    assert popularity.upvote_ratio == expected_popularity.upvote_ratio
    assert popularity.gilded_count == expected_popularity.gilded_count
    assert popularity.comments_count == expected_popularity.comments_count
    assert popularity.is_controversial == expected_popularity.is_controversial
    assert popularity.file_date == expected_popularity.file_date


@pytest.mark.parametrize("comment, expected_popularity", test_popularity_from_comment_cases)
def test_from_comment(comment: Comment, expected_popularity: Popularity) -> None:
    # Arrange
    # Act
    popularity = Popularity.from_comment(comment)

    # Assert
    assert popularity.reddit_id == expected_popularity.reddit_id
    assert popularity.comment_id == expected_popularity.comment_id
    assert popularity.phrase == expected_popularity.phrase
    assert popularity.author == expected_popularity.author
    assert popularity.entry_type == expected_popularity.entry_type
    assert popularity.entry_level == expected_popularity.entry_level
    assert popularity.score == expected_popularity.score
    assert popularity.upvote_ratio == expected_popularity.upvote_ratio
    assert popularity.gilded_count == expected_popularity.gilded_count
    assert popularity.comments_count == expected_popularity.comments_count
    assert popularity.is_controversial == expected_popularity.is_controversial
    assert popularity.file_date == expected_popularity.file_date
