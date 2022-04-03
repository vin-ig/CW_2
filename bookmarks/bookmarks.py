from flask import Blueprint, render_template, request, redirect
from utils import load_json, get_post_by_id, write_json, get_tags_by_posts, get_comments_count
from config import POSTS, COMMENTS, BOOKMARKS

bookmarks = Blueprint('bookmarks', __name__, template_folder='templates')


@bookmarks.route('/bookmarks')
def all_bookmarks():
	"""Закладки"""
	posts = load_json(POSTS)
	comments = load_json(COMMENTS)
	bookmarks = load_json(BOOKMARKS)

	comments_count = get_comments_count(comments)
	tags = get_tags_by_posts(posts)

	return render_template('bookmarks.html', posts=bookmarks, comments_count=comments_count,
							bookmarks=bookmarks, tags=tags)


@bookmarks.route('/bookmark')
def bookmark():
	"""Добавление/удаление закладок"""
	posts = load_json(POSTS)
	bm = request.args.get('bm')  # Обрабатываем запрос при нажатии на кнопку закладки
	pos = bm.rfind('&')  # Разделяем два значения по разделителю &
	page, uid = bm[:pos], int(bm[pos + 1:])  # Страница, куда будет выполнен редирект; ID поста
	post = get_post_by_id(posts, uid)
	write_json(BOOKMARKS, post)  # Обновляем файл с закладками
	return redirect(page, code=302)
