import pytest
from typing import List

from model import SentimentAnalysis
from test.provider.stub.supabase_postgres_sentiment_analysis_provider_stub import SupabasePostgresSentimentAnalysisProviderStub
from test.provider.supabase_postgres.fixtures_test_cases import sentiment_analyses as all_sentiment_analyses


@pytest.mark.parametrize("sentiment_analyses, expected_file_dates", [
    (all_sentiment_analyses, ["2026-01-01", "2022-01-01", "2020-01-01", "2020-01-01"]),
    ([all_sentiment_analyses[0], all_sentiment_analyses[3]], ["2026-01-01", "2020-01-01"])
])
def test_get_file_dates(sentiment_analyses: List[SentimentAnalysis], expected_file_dates: List[str]) -> None:
    # Arrange
    supabase_postgres_sentiment_analysis_provider = SupabasePostgresSentimentAnalysisProviderStub(sentiment_analyses)
    # Act
    file_dates = supabase_postgres_sentiment_analysis_provider.get_file_dates(phrase="")
    # Assert
    assert len(file_dates) == len(expected_file_dates)
    for fd, efd in zip(file_dates, expected_file_dates):
        assert fd == efd


@pytest.mark.parametrize("sentiment_analyses, expected_sentiment_analyses", [
    (all_sentiment_analyses, all_sentiment_analyses),
    ([all_sentiment_analyses[0], all_sentiment_analyses[3]], [all_sentiment_analyses[0], all_sentiment_analyses[3]])
])
def test_get_sentiment_analyses(sentiment_analyses: List[SentimentAnalysis], expected_sentiment_analyses: List[SentimentAnalysis]) -> None:
    # Arrange
    supabase_postgres_sentiment_analysis_provider = SupabasePostgresSentimentAnalysisProviderStub(sentiment_analyses)
    # Act
    returned_sentiment_analyses = supabase_postgres_sentiment_analysis_provider.get_sentiment_analyses(phrase="")
    # Assert
    assert len(returned_sentiment_analyses) == len(expected_sentiment_analyses)
    for rr, er in zip(returned_sentiment_analyses, expected_sentiment_analyses):
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
