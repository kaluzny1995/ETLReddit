import pytest
from typing import List

from model import Comment
from model.enum.e_file_date_type import EFileDateType
from test.provider.stub.supabase_postgres_comment_provider_stub import SupabasePostgresCommentProviderStub
from test.provider.supabase_postgres.fixtures_test_cases import comments as all_comments


@pytest.mark.parametrize("comments, expected_comments", [
    (all_comments, all_comments),
    ([all_comments[0], all_comments[3]], [all_comments[0], all_comments[3]])
])
def test_get_comments(comments: List[Comment], expected_comments: List[Comment]) -> None:
    # Arrange
    supabase_postgres_comment_provider = SupabasePostgresCommentProviderStub(comments)
    # Act
    returned_comments = supabase_postgres_comment_provider.get_comments(phrase="", file_dates=[], which=EFileDateType.START)
    # Assert
    assert len(returned_comments) == len(expected_comments)
    for rc, ec in zip(returned_comments, expected_comments):
        assert rc.comment_id == ec.comment_id
        assert rc.reddit_id == ec.reddit_id
        assert rc.parent_comment_id == ec.parent_comment_id
        assert rc.permalink == ec.permalink
        assert rc.phrase == ec.phrase
        assert rc.author == ec.author
        assert rc.body == ec.body
        assert rc.datetime_created == ec.datetime_created
        assert rc.datetime_created_utc == ec.datetime_created_utc
        assert rc.depth_level == ec.depth_level
        assert rc.controversiality == ec.controversiality
        assert rc.likes == ec.likes
        assert rc.ups == ec.ups
        assert rc.downs == ec.downs
        assert rc.score == ec.score
        assert rc.upvote_ratio == ec.upvote_ratio
        assert rc.gilded_number == ec.gilded_number
        assert rc.number_of_replies == ec.number_of_replies
        assert rc.start_file_date == ec.start_file_date
        assert rc.end_file_date == ec.end_file_date
