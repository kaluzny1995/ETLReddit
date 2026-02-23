import pytest
from typing import List

from model import Reddit
from model.enum.e_file_date_type import EFileDateType
from test.provider.stub.supabase_postgres_reddit_provider_stub import SupabasePostgresRedditProviderStub
from test.provider.supabase_postgres.fixtures_test_cases import reddits as all_reddits


@pytest.mark.parametrize("reddits, which, expected_file_dates", [
    (all_reddits, EFileDateType.START, ["2026-01-01", "2022-01-01", "2022-01-01", "2024-01-01"]),
    (all_reddits, EFileDateType.END, ["2027-01-01", "2023-01-01", "2023-01-01", "2025-01-01"]),
    ([all_reddits[0], all_reddits[3]], EFileDateType.START, ["2026-01-01", "2024-01-01"]),
    ([all_reddits[0], all_reddits[3]], EFileDateType.END, ["2027-01-01", "2025-01-01"])
])
def test_get_file_dates(reddits: List[Reddit], which: EFileDateType, expected_file_dates: List[str]) -> None:
    # Arrange
    supabase_postgres_reddits_provider = SupabasePostgresRedditProviderStub(reddits)
    # Act
    file_dates = supabase_postgres_reddits_provider.get_file_dates(phrase="", which=which)
    # Assert
    assert len(file_dates) == len(expected_file_dates)
    for fd, efd in zip(file_dates, expected_file_dates):
        assert fd == efd


@pytest.mark.parametrize("reddits, expected_reddits", [
    (all_reddits, all_reddits),
    ([all_reddits[0], all_reddits[3]], [all_reddits[0], all_reddits[3]])
])
def test_get_reddits(reddits: List[Reddit], expected_reddits: List[Reddit]) -> None:
    # Arrange
    supabase_postgres_reddits_provider = SupabasePostgresRedditProviderStub(reddits)
    # Act
    returned_reddits = supabase_postgres_reddits_provider.get_reddits(phrase="", file_dates=[], which=EFileDateType.START)
    # Assert
    assert len(returned_reddits) == len(expected_reddits)
    for rr, er in zip(returned_reddits, expected_reddits):
        assert rr.reddit_id == er.reddit_id
        assert rr.name == er.name
        assert rr.permalink == er.permalink
        assert rr.phrase == er.phrase
        assert rr.author == er.author
        assert rr.title == er.title
        assert rr.body == er.body
        assert rr.datetime_created == er.datetime_created
        assert rr.datetime_created_utc == er.datetime_created_utc
        assert rr.likes == er.likes
        assert rr.ups == er.ups
        assert rr.downs == er.downs
        assert rr.score == er.score
        assert rr.upvote_ratio == er.upvote_ratio
        assert rr.gilded_number == er.gilded_number
        assert rr.number_of_comments == er.number_of_comments
        assert rr.start_file_date == er.start_file_date
        assert rr.end_file_date == er.end_file_date
