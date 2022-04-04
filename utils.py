import json
import logging


logging.basicConfig(level=logging.ERROR)


def load_json(path: str) -> list | str:
	"""Загружает данные из json-файла"""
	try:
		with open(path, encoding='utf-8') as file:
			return json.load(file)
	except FileNotFoundError:
		logging.error("Файл не найден")
		return 'ERROR'
	except json.JSONDecodeError:
		logging.error('Ошибка преобразования json-файла')
		return 'ERROR'


def get_posts_by_user(data: list, text: str) -> list:
	"""Возвращает посты заданного пользователя"""
	return [elem for elem in data if text.lower() == elem.get('poster_name').lower()]


def get_comments_by_post(data: list, uid: int) -> list:
	"""Возвращает комментарии к заданному посту"""
	return [elem for elem in data if uid == elem.get('post_id')]


def search_for_post(data: list, query: str) -> list:
	"""Возвращает посты по ключевому слову"""
	try:
		return [elem for elem in data if query.lower() in elem.get('content').lower()]
	except AttributeError:
		return []


def get_post_by_id(data: list, uid: int) -> dict | None:
	"""Возвращает пост по идентификатору"""
	for elem in data:
		if elem['post_id'] == uid:
			return elem
	return None


def get_comments_count(comments: list) -> dict:
	"""Возвращает количество комментариев к посту"""
	count = {}
	uids = set()
	for comment in comments:
		uids.add(comment.get('post_id'))
	for uid in list(uids):
		num = len(get_comments_by_post(comments, uid))
		count[uid] = f'{num} комментари{ending(num)}'  # Подбираем правильное окончание
	return count


def ending(k: int) -> str:
	"""Возвращает правильное окончание слова"""
	if 11 <= k % 100 <= 20:
		end = 'ев'
	elif k % 10 == 1:
		end = 'й'
	elif k % 10 in [2, 3, 4]:
		end = 'я'
	else:
		end = 'ев'
	return end


def get_tags_by_text(text: str) -> list:
	"""Возвращает список хештегов в тексте"""
	punctuation = (',', '.', '?', '!', '@', '', '*', '/', '-', '–')
	for elem in punctuation:
		text = text.replace(elem, '')  # Удаляем все знаки препинания
		text = text.replace('  ', ' ')  # Удаляем двойные пробелы
	tags = []
	for word in text.split(' '):
		if word[0] == '#':
			tags.append(word[1:])
	return tags


def get_tags_by_posts(data: list) -> dict:
	"""Возвращает список хештегов, относящихся к соответствующему посту"""
	tags = {}
	for elem in data:
		tags_by_text = get_tags_by_text(elem.get('content'))
		tags[elem.get('post_id')] = tags_by_text
	return tags


def create_tags(post: dict, tags: list):
	"""Превращает текстовые хештеги в активные ссылки"""
	for tag in tags:
		text = f'#{tag}'
		link = f'<a href="/tag/{tag}">#{tag}</a>'
		post['content'] = post.get('content').replace(text, link)


def write_json(path: str, update: dict):
	"""Обновляет json-файл"""
	with open(path, encoding='utf-8') as file:
		data = json.load(file)

	# Если данных нет в списке, то добавляем их, если есть - удаляем
	if update not in data:
		data.append(update)
	else:
		for elem in data:
			if elem == update:
				data.remove(elem)

	with open(path, 'w', encoding='utf-8') as file:
		json.dump(data, file, indent=2, ensure_ascii=False)
