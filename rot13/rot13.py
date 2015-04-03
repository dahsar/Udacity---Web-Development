import cgi
import string
import webapp2
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

form = """
<b> <h1> Wattup yo....enter some text to do some fancy cryptography type stuff. </b> </h1>
<form method = "POST">
	<textarea name = "text">%(happy)s</textarea>
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


	def newin(self,index):
		if index + 13 > 25:
			diff = 26 - index - 1
			return 13 - diff - 1
		else:
			return index + 13

	def rot13(self,text):
		i = 0
		while i < len(text):
			if text[i] in string.ascii_lowercase:
				for x in range(0, 26):
					if text[i] == string.ascii_lowercase[x]:
						index = x
						break
				index = self.newin(index)
			#text[i] = string.ascii_lowercase[index] //illegal
				text = text[:i] + string.ascii_lowercase[index] + text[i+1:]
			
			if text[i] in string.ascii_uppercase:
				for x in range(0,26):
					if text[i] == string.ascii_uppercase[x]:
						index = x
						break
				index = self.newin(index)
			#text[i] = string.ascii_uppercase[index]
				text = text[:i] + string.ascii_uppercase[index] + text[i+1:] 
			i = i + 1	
		return text	


	def write_form(self, inputz = ""):
	#	self.response.out.write(form % {"happy" : inputz})
		self.render("form.html", happy = inputz)


	def get(self):
		self.write_form()
	
	def post(self):
		inputzz = self.request.get('text')
		inputzz = self.rot13(inputzz)
		inputzz = cgi.escape(inputzz, quote = True)
		self.write_form(inputzz)
# [END main_page]





application = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
