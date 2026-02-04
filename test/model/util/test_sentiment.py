import pytest

from model import NLTKSentiment, TextblobSentiment, Sentiment


@pytest.mark.parametrize("nltk_sentiment, textblob_sentiment, expected_sentiment", [
    (NLTKSentiment(negative=0., neutral=0., positive=0., compound=0.),
     TextblobSentiment(polarity=0., subjectivity=0.),
     Sentiment(negative=0., neutral=0., positive=0., compound=0., polarity=0., subjectivity=0.)),
    (NLTKSentiment(negative=0.1, neutral=0.2, positive=0.3, compound=0.4),
     TextblobSentiment(polarity=0.5, subjectivity=0.6),
     Sentiment(negative=0.1, neutral=0.2, positive=0.3, compound=0.4, polarity=0.5, subjectivity=0.6)),
    (NLTKSentiment(negative=0.3, neutral=0.5, positive=0.3, compound=0.45),
     TextblobSentiment(polarity=-0.2, subjectivity=0.33),
     Sentiment(negative=0.3, neutral=0.5, positive=0.3, compound=0.45, polarity=-0.2, subjectivity=0.33))
])
def test_from_ntlk_and_textblob(nltk_sentiment: NLTKSentiment, textblob_sentiment: TextblobSentiment, expected_sentiment: Sentiment) -> None:
    # Arrange
    # Act
    sentiment = Sentiment.from_ntlk_and_textblob(nltk_sentiment, textblob_sentiment)

    # Assert
    assert sentiment.negative == expected_sentiment.negative
    assert sentiment.neutral == expected_sentiment.neutral
    assert sentiment.positive == expected_sentiment.positive
    assert sentiment.compound == expected_sentiment.compound
    assert sentiment.polarity == expected_sentiment.polarity
    assert sentiment.subjectivity == expected_sentiment.subjectivity
