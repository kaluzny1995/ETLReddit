import pytest

from model import EmotionResult, Reddit, Comment, Emotion

from test.model.entity.fixtures_test_cases import (test_emotion_from_reddit_cases,
                                                   test_emotion_from_comment_cases)


@pytest.mark.parametrize("reddit, emotion_result, expected_emotion", test_emotion_from_reddit_cases)
def test_from_reddit(reddit: Reddit, emotion_result: EmotionResult, expected_emotion: Emotion) -> None:
    # Arrange
    # Act
    emotion = Emotion.from_reddit(reddit, emotion_result)

    # Assert
    assert emotion.reddit_id == expected_emotion.reddit_id
    assert emotion.comment_id == expected_emotion.comment_id
    assert emotion.phrase == expected_emotion.phrase
    assert emotion.num_happy == expected_emotion.num_happy
    assert emotion.num_angry == expected_emotion.num_angry
    assert emotion.num_surprise == expected_emotion.num_surprise
    assert emotion.num_sad == expected_emotion.num_sad
    assert emotion.num_fear == expected_emotion.num_fear
    assert emotion.total_words == expected_emotion.total_words
    assert emotion.file_date == expected_emotion.file_date


@pytest.mark.parametrize("comment, emotion_result, expected_emotion", test_emotion_from_comment_cases)
def test_from_comment(comment: Comment, emotion_result: EmotionResult, expected_emotion: Emotion) -> None:
    # Arrange
    # Act
    emotion = Emotion.from_comment(comment, emotion_result)

    # Assert
    assert emotion.reddit_id == expected_emotion.reddit_id
    assert emotion.comment_id == expected_emotion.comment_id
    assert emotion.phrase == expected_emotion.phrase
    assert emotion.num_happy == expected_emotion.num_happy
    assert emotion.num_angry == expected_emotion.num_angry
    assert emotion.num_surprise == expected_emotion.num_surprise
    assert emotion.num_sad == expected_emotion.num_sad
    assert emotion.num_fear == expected_emotion.num_fear
    assert emotion.total_words == expected_emotion.total_words
    assert emotion.file_date == expected_emotion.file_date
