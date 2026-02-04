import pytest
from typing import Any, List

import util


@pytest.mark.parametrize("filename, expected_start_date_str", [
    ("reddits_corgi_2020-01-01T00:00:00_2021-01-01T00:00:00.json", "2020-01-01T00:00:00"),
    ("reddits_corgi_2023-01-01T00:00:00_2024-01-01T00:00:00.json", "2023-01-01T00:00:00"),
    ("reddits_corgi_2026-01-01T00:00:00_2027-01-01T00:00:00.json", "2026-01-01T00:00:00")
])
def test_get_start_date_string_from_filename(filename: str, expected_start_date_str: str):
    # Arrange
    # Act
    start_date_str = util.get_start_date_string_from_filename(filename)
    # Assert
    assert start_date_str == expected_start_date_str


@pytest.mark.parametrize("filename, expected_end_date_str", [
    ("reddits_corgi_2020-01-01T00:00:00_2021-01-01T00:00:00.json", "2021-01-01T00:00:00"),
    ("reddits_corgi_2023-01-01T00:00:00_2024-01-01T00:00:00.json", "2024-01-01T00:00:00"),
    ("reddits_corgi_2026-01-01T00:00:00_2027-01-01T00:00:00.json", "2027-01-01T00:00:00")
])
def test_get_end_date_string_from_filename(filename: str, expected_end_date_str: str):
    # Arrange
    # Act
    start_date_str = util.get_end_date_string_from_filename(filename)
    # Assert
    assert start_date_str == expected_end_date_str


@pytest.mark.parametrize("elements, batch_size, expected_chunks", [
    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]),
    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 4, [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]]),
    (["one", "two", "three", "four", "five", "six", "seven"], 4, [["one", "two", "three", "four"], ["five", "six", "seven"]]),
    ([False, False, True, True], 3, [[False, False, True], [True]])
])
def test_chunk_list_equal_size(elements: List[Any], batch_size: int, expected_chunks: List[List[Any]]) -> None:
    # Arrange
    # Act
    chunks = util.chunk_list_equal_size(elements, batch_size)
    print(chunks)

    # Assert
    assert len(chunks) == len(expected_chunks)
    for chunk, expected_chunk in zip(chunks, expected_chunks):
        assert len(chunk) == len(expected_chunk)
        for element, expected_element in zip(chunk, expected_chunk):
            assert element == expected_element


@pytest.mark.parametrize("elements, number, expected_chunks", [
    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 3, [[0, 3, 6, 9], [1, 4, 7], [2, 5, 8]]),
    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 4, [[0, 4, 8], [1, 5, 9], [2, 6], [3, 7]]),
    (["one", "two", "three", "four", "five", "six", "seven"], 4, [["one", "five"], ["two", "six"], ["three", "seven"], ["four"]]),
    ([False, False, True, True], 3, [[False, True], [False], [True]])
])
def test_chunk_list_n_elements(elements: List[Any], number: int, expected_chunks: List[List[Any]]) -> None:
    # Arrange
    # Act
    chunks = util.chunk_list_n_elements(elements, number)

    # Assert
    assert len(chunks) == len(expected_chunks)
    for chunk, expected_chunk in zip(chunks, expected_chunks):
        assert len(chunk) == len(expected_chunk)
        for element, expected_element in zip(chunk, expected_chunk):
            assert element == expected_element
