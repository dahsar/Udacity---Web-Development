import webapp2
import jinja2
import os
template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

form2 = """
	<form method = "get" action = "/testform">
	<input name = "q">
	<input type = "submit">
</form>
"""


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
	self.render("form.html",name = self.request.get('name'))

class TestHandler(Handler):
	def post(self):
 #    		q = self.request.get("q")
#		self.response.out.write(q)
		self.response.headers['Content-Type'] = 'text/plain'
		self.write(self.request)

	def get(self):
		self.write("Hello, world!")


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/testform', TestHandler)
], debug=True)
