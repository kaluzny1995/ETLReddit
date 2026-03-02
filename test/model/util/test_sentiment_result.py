import pytest

from model import NLTKSentiment, TextblobSentiment, SentimentResult


@pytest.mark.parametrize("nltk_sentiment, textblob_sentiment, expected_sentiment_result", [
    (NLTKSentiment(negative=0., neutral=0., positive=0., compound=0.),
     TextblobSentiment(polarity=0., subjectivity=0.),
     SentimentResult(negative=0., neutral=0., positive=0., compound=0., polarity=0., subjectivity=0.)),
    (NLTKSentiment(negative=0.1, neutral=0.2, positive=0.3, compound=0.4),
     TextblobSentiment(polarity=0.5, subjectivity=0.6),
     SentimentResult(negative=0.1, neutral=0.2, positive=0.3, compound=0.4, polarity=0.5, subjectivity=0.6)),
    (NLTKSentiment(negative=0.3, neutral=0.5, positive=0.3, compound=0.45),
     TextblobSentiment(polarity=-0.2, subjectivity=0.33),
     SentimentResult(negative=0.3, neutral=0.5, positive=0.3, compound=0.45, polarity=-0.2, subjectivity=0.33))
])
def test_from_ntlk_and_textblob(nltk_sentiment: NLTKSentiment, textblob_sentiment: TextblobSentiment,
                                expected_sentiment_result: SentimentResult) -> None:
    # Arrange
    # Act
    sentiment_result = SentimentResult.from_ntlk_and_textblob(nltk_sentiment, textblob_sentiment)

    # Assert
    assert sentiment_result.negative == expected_sentiment_result.negative
    assert sentiment_result.neutral == expected_sentiment_result.neutral
    assert sentiment_result.positive == expected_sentiment_result.positive
    assert sentiment_result.compound == expected_sentiment_result.compound
    assert sentiment_result.polarity == expected_sentiment_result.polarity
    assert sentiment_result.subjectivity == expected_sentiment_result.subjectivity
