import webapp2
import pagehandler

app = webapp2.WSGIApplication([('/?', pagehandler.AllPostsPage),
							   ('/post/([0-9]+)', pagehandler.PostPage),
							   ('/newpost', pagehandler.NewPostPage),
							   ('/myposts', pagehandler.MyPostsPage),
							   ('/deletepost/([0-9]+)', pagehandler.DeletePost),
							   ('/deletecomment/([0-9]+)', pagehandler.DeleteComment),
							   ('/editcomment/([0-9]+)', pagehandler.EditCommentPage),
							   ('/newcomment/([0-9]+)', pagehandler.NewComment),
							   ('/like/([0-9]+)', pagehandler.LikeHanlder),
							   ('/editpost/([0-9]+)', pagehandler.EditPostPage),
							   ('/signup', pagehandler.Register),
							   ('/login', pagehandler.Login),
							   ('/logout', pagehandler.Logout)
							   ],
							  debug=True)