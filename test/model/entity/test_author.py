import pytest
from typing import Dict, Any

from model import Author

from test.model.entity.fixtures_test_cases import test_author_from_raw_json_cases


@pytest.mark.parametrize("json_object, expected_author", test_author_from_raw_json_cases)
def test_from_raw_json(json_object: Dict[str, Any], expected_author: Author) -> None:
    # Arrange
    # Act
    author = Author.from_raw_json(json_object)

    # Assert
    assert author.name == expected_author.name
    assert author.background_color == expected_author.background_color
    assert author.css_class == expected_author.css_class
    assert author.richtext == expected_author.richtext
    assert author.template_id == expected_author.template_id
    assert author.text == expected_author.text
    assert author.text_color == expected_author.text_color
    assert author.type == expected_author.type
    assert author.fullname == expected_author.fullname
    assert author.is_blocked == expected_author.is_blocked
    assert author.is_patreon_flair == expected_author.is_patreon_flair
    assert author.is_premium == expected_author.is_premium
    assert author.datetime_created == expected_author.datetime_created
    assert author.datetime_created_utc == expected_author.datetime_created_utc
    assert author.permalink == expected_author.permalink
