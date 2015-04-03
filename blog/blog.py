import webapp2
import jinja2
import os
import string
from google.appengine.ext import db
template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class postit(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a,**kw)

	def render_str(self,template,**params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template,**kw))


class MainPage(Handler):
    def get(self):
     #   self.response.headers['Content-Type'] = 'text/plain'
	
	posts = db.GqlQuery("SELECT * from postit ORDER BY created DESC")
	self.render("front.html", posts = posts)

#class TestHandler(Handler):
#	def post(self):
 #    		q = self.request.get("q")
#		self.response.out.write(q)
#		self.response.headers['Content-Type'] = 'text/plain'
#		self.write(self.request)

#	def get(self):
#		self.write("Hello, world!")


class NewPostHandler(Handler):


	def write_form(self, sp = "", cp = "", postErr = ""):
		#self.response.out.write(form2 % { "usererr" : uerr, "passerr" : perr, "mailerr" : eerr, "matchoo" : matcho, "up": u, "ep" : p})
		self.render("postform.html",sp = sp, cp = cp, postErr = postErr)


	def get(self):
		self.write_form()

	def post(self):
		posterr = "Nigga, can you read? Subject and body, please."
		content = self.request.get('content')
		subject = self.request.get('subject')
		print content
		print subject
		if content and subject:
			#generate permalink, then go to it
			#self.redirect('/valid?name=' + self.userstuff)
			print content
			print subject
			print 2
			p = postit(subject = subject, content = content)
			
			p.put()
			
			theid = str(p.key().id())
			print type(theid)
			print theid
			self.redirect('/' + theid)
			#put permalink here
		else:
			self.write_form(subject, content, posterr)


class PermaHandler(Handler):
	def get(self,the_id):
					
		#posts = db.GqlQuery("SELECT * from postit ORDER BY created DESC")
		posts = postit.get_by_id(int(the_id))
		self.render("perma.html", posts = posts)


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/newpost', NewPostHandler),
    (r'/(\d+)', PermaHandler)
], debug=True)

