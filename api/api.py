from flask import Blueprint, jsonify
from utils import load_json,get_post_by_id
from config import POSTS

api = Blueprint('api', __name__)


@api.route('/api/posts')
def api_posts():
	"""Вывод всех постов в формате JSON"""
	posts = load_json(POSTS)
	return jsonify(posts)


@api.route('/api/post/<int:uid>')
def api_post(uid):
	"""Вывод одного поста в формате JSON"""
	posts = load_json(POSTS)
	post = get_post_by_id(posts, uid)
	return jsonify(post)
