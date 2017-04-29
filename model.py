import random
import hashlib
from string import letters
from google.appengine.ext import db

def make_salt(length = 5):
	return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
	if not salt:
		salt = make_salt()
	h = hashlib.sha256(name + pw + salt).hexdigest()
	return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
	salt = h.split(',')[0]
	return h == make_pw_hash(name, password, salt)

class User(db.Model):
	"""Represents an user and his properties."""
	name = db.StringProperty(required = True)
	pw_hash = db.StringProperty(required = True)
	email = db.StringProperty()

	@classmethod
	def by_id(self, uid):
		return User.get_by_id(uid)

	@classmethod
	def by_name(self, name):
		u = User.all().filter('name =', name).get()
		return u

	@classmethod
	def register(self, name, pw, email = None):
		pw_hash = make_pw_hash(name, pw)
		return User(name = name,
					pw_hash = pw_hash,
					email = email)

	@classmethod
	def login(self, name, pw):
		u = self.by_name(name)
		if u and valid_pw(name, pw, u.pw_hash):
			return u

class Post(db.Model):
	"""Represents a post and his properties."""
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	last_modified = db.DateTimeProperty(auto_now = True)
	author = db.ReferenceProperty(User,
								   collection_name='posts', required=True)
	likes = db.ListProperty(long)

	def get_content(self):
		return self.content.replace('\n', '<br>')

	@classmethod
	def by_id(self, uid):
		return Post.get_by_id(uid)

	@classmethod
	def register(self, subject, content, author):
		return Post(subject = subject, content = content, author=author)

class Comment(db.Model):
	"""Represents a comment and his properties."""
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	author = db.ReferenceProperty(User, required=True)
	post = db.ReferenceProperty(Post, collection_name='comments', required=True)