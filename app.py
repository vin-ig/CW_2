from flask import Flask, render_template, request
from utils import *
from api.api import api
from bookmarks.bookmarks import bookmarks

app = Flask(__name__)

# Blueprint для закладок
app.register_blueprint(bookmarks)
# Blueprint для API
app.register_blueprint(api)

app.config.from_pyfile('config.py')

POSTS = app.config.get('POSTS')
COMMENTS = app.config.get('COMMENTS')
BOOKMARKS = app.config.get('BOOKMARKS')


@app.route('/')
def index():
	"""Главная страница"""
	posts = load_json(POSTS)
	comments = load_json(COMMENTS)
	bookmarks = load_json(BOOKMARKS)
	if posts == 'ERROR' or comments == 'ERROR' or bookmarks == 'ERROR':
		return render_template('error.html', message='Ошибка загрузки данных')

	comments_count = get_comments_count(comments)  # Количество комментариев
	tags = get_tags_by_posts(posts)  # Список тегов перед постом

	return render_template('index.html', posts=posts, comments_count=comments_count,
							bookmarks=bookmarks, tags=tags)


@app.route('/post/<int:uid>')
def post(uid):
	"""Страница с отдельным постом"""
	posts = load_json(POSTS)
	comments = load_json(COMMENTS)
	bookmarks = load_json(BOOKMARKS)
	if posts == 'ERROR' or comments == 'ERROR' or bookmarks == 'ERROR':
		return render_template('error.html', message='Ошибка загрузки данных')

	post = get_post_by_id(posts, uid)  # Находим пост по ID
	if not post:
		return render_template('error.html', message='Пост не найден')

	bookmark = post in bookmarks  # Необходимо для корректного отображения иконки закладки
	comments_by_post = get_comments_by_post(comments, uid)  # Загружаем комментарии к посту
	tags = get_tags_by_text(post.get('content'))  # Ищем хештеги в тексте поста
	comments_count = get_comments_count(comments)  # Количество комментариев
	create_tags(post, tags)  # Превращаем текстовые хештеги в активные ссылки
	return render_template('post.html', post=post, comments_count=comments_count,
							comments=comments_by_post, tags=tags, bookmark=bookmark)


@app.route('/search')
def search():
	"""Страница поиска"""
	posts = load_json(POSTS)
	comments = load_json(COMMENTS)
	bookmarks = load_json(BOOKMARKS)
	if posts == 'ERROR' or comments == 'ERROR' or bookmarks == 'ERROR':
		return render_template('error.html', message='Ошибка загрузки данных')

	comments_count = get_comments_count(comments)
	tags = get_tags_by_posts(posts)
	s = request.args.get('s')
	found_posts = search_for_post(posts, s)
	return render_template('search.html', s=s, comments_count=comments_count,
							bookmarks=bookmarks, tags=tags, posts=found_posts)


@app.route('/user/<name>')
def user(name):
	"""Страница со всеми постами одного пользователя"""
	posts = load_json(POSTS)
	comments = load_json(COMMENTS)
	bookmarks = load_json(BOOKMARKS)
	if posts == 'ERROR' or comments == 'ERROR' or bookmarks == 'ERROR':
		return render_template('error.html', message='Ошибка загрузки данных')

	user_posts = get_posts_by_user(posts, name)
	if not user_posts:
		return render_template('error.html', message='Пользователь не найден')

	comments_count = get_comments_count(comments)
	tags = get_tags_by_posts(user_posts)
	return render_template('user-feed.html', posts=user_posts, tags=tags,
							bookmarks=bookmarks, comments_count=comments_count)


@app.route('/tag/<tag>')
def hashtag(tag):
	"""Страница с постами по хештегу"""
	posts = load_json(POSTS)
	comments = load_json(COMMENTS)
	bookmarks = load_json(BOOKMARKS)
	if posts == 'ERROR' or comments == 'ERROR' or bookmarks == 'ERROR':
		return render_template('error.html', message='Ошибка загрузки данных')

	tags = get_tags_by_posts(posts)
	comments_count = get_comments_count(comments)
	posts_by_tag = []
	for uid, post_tags in tags.items():
		if tag in post_tags:
			posts_by_tag.append(get_post_by_id(posts, uid))

	if not posts_by_tag:
		return render_template('error.html', message='Теги не найдены')

	return render_template('tag.html', posts=posts_by_tag, tags=tags, tag=tag,
							comments_count=comments_count, bookmarks=bookmarks)


@app.errorhandler(404)
def not_found_error(error):
	return render_template('error.html', message='Упс! Такой странички у нас нет(('), 404


if __name__ == '__main__':
	app.run()
