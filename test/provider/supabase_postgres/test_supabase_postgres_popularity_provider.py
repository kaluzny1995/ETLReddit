import pytest
from typing import List

from model import Popularity
from test.provider.stub.supabase_postgres_popularity_provider import SupabasePostgresPopularityProviderStub
from test.provider.supabase_postgres.fixtures_test_cases import popularities as all_popularities


@pytest.mark.parametrize("popularities, expected_file_dates", [
    (all_popularities, ["2026-01-01", "2022-01-01", "2022-01-01", "2026-01-01"]),
    ([all_popularities[0], all_popularities[3]], ["2026-01-01", "2026-01-01"])
])
def test_get_file_dates(popularities: List[Popularity], expected_file_dates: List[str]) -> None:
    # Arrange
    supabase_postgres_popularity_provider = SupabasePostgresPopularityProviderStub(popularities)
    # Act
    file_dates = supabase_postgres_popularity_provider.get_file_dates(phrase="")
    # Assert
    assert len(file_dates) == len(expected_file_dates)
    for fd, efd in zip(file_dates, expected_file_dates):
        assert fd == efd


@pytest.mark.parametrize("popularities, expected_popularities", [
    (all_popularities, all_popularities),
    ([all_popularities[0], all_popularities[3]], [all_popularities[0], all_popularities[3]])
])
def test_get_sentiments(popularities: List[Popularity], expected_popularities: List[Popularity]) -> None:
    # Arrange
    supabase_postgres_popularity_provider = SupabasePostgresPopularityProviderStub(popularities)
    # Act
    returned_popularities = supabase_postgres_popularity_provider.get_popularities(phrase="")
    # Assert
    assert len(returned_popularities) == len(expected_popularities)
    for rp, ep in zip(returned_popularities, expected_popularities):
        assert rp.reddit_id == ep.reddit_id
        assert rp.comment_id == ep.comment_id
        assert rp.phrase == ep.phrase
        assert rp.author == ep.author
        assert rp.entry_type == ep.entry_type
        assert rp.entry_level == ep.entry_level
        assert rp.score == ep.score
        assert rp.upvote_ratio == ep.upvote_ratio
        assert rp.gilded_count == ep.gilded_count
        assert rp.comments_count == ep.comments_count
        assert rp.is_controversial == ep.is_controversial
        assert rp.file_date == ep.file_date
