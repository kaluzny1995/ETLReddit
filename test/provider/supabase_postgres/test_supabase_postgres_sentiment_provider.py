import pytest
from typing import List

from model import Sentiment
from test.provider.stub.supabase_postgres_sentiment_provider_stub import SupabasePostgresSentimentProviderStub
from test.provider.supabase_postgres.fixtures_test_cases import sentiments as all_sentiments


@pytest.mark.parametrize("sentiments, expected_file_dates", [
    (all_sentiments, ["2026-01-01", "2022-01-01", "2020-01-01", "2020-01-01"]),
    ([all_sentiments[0], all_sentiments[3]], ["2026-01-01", "2020-01-01"])
])
def test_get_file_dates(sentiments: List[Sentiment], expected_file_dates: List[str]) -> None:
    # Arrange
    supabase_postgres_sentiment_provider = SupabasePostgresSentimentProviderStub(sentiments)
    # Act
    file_dates = supabase_postgres_sentiment_provider.get_file_dates(phrase="")
    # Assert
    assert len(file_dates) == len(expected_file_dates)
    for fd, efd in zip(file_dates, expected_file_dates):
        assert fd == efd


@pytest.mark.parametrize("sentiments, expected_sentiments", [
    (all_sentiments, all_sentiments),
    ([all_sentiments[0], all_sentiments[3]], [all_sentiments[0], all_sentiments[3]])
])
def test_get_sentiments(sentiments: List[Sentiment], expected_sentiments: List[Sentiment]) -> None:
    # Arrange
    supabase_postgres_sentiment_provider = SupabasePostgresSentimentProviderStub(sentiments)
    # Act
    returned_sentiments = supabase_postgres_sentiment_provider.get_sentiments(phrase="")
    # Assert
    assert len(returned_sentiments) == len(expected_sentiments)
    for rr, er in zip(returned_sentiments, expected_sentiments):
        assert rr.reddit_id == er.reddit_id
        assert rr.comment_id == er.comment_id
        assert rr.phrase == er.phrase
        assert rr.author == er.author
        assert rr.text == er.text
        assert rr.datetime_created == er.datetime_created
        assert rr.score == er.score
        assert rr.upvote_ratio == er.upvote_ratio
        assert rr.gilded_number == er.gilded_number
        assert rr.number_of_comments == er.number_of_comments
        assert rr.controversiality == er.controversiality
        assert rr.s_neg == er.s_neg
        assert rr.s_neu == er.s_neu
        assert rr.s_pos == er.s_pos
        assert rr.s_com == er.s_com
        assert rr.s_pol == er.s_pol
        assert rr.s_sub == er.s_sub
        assert rr.file_date == er.file_date
