from flask import Flask, render_template, request, redirect, jsonify
from utils import *

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['JSON_AS_ASCII'] = False

POSTS = app.config.get('POSTS')
COMMENTS = app.config.get('COMMENTS')
BOOKMARKS = app.config.get('BOOKMARKS')


@app.route('/')
def index():
	"""Главная страница"""
	posts = load_json(POSTS)
	comments = load_json(COMMENTS)
	bookmarks = load_json(BOOKMARKS)

	if not posts or not comments:
		return render_template('error.html', message='Ошибка загрузки данных')

	comments_count = get_comments_count(comments)
	tags = get_tags_by_posts(posts)

	return render_template('index.html', posts=posts, comments_count=comments_count,
							bookmarks=bookmarks, tags=tags)


@app.route('/post/<int:uid>')
def post(uid):
	posts = load_json(POSTS)
	comments = load_json(COMMENTS)
	bookmarks = load_json(BOOKMARKS)
	post = get_post_by_id(posts, uid)
	bookmark = post in bookmarks
	comments_by_post = get_comments_by_post(comments, uid)
	tags = get_tags_by_text(post.get('content'))
	comments_count = get_comments_count(comments)
	create_tags(post, tags)
	if post:
		return render_template('post.html', post=post, comments_count=comments_count,
								comments=comments_by_post, tags=tags, bookmark=bookmark)
	else:
		return render_template('error.html', message='Пост не найден')


@app.route('/search')
def search():
	posts = load_json(POSTS)
	comments = load_json(COMMENTS)
	bookmarks = load_json(BOOKMARKS)
	comments_count = get_comments_count(comments)
	tags = get_tags_by_posts(posts)
	s = request.args.get('s')
	found_posts = search_for_post(posts, s)
	return render_template('search.html', s=s, comments_count=comments_count,
							bookmarks=bookmarks, tags=tags, posts=found_posts)


@app.route('/user/<name>')
def user(name):
	posts = load_json(POSTS)
	comments = load_json(COMMENTS)
	bookmarks = load_json(BOOKMARKS)
	comments_count = get_comments_count(comments)
	user_posts = get_posts_by_user(posts, name)
	tags = get_tags_by_posts(user_posts)

	return render_template('user-feed.html', posts=user_posts, tags=tags,
							bookmarks=bookmarks, comments_count=comments_count)


@app.route('/tag/<tag>')
def hashtag(tag):
	posts = load_json(POSTS)
	comments = load_json(COMMENTS)
	bookmarks = load_json(BOOKMARKS)
	comments_count = get_comments_count(comments)
	tags = get_tags_by_posts(posts)
	posts_by_tag = []
	for uid, post_tags in tags.items():
		if tag in post_tags:
			posts_by_tag.append(get_post_by_id(posts, uid))
	return render_template('tag.html', posts=posts_by_tag, tags=tags, tag=tag,
							comments_count=comments_count, bookmarks=bookmarks)


@app.route('/bookmarks')
def bookmarks():
	posts = load_json(POSTS)
	comments = load_json(COMMENTS)
	bookmarks = load_json(BOOKMARKS)
	comments_count = get_comments_count(comments)
	tags = get_tags_by_posts(posts)

	return render_template('bookmarks.html', posts=bookmarks, comments_count=comments_count,
							bookmarks=bookmarks, tags=tags)


@app.route('/bookmark')
def bookmark():
	bm = request.args.get('bm')
	pos = bm.rfind('&')
	page, uid = bm[:pos], int(bm[pos + 1:])
	posts = load_json(POSTS)
	post = get_post_by_id(posts, uid)
	write_json(BOOKMARKS, post)
	return redirect(page, code=302)


@app.route('/api/posts')
def api_posts():
	posts = load_json(POSTS)
	return jsonify(posts)


@app.route('/api/post/<int:uid>')
def api_post(uid):
	posts = load_json(POSTS)
	post = get_post_by_id(posts, uid)
	return jsonify(post)


if __name__ == '__main__':
	app.run(debug=app.config.get('DEBUG'))
