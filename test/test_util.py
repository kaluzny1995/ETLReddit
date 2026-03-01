import pytest
import datetime as dt
from typing import Any, List, Tuple

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


@pytest.mark.parametrize("start_date, end_date, interval, expected_date_periods", [
    (dt.datetime(2026, 1, 1, 20), dt.datetime(2026, 1, 2, 1), "h", [
        (dt.datetime(2026, 1, 1, 20), dt.datetime(2026, 1, 1, 21)),
        (dt.datetime(2026, 1, 1, 21), dt.datetime(2026, 1, 1, 22)),
        (dt.datetime(2026, 1, 1, 22), dt.datetime(2026, 1, 1, 23)),
        (dt.datetime(2026, 1, 1, 23), dt.datetime(2026, 1, 2, 0)),
        (dt.datetime(2026, 1, 2, 0), dt.datetime(2026, 1, 2, 1)),
        (dt.datetime(2026, 1, 2, 1), dt.datetime(2026, 1, 2, 2))
    ]),
    (dt.datetime(2026, 1, 30), dt.datetime(2026, 2, 5), "d", [
        (dt.datetime(2026, 1, 30), dt.datetime(2026, 1, 31)),
        (dt.datetime(2026, 1, 31), dt.datetime(2026, 2, 1)),
        (dt.datetime(2026, 2, 1), dt.datetime(2026, 2, 2)),
        (dt.datetime(2026, 2, 2), dt.datetime(2026, 2, 3)),
        (dt.datetime(2026, 2, 3), dt.datetime(2026, 2, 4)),
        (dt.datetime(2026, 2, 4), dt.datetime(2026, 2, 5)),
        (dt.datetime(2026, 2, 5), dt.datetime(2026, 2, 6))
    ]),
    (dt.datetime(2025, 12, 10), dt.datetime(2026, 4, 20), "m", [
        (dt.datetime(2025, 12, 1), dt.datetime(2026, 1, 1)),
        (dt.datetime(2026, 1, 1), dt.datetime(2026, 2, 1)),
        (dt.datetime(2026, 2, 1), dt.datetime(2026, 3, 1)),
        (dt.datetime(2026, 3, 1), dt.datetime(2026, 4, 1)),
        (dt.datetime(2026, 4, 1), dt.datetime(2026, 5, 1))
    ]),
    (dt.datetime(2019, 10, 10), dt.datetime(2026, 2, 10), "y", [
        (dt.datetime(2019, 1, 1), dt.datetime(2020, 1, 1)),
        (dt.datetime(2020, 1, 1), dt.datetime(2021, 1, 1)),
        (dt.datetime(2021, 1, 1), dt.datetime(2022, 1, 1)),
        (dt.datetime(2022, 1, 1), dt.datetime(2023, 1, 1)),
        (dt.datetime(2023, 1, 1), dt.datetime(2024, 1, 1)),
        (dt.datetime(2024, 1, 1), dt.datetime(2025, 1, 1)),
        (dt.datetime(2025, 1, 1), dt.datetime(2026, 1, 1)),
        (dt.datetime(2026, 1, 1), dt.datetime(2027, 1, 1))
    ])
])
def test_date_range(start_date: dt.datetime, end_date: dt.datetime, interval: str | None,
                    expected_date_periods: List[Tuple[dt.datetime, dt.datetime]]) -> None:
    # Arrange
    # Act
    date_periods = list(util.date_range(start_date, end_date, interval))

    # Assert
    assert len(date_periods) == len(expected_date_periods)
    for date_period, expected_date_period in zip(date_periods, expected_date_periods):
        assert date_period[0] == expected_date_period[0]
        assert date_period[1] == expected_date_period[1]
