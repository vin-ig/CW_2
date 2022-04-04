import pytest
from utils import *

posts = load_json('./data/data.json')
comments = load_json('./data/comments.json')

post_by_user = [
    (posts, 'LaRrY', [posts[3], posts[7]]),
    (posts, 'ghfd', [])
]

comments_by_post = [
    (comments, 5, [comments[16], comments[17]]),
    (comments, 45, []),
    (comments, 2, [comments[4], comments[5], comments[6], comments[7]]),
    (comments, '1', [])
]

search_post = [
    (posts, 'ТАреЛКа', [posts[0]]),
    (posts, 'ЗАКАТ', [posts[6]]),
    (posts, 'абырвалг', []),
    (posts, 'кот', [posts[1], posts[4], posts[5], posts[7]]),
]

post_by_id = [
    (posts, 4, posts[3]),
    (posts, 8, posts[7]),
    (posts, 43, None),
    (posts, '3', None),
]


# get_posts_by_user
@pytest.mark.parametrize('first, second, expected', post_by_user)
def test_user_post(first, second, expected):
    assert get_posts_by_user(first, second) == expected


# get_comments_by_post
@pytest.mark.parametrize('first, second, expected', comments_by_post)
def test_search_comment(first, second, expected):
    assert get_comments_by_post(first, second) == expected


# search_for_post
@pytest.mark.parametrize('first, second, expected', search_post)
def test_search_for_post(first, second, expected):
    assert search_for_post(first, second) == expected


# get_post_by_id
@pytest.mark.parametrize('first, second, expected', post_by_id)
def test_get_post_by_pk(first, second, expected):
    assert get_post_by_id(first, second) == expected
