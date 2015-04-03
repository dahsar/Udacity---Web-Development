import cgi
import string
import webapp2
import re

import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)




form2 = """
<b> <h1> Wattup yo....ok this time im having yall sign up to this wack website </b> </h1>
<form method = "POST">
<label>
Username:	<input type = "text" name = "username" value = "%(up)s">  <b style = "color : red"> %(usererr)s </b>
</label> 
<br>
<label> Password:
	<input type = "password" name = "password"> <b style = "color : red">%(passerr)s </b>
</label>
<br>
<label> 
Verify password: <input type = "password" name = "verify"> <b style = "color : red">%(matchoo)s </b>
</label>
<br>
<label> Email (Optional): 
<input type = "text" name = "email" value = "%(ep)s"> <b style = "color : red"> %(mailerr)s </b>
</label>
<br>
<input type = "submit">
</form>"""

form = """
<b> <h1> Wattup yo....ok this time im having yall sign up to this wack website </b> </h1>
<form method = "POST">
	<textarea name = "text">%(happy)s</textarea>
	<input type = "submit">
</form>
 """
usah = "" 
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EM_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def validuser(text):
	#print USER_RE.match(text)
	if USER_RE.match(text) and text != "":
		return True
	else:
		return False	

def validpass(text):
	#print PASS_RE.match(text)
	if PASS_RE.match(text) and text != "":
		return True
	else:
		return False

def validemail(text):
	#print EM_RE.match(text)
	if EM_RE.match(text) or text == "":
		return True
	else:
		return False

def validmatch(text1,text2):
	if text1 == text2:
		return True
	else:
		return False

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a,**kw)

	def render_str(self,template,**params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template,**kw))



class MainPage(Handler):
	user = False
	passs = False
	match = False
	email = True
	uerr = ""
	perr = ""
	eerr = ""
	matcho = ""
	userstuff = ""
	passstuff = ""
	verstuff = ""
	emstuff = ""

	def write_form(self, uerr = "", perr = "", eerr = "", matcho = "", u = "", p = ""):
		#self.response.out.write(form2 % { "usererr" : uerr, "passerr" : perr, "mailerr" : eerr, "matchoo" : matcho, "up": u, "ep" : p})
		self.render("form.html",usererr = uerr, passerr = perr, mailerr = eerr, matchoo = matcho, up = u, ep = p)
	def isitvalid(self):
		self.userstuff = cgi.escape(self.request.get('username'), quote = True)
		usah = self.userstuff
		#print usah
		self.passstuff = cgi.escape(self.request.get('password'),quote = True)
		self.verstuff = cgi.escape(self.request.get('verify'),quote = True)
		self.emstuff = cgi.escape(self.request.get('email'),quote = True)
	#	print userstuff
	#	print passstuff
	#	print verstuff
	#	print emstuff
		self.user = validuser(self.userstuff)
		self.passs = validpass(self.passstuff)
		self.match = validmatch(self.verstuff,self.passstuff)
		self.email = validemail(self.emstuff)
	#	print self.user
	#	print self.passs
	#	print self.match
	#	print self.email	
			
	def get(self):
		self.write_form()
	
	def post(self):
		#inputzz = self.request.get('text')
		#inputzz = self.rot13(inputzz)
		#inputzz = cgi.escape(inputzz, quote = True)
		#self.write_form(inputzz)
		self.isitvalid()
		if not(self.user):
			self.uerr = "That's not a valid username."
		if not(self.passs):
			self.perr = "That wasn't a valid password."

		if not(self.match):
			self.matcho = "Your passwords didn't match."
	
		if not(self.email):
			self.eerr = "That's not a valid email." 
		if self.user and self.passs and self.match and self.email:
			self.redirect('/valid?name=' + self.userstuff)
		else:
			self.write_form(self.uerr,self.perr,self.eerr,self.matcho, self.userstuff,self.emstuff)
# [END main_page]

class validhandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("<h1> Welcome, %s! You all signed up. For what, I have no fucking clue." % self.request.get('name') )

application = webapp2.WSGIApplication([
    ('/', MainPage), ('/valid', validhandler)
], debug=True)
