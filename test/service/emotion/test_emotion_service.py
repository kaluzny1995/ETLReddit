import pytest

from model import EmotionResult

from test.service.stub.emotion_service_stub import EmotionServiceStub
from test.service.emotion.fixtures_test_cases import (
    test_emotion_service_get_autocorrected_text_cases,
    test_emotion_service_get_text2emotion_text_cases
)


@pytest.mark.parametrize("text, expected_autocorrected_text", test_emotion_service_get_autocorrected_text_cases)
def test_get_autocorrected_text(text: str | None, expected_autocorrected_text: str | None) -> None:
    # Arrange
    emotion_service = EmotionServiceStub()
    # Act
    autocorrected_text = emotion_service.get_autocorrected_text(text)
    # Assert
    assert autocorrected_text == expected_autocorrected_text


@pytest.mark.parametrize("text, expected_emotion_result", test_emotion_service_get_text2emotion_text_cases)
def test_get_text2emotion(text: str | None, expected_emotion_result: EmotionResult) -> None:
    # Arrange
    emotion_service = EmotionServiceStub()
    # Act
    emotion_result = emotion_service.get_text2emotion(text)
    # Assert
    assert emotion_result == expected_emotion_result
    assert emotion_result.num_happy == expected_emotion_result.num_happy
    assert emotion_result.num_angry == expected_emotion_result.num_angry
    assert emotion_result.num_surprise == expected_emotion_result.num_surprise
    assert emotion_result.num_sad == expected_emotion_result.num_sad
    assert emotion_result.num_fear == expected_emotion_result.num_fear
    assert emotion_result.total_words == expected_emotion_result.total_words
