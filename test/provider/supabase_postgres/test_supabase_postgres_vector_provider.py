import pytest
from typing import List

from model import Vector
from test.provider.stub.supabase_postgres_vector_provider_stub import SupabasePostgresVectorProviderStub
from test.provider.supabase_postgres.fixtures_test_cases import vectors as all_vectors


@pytest.mark.parametrize("vectors, expected_file_dates", [
    (all_vectors, ["2026-01-01", "2022-01-01", "2022-01-01", "2026-01-01"]),
    ([all_vectors[0], all_vectors[3]], ["2026-01-01", "2026-01-01"])
])
def test_get_file_dates(vectors: List[Vector], expected_file_dates: List[str]) -> None:
    # Arrange
    supabase_postgres_vector_provider = SupabasePostgresVectorProviderStub(vectors)
    # Act
    file_dates = supabase_postgres_vector_provider.get_file_dates(phrase="")
    # Assert
    assert len(file_dates) == len(expected_file_dates)
    for fd, efd in zip(file_dates, expected_file_dates):
        assert fd == efd


@pytest.mark.parametrize("vectors, expected_vectors", [
    (all_vectors, all_vectors),
    ([all_vectors[0], all_vectors[3]], [all_vectors[0], all_vectors[3]])
])
def test_get_sentiments(vectors: List[Vector], expected_vectors: List[Vector]) -> None:
    # Arrange
    supabase_postgres_vector_provider = SupabasePostgresVectorProviderStub(vectors)
    # Act
    returned_vectors = supabase_postgres_vector_provider.get_vectors(phrase="")
    # Assert
    assert len(returned_vectors) == len(expected_vectors)
    for rp, ep in zip(returned_vectors, expected_vectors):
        assert rp.reddit_id == ep.reddit_id
        assert rp.comment_id == ep.comment_id
        assert rp.phrase == ep.phrase
        assert rp.embeddings == ep.embeddings
        assert rp.file_date == ep.file_date
