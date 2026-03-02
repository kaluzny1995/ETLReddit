import pytest

from model import NLTKSentiment, TextblobSentiment

from test.service.stub.sentiment_service_stub import SentimentServiceStub
from test.service.sentiment.fixtures_test_cases import (
    test_sentiment_service_get_autocorrected_text_cases,
    test_sentiment_service_get_nltk_sentiment_cases,
    test_sentiment_service_get_textblob_sentiment_cases
)


@pytest.mark.parametrize("text, expected_autocorrected_text", test_sentiment_service_get_autocorrected_text_cases)
def test_get_autocorrected_text(text: str | None, expected_autocorrected_text: str | None) -> None:
    # Arrange
    sentiment_service = SentimentServiceStub()
    # Act
    autocorrected_text = sentiment_service.get_autocorrected_text(text)
    # Assert
    assert autocorrected_text == expected_autocorrected_text


@pytest.mark.parametrize("text, expected_nltk_sentiment", test_sentiment_service_get_nltk_sentiment_cases)
def test_get_nltk_sentiment(text: str | None, expected_nltk_sentiment: NLTKSentiment) -> None:
    # Arrange
    sentiment_service = SentimentServiceStub()
    # Act
    nltk_sentiment = sentiment_service.get_nltk_sentiment(text)
    # Assert
    assert nltk_sentiment.negative == expected_nltk_sentiment.negative
    assert nltk_sentiment.neutral == expected_nltk_sentiment.neutral
    assert nltk_sentiment.positive == expected_nltk_sentiment.positive
    assert nltk_sentiment.compound == expected_nltk_sentiment.compound


@pytest.mark.parametrize("text, expected_textblob_sentiment", test_sentiment_service_get_textblob_sentiment_cases)
def test_get_textblob_sentiment(text: str | None, expected_textblob_sentiment: TextblobSentiment) -> None:
    # Arrange
    sentiment_service = SentimentServiceStub()
    # Act
    textblob_sentiment = sentiment_service.get_textblob_sentiment(text)
    # Assert
    assert textblob_sentiment.polarity == expected_textblob_sentiment.polarity
    assert textblob_sentiment.subjectivity == expected_textblob_sentiment.subjectivity
