class Post:
	def __init__(self, data):
		self.poster_name = data.get('poster_name')
		self.poster_avatar = data.get('poster_avatar')
		self.pic = data.get('pic')
		self.content = data.get('content')
		self.views_count = data.get('views_count')
		self.likes_count = data.get('likes_count')
		self.pk = data.get('pk')

	def get_user_post(self, name):
		


























