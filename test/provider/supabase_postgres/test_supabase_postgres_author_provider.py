import pytest
from typing import List

from model import Author
from test.provider.stub.supabase_postgres_author_provider_stub import SupabasePostgresDbAuthorProviderStub
from test.provider.supabase_postgres.fixtures_test_cases import authors as all_authors


@pytest.mark.parametrize("authors, expected_names", [
    (all_authors, ["MooseWhisperer09", "ch0c0l2te", "OmdiAnomenkinshin", "aarretuli"]),
    ([all_authors[0], all_authors[3]], ["MooseWhisperer09", "aarretuli"]),
])
def test_get_names(authors: List[Author], expected_names: List[str]) -> None:
    # Arrange
    supabase_postgres_author_provider = SupabasePostgresDbAuthorProviderStub(authors)
    # Act
    names = supabase_postgres_author_provider.get_names()
    # Assert
    assert len(names) == len(expected_names)
    for n, en in zip(names, expected_names):
        assert n == en
