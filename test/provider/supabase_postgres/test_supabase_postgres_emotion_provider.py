import pytest
from typing import List

from model import Emotion
from test.provider.stub.supabase_postgres_emotion_provider_stub import SupabasePostgresEmotionProviderStub
from test.provider.supabase_postgres.fixtures_test_cases import emotions as all_emotions


@pytest.mark.parametrize("emotions, expected_file_dates", [
    (all_emotions, ["2026-01-01", "2022-01-01", "2022-01-01", "2026-01-01"]),
    ([all_emotions[0], all_emotions[3]], ["2026-01-01", "2026-01-01"])
])
def test_get_file_dates(emotions: List[Emotion], expected_file_dates: List[str]) -> None:
    # Arrange
    supabase_postgres_emotion_provider = SupabasePostgresEmotionProviderStub(emotions)
    # Act
    file_dates = supabase_postgres_emotion_provider.get_file_dates(phrase="")
    # Assert
    assert len(file_dates) == len(expected_file_dates)
    for fd, efd in zip(file_dates, expected_file_dates):
        assert fd == efd


@pytest.mark.parametrize("emotions, expected_emotions", [
    (all_emotions, all_emotions),
    ([all_emotions[0], all_emotions[3]], [all_emotions[0], all_emotions[3]])
])
def test_get_sentiments(emotions: List[Emotion], expected_emotions: List[Emotion]) -> None:
    # Arrange
    supabase_postgres_emotion_provider = SupabasePostgresEmotionProviderStub(emotions)
    # Act
    returned_emotions = supabase_postgres_emotion_provider.get_emotions(phrase="")
    # Assert
    assert len(returned_emotions) == len(expected_emotions)
    for rp, ep in zip(returned_emotions, expected_emotions):
        assert rp.reddit_id == ep.reddit_id
        assert rp.comment_id == ep.comment_id
        assert rp.phrase == ep.phrase
        assert rp.num_happy == ep.num_happy
        assert rp.num_angry == ep.num_angry
        assert rp.num_surprise == ep.num_surprise
        assert rp.num_sad == ep.num_sad
        assert rp.num_fear == ep.num_fear
        assert rp.total_words == ep.total_words
        assert rp.emotion_classes == ep.emotion_classes
        assert rp.file_date == ep.file_date
