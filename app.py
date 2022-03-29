from flask import Flask, render_template, send_from_directory, request
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

	return render_template('index.html', posts=posts, comments_count=comments_count, bookmarks_count=len(bookmarks))


@app.route('/search')
def search():
	posts = load_json(POSTS)
	s = request.args.get('s')
	found_posts = search_for_post(posts, s)
	return render_template('search.html', s=s, found_posts=found_posts)




# @app.route("/uploads/<path:path>")
# def static_dir(path):
# 	return send_from_directory("uploads", path)


if __name__ == '__main__':
	app.run(debug=True)
