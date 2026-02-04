import pytest

from model import Sentiment, Reddit, Comment, SentimentAnalysis

from test.model.entity.fixtures_test_cases import (test_sentiment_analysis_from_reddit_cases,
                                                   test_sentiment_analysis_from_comment_cases)


@pytest.mark.parametrize("reddit, text, sentiment, expected_sentiment_analysis", test_sentiment_analysis_from_reddit_cases)
def test_from_reddit(reddit: Reddit, text: str, sentiment: Sentiment, expected_sentiment_analysis: SentimentAnalysis) -> None:
    # Arrange
    # Act
    sentiment_analysis = SentimentAnalysis.from_reddit(reddit, text, sentiment)

    # Assert
    assert sentiment_analysis.reddit_id == expected_sentiment_analysis.reddit_id
    assert sentiment_analysis.comment_id == expected_sentiment_analysis.comment_id
    assert sentiment_analysis.phrase == expected_sentiment_analysis.phrase
    assert sentiment_analysis.author == expected_sentiment_analysis.author
    assert sentiment_analysis.text == expected_sentiment_analysis.text
    assert sentiment_analysis.datetime_created == expected_sentiment_analysis.datetime_created
    assert sentiment_analysis.score == expected_sentiment_analysis.score
    assert sentiment_analysis.upvote_ratio == expected_sentiment_analysis.upvote_ratio
    assert sentiment_analysis.gilded_number == expected_sentiment_analysis.gilded_number
    assert sentiment_analysis.number_of_comments == expected_sentiment_analysis.number_of_comments
    assert sentiment_analysis.controversiality == expected_sentiment_analysis.controversiality
    assert sentiment_analysis.s_neg == expected_sentiment_analysis.s_neg
    assert sentiment_analysis.s_neu == expected_sentiment_analysis.s_neu
    assert sentiment_analysis.s_pos == expected_sentiment_analysis.s_pos
    assert sentiment_analysis.s_com == expected_sentiment_analysis.s_com
    assert sentiment_analysis.s_pol == expected_sentiment_analysis.s_pol
    assert sentiment_analysis.s_sub == expected_sentiment_analysis.s_sub
    assert sentiment_analysis.file_date == expected_sentiment_analysis.file_date


@pytest.mark.parametrize("comment, text, sentiment, expected_sentiment_analysis", test_sentiment_analysis_from_comment_cases)
def test_from_comment(comment: Comment, text: str, sentiment: Sentiment, expected_sentiment_analysis: SentimentAnalysis) -> None:
    # Arrange
    # Act
    sentiment_analysis = SentimentAnalysis.from_comment(comment, text, sentiment)

    # Assert
    assert sentiment_analysis.reddit_id == expected_sentiment_analysis.reddit_id
    assert sentiment_analysis.comment_id == expected_sentiment_analysis.comment_id
    assert sentiment_analysis.phrase == expected_sentiment_analysis.phrase
    assert sentiment_analysis.author == expected_sentiment_analysis.author
    assert sentiment_analysis.text == expected_sentiment_analysis.text
    assert sentiment_analysis.datetime_created == expected_sentiment_analysis.datetime_created
    assert sentiment_analysis.score == expected_sentiment_analysis.score
    assert sentiment_analysis.upvote_ratio == expected_sentiment_analysis.upvote_ratio
    assert sentiment_analysis.gilded_number == expected_sentiment_analysis.gilded_number
    assert sentiment_analysis.number_of_comments == expected_sentiment_analysis.number_of_comments
    assert sentiment_analysis.controversiality == expected_sentiment_analysis.controversiality
    assert sentiment_analysis.s_neg == expected_sentiment_analysis.s_neg
    assert sentiment_analysis.s_neu == expected_sentiment_analysis.s_neu
    assert sentiment_analysis.s_pos == expected_sentiment_analysis.s_pos
    assert sentiment_analysis.s_com == expected_sentiment_analysis.s_com
    assert sentiment_analysis.s_pol == expected_sentiment_analysis.s_pol
    assert sentiment_analysis.s_sub == expected_sentiment_analysis.s_sub
    assert sentiment_analysis.file_date == expected_sentiment_analysis.file_date
