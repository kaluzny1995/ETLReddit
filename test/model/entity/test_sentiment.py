import pytest

from model import SentimentResult, Reddit, Comment, Sentiment

from test.model.entity.fixtures_test_cases import (test_sentiment_from_reddit_cases,
                                                   test_sentiment_from_comment_cases)


@pytest.mark.parametrize("reddit, clean_text, sentiment_result, expected_sentiment", test_sentiment_from_reddit_cases)
def test_from_reddit(reddit: Reddit, clean_text: str, sentiment_result: SentimentResult, expected_sentiment: Sentiment) -> None:
    # Arrange
    # Act
    sentiment = Sentiment.from_reddit(reddit, clean_text, sentiment_result)

    # Assert
    assert sentiment.reddit_id == expected_sentiment.reddit_id
    assert sentiment.comment_id == expected_sentiment.comment_id
    assert sentiment.phrase == expected_sentiment.phrase
    assert sentiment.author == expected_sentiment.author
    assert sentiment.entry_type == expected_sentiment.entry_type
    assert sentiment.clean_text == expected_sentiment.clean_text
    assert sentiment.s_neg == expected_sentiment.s_neg
    assert sentiment.s_neu == expected_sentiment.s_neu
    assert sentiment.s_pos == expected_sentiment.s_pos
    assert sentiment.s_com == expected_sentiment.s_com
    assert sentiment.s_pol == expected_sentiment.s_pol
    assert sentiment.s_sub == expected_sentiment.s_sub
    assert sentiment.s_class == expected_sentiment.s_class
    assert sentiment.file_date == expected_sentiment.file_date


@pytest.mark.parametrize("comment, clean_text, sentiment_result, expected_sentiment", test_sentiment_from_comment_cases)
def test_from_comment(comment: Comment, clean_text: str, sentiment_result: SentimentResult, expected_sentiment: Sentiment) -> None:
    # Arrange
    # Act
    sentiment = Sentiment.from_comment(comment, clean_text, sentiment_result)

    # Assert
    assert sentiment.reddit_id == expected_sentiment.reddit_id
    assert sentiment.comment_id == expected_sentiment.comment_id
    assert sentiment.phrase == expected_sentiment.phrase
    assert sentiment.author == expected_sentiment.author
    assert sentiment.entry_type == expected_sentiment.entry_type
    assert sentiment.clean_text == expected_sentiment.clean_text
    assert sentiment.s_neg == expected_sentiment.s_neg
    assert sentiment.s_neu == expected_sentiment.s_neu
    assert sentiment.s_pos == expected_sentiment.s_pos
    assert sentiment.s_com == expected_sentiment.s_com
    assert sentiment.s_pol == expected_sentiment.s_pol
    assert sentiment.s_sub == expected_sentiment.s_sub
    assert sentiment.s_class == expected_sentiment.s_class
    assert sentiment.file_date == expected_sentiment.file_date
