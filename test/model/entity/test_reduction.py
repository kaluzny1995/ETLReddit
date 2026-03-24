import pytest

from model import ReductionResult, Vector, Reduction

from test.model.entity.fixtures_test_cases import test_reduction_from_vector_cases


@pytest.mark.parametrize("vector, reduction_result, expected_reduction", test_reduction_from_vector_cases)
def test_from_vector(vector: Vector, reduction_result: ReductionResult, expected_reduction: Reduction) -> None:
    # Arrange
    # Act
    reduction = Reduction.from_vector(vector, reduction_result)

    # Assert
    assert reduction.reddit_id == expected_reduction.reddit_id
    assert reduction.comment_id == expected_reduction.comment_id
    assert reduction.phrase == expected_reduction.phrase
    assert reduction.pca2_0 == expected_reduction.pca2_0
    assert reduction.pca2_1 == expected_reduction.pca2_1
    assert reduction.pca3_0 == expected_reduction.pca3_0
    assert reduction.pca3_1 == expected_reduction.pca3_1
    assert reduction.pca3_2 == expected_reduction.pca3_2
    assert reduction.sne2_0 == expected_reduction.sne2_0
    assert reduction.sne2_1 == expected_reduction.sne2_1
    assert reduction.sne3_0 == expected_reduction.sne3_0
    assert reduction.sne3_1 == expected_reduction.sne3_1
    assert reduction.sne3_2 == expected_reduction.sne3_2
    assert reduction.file_date == expected_reduction.file_date
