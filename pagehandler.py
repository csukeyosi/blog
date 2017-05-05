import re
import model
import time
from bloghandler import BlogHandler

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
	return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

def valid_email(email):
	return not email or EMAIL_RE.match(email)

class AllPostsPage(BlogHandler):
	"""Responsible for showing all posts"""
	def get(self):
		posts = model.Post.all().order("-created");
		self.render(False, 'list-posts.html', posts = posts)

class DeletePost(BlogHandler):
	"""Responsible for deleting the post"""
	def post(self, post_id):
		if not self.user:
			self.redirect('/login')
			return

		#check post
		post = model.Post.by_id(long(post_id))
		if not post:
			self.error(404)
			return

		#check author
		is_author = post.author.key().id() == self.user.key().id()
		if not is_author:
			self.error(401)
			return

		post.delete()

		# reloads the page
		time.sleep(0.1)

		self.redirect('/')

class NewComment(BlogHandler):
	"""Responsible for creating a new comment in the post"""
	def post(self, post_id):
		if not self.user:
			self.redirect('/login')
			return

		#check post
		post = model.Post.by_id(long(post_id))
		if not post:
			self.error(404)
			return

		#check author
		is_author = post.author.key().id() == self.user.key().id()

		content = self.request.get('content')
		if content:
			comment = model.Comment(content = content, author=self.user,
				post=post)
			comment.put()
			# reloads the page
			time.sleep(0.1)

		self.redirect(self.request.referer)

class DeleteComment(BlogHandler):
	"""Responsible for deleting the comment"""
	def post(self, comment_id):
		if not self.user:
			self.redirect('/login')
			return

		#check comment
		comment = model.Comment.by_id(long(comment_id))
		if not comment:
			self.error(404)
			return

		#check author
		is_author = comment.author.key().id() == self.user.key().id()
		if not is_author:
			self.error(401)
			return

		comment.delete()

		# reloads the page
		time.sleep(0.1)

		self.redirect(self.request.referer)

class EditCommentPage(BlogHandler):
	"""Responsible for showing/handling the post edit page and post edit form"""
	def get(self, comment_id):
		if not self.user:
			self.redirect('/login')
			return

		#check comment
		comment = model.Comment.by_id(long(comment_id))
		if not comment:
			self.error(404)
			return

		#check author
		is_author = comment.author.key().id() == self.user.key().id()
		if not is_author:
			self.error(401)
			return

		self.render(True, "comment-form.html", content=comment.content)

	def post(self, comment_id):
		if not self.user:
			self.redirect('/login')
			return

		content = self.request.get('content')
		if content:
			#check comment
			comment = model.Comment.by_id(long(comment_id))
			if not comment:
				self.error(404)
				return

			#check author
			is_author = comment.author.key().id() == self.user.key().id()
			if not is_author:
				self.error(401)
				return

			comment.content = content
			comment.put()

			# reloads the page
			time.sleep(0.1)

			self.redirect('/post/%s' % str(comment.post.key().id()))
		else:
			error = "Content, please!"
			self.render(True, "comment-form.html", error=error)


class MyPostsPage(BlogHandler):
	"""Responsible for showing the myposts page"""
	def get(self):
		if not self.user:
			self.redirect('/login')
			return

		self.render(True, 'list-posts.html', posts = self.user.posts)

class PostPage(BlogHandler):
	"""Responsible for showing the post page"""
	def get(self, post_id):
		#check post
		post = model.Post.by_id(long(post_id))
		if not post:
			self.error(404)
			return

		is_author = self.user and (post.author.key().id() == self.user.key().id())
		has_liked = self.user and (self.user.key().id() in post.likes)
		comments = post.comments.order("-created")

		self.render(False, "list-posts.html", is_author = is_author,
			has_liked = has_liked, comments= comments, posts = [post],
			is_post_page = True)

class NewPostPage(BlogHandler):
	"""Responsible for showing/handling the new post page and new post form"""
	def get(self):
		self.render(True, "post-form.html", is_creation= True)

	def post(self):
		if not self.user:
			self.redirect('/login')
			return

		subject = self.request.get('subject')
		content = self.request.get('content')

		if subject and content:
			p = model.Post.register(subject = subject, content = content,
				author= self.user)
			p.put()
			self.redirect('/post/%s' % str(p.key().id()))
		else:
			error = "Subject and content, please!"
			self.render(True, "post-form.html", is_creation= True,
				subject=subject, content=content, error=error)

class EditPostPage(BlogHandler):
	"""Responsible for showing/handling the post edit page and post edit form"""
	def get(self, post_id):
		if not self.user:
			self.redirect('/login')
			return

		#check post
		post = model.Post.by_id(long(post_id))
		if not post:
			self.error(404)
			return

		#check author
		is_author = post.author.key().id() == self.user.key().id()
		if not is_author:
			self.error(401)
			return

		self.render(True, "post-form.html", is_creation= False,
			post_id=post.subject, subject=post.subject, content=post.content)

	def post(self, post_id):
		if not self.user:
			self.redirect('/login')
			return

		subject = self.request.get('subject')
		content = self.request.get('content')
		if subject and content:
			#check post
			post = model.Post.by_id(long(post_id))
			if not post:
				self.error(404)
				return

			#check author
			is_author = post.author.key().id() == self.user.key().id()
			if not is_author:
				self.error(401)
				return

			post.subject = subject
			post.content = content
			post.put()

			self.redirect('/post/%s' % str(post_id))
		else:
			error = "Subject and content, please!"
			self.render(True, "post-form.html", is_creation= False,
				subject=subject, content=content, error=error)

class LikeHanlder(BlogHandler):
	"""Responsible for the like/unlike action"""
	def post(self, post_id):
		if not self.user:
			self.redirect('/login')
			return

		#check post
		post = model.Post.by_id(long(post_id))
		if not post:
			self.error(404)
			return

		if self.user.key().id() in post.likes:
			post.likes.remove(self.user.key().id())
		else:
			post.likes.append(self.user.key().id())

		post.put()
		self.redirect('/post/%s' % str(post_id))

class Signup(BlogHandler):
	"""Responsible for showing/handling the signup form"""
	def get(self):
		self.render(False, "signup-form.html")

	def post(self):
		have_error = False
		self.username = self.request.get('username')
		self.password = self.request.get('password')
		self.verify = self.request.get('verify')
		self.email = self.request.get('email')

		params = dict(username = self.username,
					  email = self.email)

		if not valid_username(self.username):
			params['error_username'] = "That's not a valid username."
			have_error = True

		if not valid_password(self.password):
			params['error_password'] = "That wasn't a valid password."
			have_error = True
		elif self.password != self.verify:
			params['error_verify'] = "Your passwords didn't match."
			have_error = True

		if not valid_email(self.email):
			params['error_email'] = "That's not a valid email."
			have_error = True

		if have_error:
			self.render(False, 'signup-form.html', **params)
		else:
			self.done()

	def done(self, *a, **kw):
		raise NotImplementedError

class Login(BlogHandler):
	"""Responsible for showing/handling the login form and doing the login"""
	def get(self):
		self.render(False, 'login-form.html')

	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')

		u = model.User.login(username, password)
		if u:
			self.login(u)
			self.redirect('/')
		else:
			msg = 'Invalid login.'
			self.render(False, 'login-form.html', error = msg)

class Register(Signup):
	"""Responsible for creating a new user"""
	def done(self):
		#make sure the user doesn't already exist
		u = model.User.by_name(self.username)
		if u:
			msg = 'That user already exists.'
			self.render(False, 'signup-form.html', error_username = msg)
		else:
			u = model.User.register(self.username, self.password, self.email)
			u.put()

			self.login(u)
			self.redirect('/')

class Logout(BlogHandler):
	"""Responsible for logging out an user"""
	def get(self):
		self.logout()
		self.redirect('/login')