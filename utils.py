# Windows-1251
# utf-8

import json
import logging


logging.basicConfig(level=logging.ERROR)


def load_json(path: str) -> list:
	"""Загружает данные из json-файла"""
	try:
		with open(path, encoding='utf-8') as file:
			return json.load(file)
	except FileNotFoundError:
		logging.error("Файл не найден")
		return None
	except json.JSONDecodeError:
		logging.error('Ошибка преобразования json-файла')
		return None


def get_post_by_user(data: list, text: str) -> list:
	"""Возвращает пост заданного пользователя"""
	return [elem for elem in data if text.lower() in elem.get('poster_name').lower()]


def get_comments_by_post(data: list, uid: int) -> list:
	"""Возвращает комментарии к заданному посту"""
	return [elem for elem in data if uid == elem.get('post_id')]


def search_for_post(data: list, query: str) -> list:
	"""Возвращает посты по ключевому слову"""
	return [elem for elem in data if query.lower() in elem.get('content').lower()]


def get_post_by_pk(data: list, pk: int) -> dict:
	"""Возвращает пост по идентификатору"""
	for elem in data:
		for v in elem.values():
			if pk == v:
				return elem
	return None


def get_comments_count(comments: list) -> dict:
	count = {}
	uids = set()
	for comment in comments:
		uids.add(comment.get('post_id'))

	for uid in list(uids):
		count[uid] = len(get_comments_by_post(comments, uid))
	
	return count


# comments = load_json('data/comments.json')
#
# print(get_comments_count(comments))
# input()





