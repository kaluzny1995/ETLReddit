import pytest
from typing import List

from model import Reduction
from test.provider.stub.supabase_postgres_reduction_provider_stub import SupabasePostgresReductionProviderStub
from test.provider.supabase_postgres.fixtures_test_cases import reductions as all_reductions


@pytest.mark.parametrize("reductions, expected_file_dates", [
    (all_reductions, ["2026-01-01", "2022-01-01", "2022-01-01", "2026-01-01"]),
    ([all_reductions[0], all_reductions[3]], ["2026-01-01", "2026-01-01"])
])
def test_get_file_dates(reductions: List[Reduction], expected_file_dates: List[str]) -> None:
    # Arrange
    supabase_postgres_reduction_provider = SupabasePostgresReductionProviderStub(reductions)
    # Act
    file_dates = supabase_postgres_reduction_provider.get_file_dates(phrase="")
    # Assert
    assert len(file_dates) == len(expected_file_dates)
    for fd, efd in zip(file_dates, expected_file_dates):
        assert fd == efd


@pytest.mark.parametrize("reductions, expected_reductions", [
    (all_reductions, all_reductions),
    ([all_reductions[0], all_reductions[3]], [all_reductions[0], all_reductions[3]])
])
def test_get_sentiments(reductions: List[Reduction], expected_reductions: List[Reduction]) -> None:
    # Arrange
    supabase_postgres_reduction_provider = SupabasePostgresReductionProviderStub(reductions)
    # Act
    returned_reductions = supabase_postgres_reduction_provider.get_reductions(phrase="")
    # Assert
    assert len(returned_reductions) == len(expected_reductions)
    for rp, ep in zip(returned_reductions, expected_reductions):
        assert rp.reddit_id == ep.reddit_id
        assert rp.comment_id == ep.comment_id
        assert rp.phrase == ep.phrase
        assert rp.pca2_0 == ep.pca2_0
        assert rp.pca2_1 == ep.pca2_1
        assert rp.pca3_0 == ep.pca3_0
        assert rp.pca3_1 == ep.pca3_1
        assert rp.pca3_2 == ep.pca3_2
        assert rp.sne2_0 == ep.sne2_0
        assert rp.sne2_1 == ep.sne2_1
        assert rp.sne3_0 == ep.sne3_0
        assert rp.sne3_1 == ep.sne3_1
        assert rp.sne3_2 == ep.sne3_2
        assert rp.file_date == ep.file_date
