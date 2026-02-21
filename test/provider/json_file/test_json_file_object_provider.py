from typing import List, Dict, Any

import pytest

from test.provider.json_file.fixtures_test_cases import file_names, json_objects
from test.provider.stub.json_file_object_provider_stub import JsonFileObjectProviderStub


@pytest.mark.parametrize("file_dates, expected_file_names", [
    (["2020-01-01T00:00:00", "2021-01-01T00:00:00", "2022-01-01T00:00:00"], [file_names[0], file_names[1], file_names[2]]),
    (["2025-01-01T00:00:00", "2026-01-01T00:00:00"], [file_names[5], file_names[6]])
])
def test_get_file_names(file_dates: List[str], expected_file_names: List[str]) -> None:
    # Arrange
    json_file_object_provider = JsonFileObjectProviderStub(file_names, json_objects)
    # Act
    found_file_names = json_file_object_provider.get_file_names(file_dates)
    # Assert
    assert len(found_file_names) == len(expected_file_names)
    for ffn, efn in zip(found_file_names, expected_file_names):
        assert ffn == efn


@pytest.mark.parametrize("file_date, expected_file_name", [
    ("2020-01-01T00:00:00", file_names[0]),
    ("2021-01-01T00:00:00", file_names[1]),
    ("2025-01-01T00:00:00", file_names[5]),
    ("2026-01-01T00:00:00", file_names[6])
])
def test_get_file_name(file_date: str, expected_file_name: str) -> None:
    # Arrange
    json_file_object_provider = JsonFileObjectProviderStub(file_names, json_objects)
    # Act
    found_file_name = json_file_object_provider.get_file_name(file_date)
    # Assert
    assert found_file_name == expected_file_name


@pytest.mark.parametrize("file_dates, expected_json_objects", [
    (["2020-01-01T00:00:00", "2021-01-01T00:00:00", "2022-01-01T00:00:00"], [json_objects[0], json_objects[1], json_objects[2]]),
    (["2025-01-01T00:00:00", "2026-01-01T00:00:00"], [json_objects[5], json_objects[6]])
])
def test_get_json_objects(file_dates: List[str], expected_json_objects: List[List[Dict[str, Any] | List[Any]]]) -> None:
    # Arrange
    json_file_object_provider = JsonFileObjectProviderStub(file_names, json_objects)
    # Act
    found_json_objects = json_file_object_provider.get_json_objects(file_dates)
    # Assert
    assert len(found_json_objects) == len(expected_json_objects)
    for fjo, ejo in zip(found_json_objects, expected_json_objects):
        assert fjo[0].get('id') is not None
        assert fjo[0].get('file_name') is not None
        assert fjo[0]['id'] == ejo[0]['id']
        assert fjo[0]['file_name'] == ejo[0]['file_name']


@pytest.mark.parametrize("file_date, expected_json_object", [
    ("2020-01-01T00:00:00", json_objects[0]),
    ("2021-01-01T00:00:00", json_objects[1]),
    ("2025-01-01T00:00:00", json_objects[5]),
    ("2026-01-01T00:00:00", json_objects[6])
])
def test_get_json_object(file_date: str, expected_json_object: Dict[str, Any]) -> None:
    # Arrange
    json_file_object_provider = JsonFileObjectProviderStub(file_names, json_objects)
    # Act
    found_json_object = json_file_object_provider.get_json_object(file_date)
    # Assert
    assert found_json_object[0].get('id') is not None
    assert found_json_object[0].get('file_name') is not None
    assert found_json_object[0]['id'] == expected_json_object[0]['id']
    assert found_json_object[0]['file_name'] == expected_json_object[0]['file_name']
