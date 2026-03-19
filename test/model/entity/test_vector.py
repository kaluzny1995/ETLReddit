import pytest
from typing import List

from model import Reddit, Comment, Vector

from test.model.entity.fixtures_test_cases import (test_vector_from_reddit_cases,
                                                   test_vector_from_comment_cases)


@pytest.mark.parametrize("reddit, embeddings, expected_vector", test_vector_from_reddit_cases)
def test_from_reddit(reddit: Reddit, embeddings: List[float], expected_vector: Vector) -> None:
    # Arrange
    # Act
    vector = Vector.from_reddit(reddit, embeddings)

    # Assert
    assert vector.reddit_id == expected_vector.reddit_id
    assert vector.comment_id == expected_vector.comment_id
    assert vector.phrase == expected_vector.phrase
    assert vector.embeddings == expected_vector.embeddings
    assert vector.file_date == expected_vector.file_date


@pytest.mark.parametrize("comment, embeddings, expected_vector", test_vector_from_comment_cases)
def test_from_comment(comment: Comment, embeddings: List[float], expected_vector: Vector) -> None:
    # Arrange
    # Act
    vector = Vector.from_comment(comment, embeddings)

    # Assert
    assert vector.reddit_id == expected_vector.reddit_id
    assert vector.comment_id == expected_vector.comment_id
    assert vector.phrase == expected_vector.phrase
    assert vector.embeddings == expected_vector.embeddings
    assert vector.file_date == expected_vector.file_date
