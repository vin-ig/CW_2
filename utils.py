# Исправить тайп-хинты
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


def get_post_by_id(data: list, uid: int) -> dict:
	"""Возвращает пост по идентификатору"""
	for elem in data:
		if elem['post_id'] == uid:
			return elem
	return None


def get_comments_count(comments: list) -> dict:
	count = {}
	uids = set()
	for comment in comments:
		uids.add(comment.get('post_id'))
	for uid in list(uids):
		num = len(get_comments_by_post(comments, uid))
		count[uid] = f'{num} комментари{ending(num)}'
	return count


def ending(k):
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
	punktuation = (',', '.', '?', '!', '@', '', '*', '/', '-', '–')
	for elem in punktuation:
		text = text.replace(elem, '')
		text = text.replace('  ', ' ')
	tags = []
	for word in text.split(' '):
		if word[0] == '#':
			tags.append(word[1:])
	return tags


def get_tags_by_posts(data: list) -> dict:
	tags = {}
	for elem in data:
		tags_by_text = get_tags_by_text(elem.get('content'))
		tags[elem.get('post_id')] = tags_by_text
	return tags


def create_tags(post: dict, tags: list) -> dict:
	for tag in tags:
		text = f'#{tag}'
		link = f'<a href="/tag/{tag}">#{tag}</a>'
		post['content'] = post.get('content').replace(text, link)


def write_json(path: str, update: dict):
	with open(path, encoding='utf-8') as file:
		data = json.load(file)
	
	if update not in data:
		data.append(update)
	else:
		for elem in data:
			if elem == update:
				data.remove(elem)

	with open(path, 'w', encoding='utf-8') as file:
		json.dump(data, file, indent=2, ensure_ascii=False)






# bm = 'd:/temp/coursework 2/3_cw_2/data/bookmarks.json'
# data = load_json('d:/temp/coursework 2/3_cw_2/data/data.json')
# # tags = get_tags_by_text(post.get('content'))

# for i in range(0, len(data), 3):
	# post = data[i]
	# write_json(bm, post)


# posts = load_json('data/data.json')
# post = posts[0]
# tags = get_tags_by_posts(posts)
# print(tags)
# input()
