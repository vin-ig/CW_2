import pytest
from utils import *

posts = load_json('./data/data.json')
comments = load_json('./data/comments.json')


# get_posts_by_user
def test_user_post():
    allowed_keys = {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "post_id"}
    user_posts = get_posts_by_user(posts, 'hank')
    assert len(user_posts) > 0, 'Empty list'
    for post in user_posts:
        assert set(post.keys()) == allowed_keys, 'Wrong keys'


# get_comments_by_post
def test_comments_by_post():
    allowed_keys = {"post_id", "commenter_name", "comment", "pk"}
    comm = get_comments_by_post(comments, 4)
    assert len(comm) > 0, 'Empty list'
    for post in comm:
        assert set(post.keys()) == allowed_keys, 'Wrong keys'


# search_for_post
def test_search_for_post():
    allowed_keys = {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "post_id"}
    found_posts = search_for_post(posts, 'елки')
    assert len(found_posts) > 0, 'Empty list'
    for post in found_posts:
        assert set(post.keys()) == allowed_keys, 'Wrong keys'


# get_post_by_id
def test_get_post_by_id():
    allowed_keys = {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "post_id"}
    post = get_post_by_id(posts, 3)
    assert set(post.keys()) == allowed_keys, 'Wrong keys'






