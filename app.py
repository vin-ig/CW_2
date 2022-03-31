from flask import Flask, render_template, request
from utils import *

POSTS = 'data/data.json'
COMMENTS = 'data/comments.json'
BOOKMARKS = 'data/bookmarks.json'

app = Flask(__name__)


@app.route('/')
def index():
	posts = load_json(POSTS)
	comments = load_json(COMMENTS)
	bookmarks = load_json(BOOKMARKS)

	if not posts or not comments:
		return render_template('error.html', message='Ошибка загрузки данных')

	comments_count = get_comments_count(comments)
	tags = get_tags_by_posts(posts)

	return render_template('index.html', posts=posts, comments_count=comments_count,
							bookmarks_count=len(bookmarks), tags=tags)


@app.route('/post/<int:uid>')
def post(uid):
	posts = load_json(POSTS)
	comments = load_json(COMMENTS)
	post = get_post_by_id(posts, uid)

	# write_json(POSTS, post)
	# post['views_count'] += 1
	# write_json(POSTS, post)

	comments_by_post = get_comments_by_post(comments, uid)
	tags = get_tags_by_text(post.get('content'))
	comments_count = get_comments_count(comments)
	create_tags(post, tags)
	if post:
		return render_template('post.html', post=post, comments_count=comments_count,
								comments=comments_by_post, tags=tags)
	else:
		return render_template('error.html', message='Пост не найден')


@app.route('/search')
def search():
	posts = load_json(POSTS)
	tags = get_tags_by_posts(posts)
	s = request.args.get('s')
	found_posts = search_for_post(posts, s)
	return render_template('search.html', s=s, tags=tags, found_posts=found_posts)


@app.route('/user/<name>')
def user(name):
	posts = load_json(POSTS)
	user_posts = get_posts_by_user(posts, name)
	tags = get_tags_by_posts(posts)
	return render_template('user-feed.html', posts=user_posts, tags=tags)


@app.route('/tag/<tag>')
def hashtag(tag):
	posts = load_json(POSTS)
	tags = get_tags_by_posts(posts)
	posts_by_tag = []
	for uid, post_tags in tags.items():
		if tag in post_tags:
			posts_by_tag.append(get_post_by_id(posts, uid))
	return render_template('tag.html', posts=posts_by_tag, tags=tags, tag=tag)


@app.route('/bookmarks')
def bookmarks():
	bookmarks = load_json(BOOKMARKS)
	return render_template('bookmarks.html', posts=bookmarks)


if __name__ == '__main__':
	app.run(debug=True)
