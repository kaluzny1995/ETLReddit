import pytest

from model import SentimentResult, Reddit, Comment, Sentiment

from test.model.entity.fixtures_test_cases import (test_sentiment_from_reddit_cases,
                                                   test_sentiment_from_comment_cases)


@pytest.mark.parametrize("reddit, text, sentiment_result, expected_sentiment", test_sentiment_from_reddit_cases)
def test_from_reddit(reddit: Reddit, text: str, sentiment_result: SentimentResult, expected_sentiment: Sentiment) -> None:
    # Arrange
    # Act
    sentiment = Sentiment.from_reddit(reddit, text, sentiment_result)

    # Assert
    assert sentiment.reddit_id == expected_sentiment.reddit_id
    assert sentiment.comment_id == expected_sentiment.comment_id
    assert sentiment.phrase == expected_sentiment.phrase
    assert sentiment.author == expected_sentiment.author
    assert sentiment.text == expected_sentiment.text
    assert sentiment.datetime_created == expected_sentiment.datetime_created
    assert sentiment.score == expected_sentiment.score
    assert sentiment.upvote_ratio == expected_sentiment.upvote_ratio
    assert sentiment.gilded_number == expected_sentiment.gilded_number
    assert sentiment.number_of_comments == expected_sentiment.number_of_comments
    assert sentiment.controversiality == expected_sentiment.controversiality
    assert sentiment.s_neg == expected_sentiment.s_neg
    assert sentiment.s_neu == expected_sentiment.s_neu
    assert sentiment.s_pos == expected_sentiment.s_pos
    assert sentiment.s_com == expected_sentiment.s_com
    assert sentiment.s_pol == expected_sentiment.s_pol
    assert sentiment.s_sub == expected_sentiment.s_sub
    assert sentiment.file_date == expected_sentiment.file_date


@pytest.mark.parametrize("comment, text, sentiment_result, expected_sentiment", test_sentiment_from_comment_cases)
def test_from_comment(comment: Comment, text: str, sentiment_result: SentimentResult, expected_sentiment: Sentiment) -> None:
    # Arrange
    # Act
    sentiment = Sentiment.from_comment(comment, text, sentiment_result)

    # Assert
    assert sentiment.reddit_id == expected_sentiment.reddit_id
    assert sentiment.comment_id == expected_sentiment.comment_id
    assert sentiment.phrase == expected_sentiment.phrase
    assert sentiment.author == expected_sentiment.author
    assert sentiment.text == expected_sentiment.text
    assert sentiment.datetime_created == expected_sentiment.datetime_created
    assert sentiment.score == expected_sentiment.score
    assert sentiment.upvote_ratio == expected_sentiment.upvote_ratio
    assert sentiment.gilded_number == expected_sentiment.gilded_number
    assert sentiment.number_of_comments == expected_sentiment.number_of_comments
    assert sentiment.controversiality == expected_sentiment.controversiality
    assert sentiment.s_neg == expected_sentiment.s_neg
    assert sentiment.s_neu == expected_sentiment.s_neu
    assert sentiment.s_pos == expected_sentiment.s_pos
    assert sentiment.s_com == expected_sentiment.s_com
    assert sentiment.s_pol == expected_sentiment.s_pol
    assert sentiment.s_sub == expected_sentiment.s_sub
    assert sentiment.file_date == expected_sentiment.file_date
