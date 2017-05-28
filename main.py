#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import sessions
import session_module

inicio='''<!DOCTYPE html>
<html><head>
<meta name="tipo_contenido" content="text/html;" http-equiv="content-type" charset="utf-8"/>
<title>Inicio</title>
</head>
<body>
<a href="/Registro">Registro</a><br/>
<a href="/Login">Login</a><br/>
<a href="/VerPreguntas">Ver Preguntas</a><br/>
<a href="/AnadirPreguntas">Anadir Preguntas</a>
</body></html>
'''

login_form='''<html>

<head>
<meta name="tipo_contenido" content="text/html;" http-equiv="content-type" charset="utf-8"/>
<title>Login</title>
</head>

<body>
	<center>
	<h1>Login</h1>
	<form method="post" enctype="multipart/form-data">

	<table border="0">
	<tr>
		<td>Introduce el usuario: </td>
		<td><input type='text' name='usuario' id='usuario' required value='%(email)s'/><td>
	</tr>
	<tr>
		<td>Introduce la contrasena</td>
		<td><input type='password' name='contrasena' id='contrasena' required value='%(password)s'/></td>
	</tr>
	<tr><td></td>
		<td align="right"><input type="submit" name='login' id='login' value="Iniciar Sesion"/></td>
	</tr>
	</table>
	</form>
	</center>
</body>
</html>'''

signup_form='''<html>  <head>    <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
    <title>Introduzca sus datos:</title>    <style type="text/css">      
	.label {text-align: right}      .error {color: red}    </style>  
</head>   <body>  <h1>Registro</h1>    <h2>Rellene los campos por favor:</h2>    
<form method="post">
<table>        <tr>          <td class="label">
            Nombre de usuario
			</td>
			<td>
            <input type="text" name="username" value="" placeholder="Tu nombre...">          </td>          <td class="error">
</td>        </tr>         <tr>          <td class="label">            Password          
</td>          <td>            <input type="password" name="password" value="" autocomplete="off">          </td>          <td class="error">            
</td>                       </td>        
</tr>         <tr>          <td class="label">            Repetir Password          </td>          
<td>            <input type="password" name="verify" value="" placeholder="El mismo de antes">          </td>          <td class="error">                      </td>        </tr>         <tr>          <td class="label">            
Email          </td>          <td>            <input type="text" name="email" value="">          </td>          <td class="error">                      </td>        </tr>      </table>       <input type="submit">    </form>  </body> </html>'''

anadirPregunta_form= '''<html>

	<head>
	<title>Anadir Pregunta</title>
	
	</head>

	<body>
	<center>
	<h1>Anadir Pregunta</h1>
	<form method="post">
	<table>
	
	<tr>
	<td>Pregunta:</td>
	<td><input type="text" name='Nombre' id='Nombre' required value=""/></td>
	</tr>
	<tr>
	<td>Categoria:</td>
	<td><input type="text" name='Categoria' id='Categoria' required value=""/></td>
	</tr>
	<tr>
	<td>Respuesta:</td>
	<td><input type="text" name='Respuesta' id='Respuesta' required value=""/></td>
	</tr>
	<tr>
	<td>Dificultad:</td>
	<td>
		<select id="Dificultad" name="Dificultad">
			<option value="1">1</option>
			<option value="2">2</option>
			<option value="3">3</option>
			<option value="4">4</option>
			<option value="5">5</option>
		</select>
	</td>
	</tr>
	
	<tr>
	<td><input type="submit" name='Anadir' id='Anadir' value="Anadir"/></td>
	</tr>
	</table>
	</form>
	</center>
	</body>
</html>'''

def escape_html(s):
    return cgi.escape(s, quote=True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASSWORD_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)

class AnadirPreguntaHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write(anadirPregunta_form)
	def post(self):
		preg = self.request.get('Nombre')
		resp = self.request.get('Respuesta')
		cat = self.request.get('Categoria')
		dif = self.request.get('Dificultad')
		u = Pregunta()
		u.nombre = preg
		u.respuesta = resp
		u.categoria = cat
		u.dificultad = int(dif)
		u.put()
		
class VerPreguntaHandler(webapp2.RequestHandler):
	def get(self):
		pregs=Pregunta.query()
		self.response.write("<center><h1>Preguntas</h1>")
		self.response.write("<table border='1'>")
		for preg in pregs:
			self.response.write("<tr><td>")
			self.response.write(preg.nombre)
			self.response.write("</td><td>")
			self.response.write(preg.respuesta)
			self.response.write("</td><td>")
			self.response.write(preg.dificultad)
			self.response.write("</td><td>")
			self.response.write(preg.categoria)
			self.response.write("</td></tr>")
			
		self.response.write("</table></center>")

class RegistroHandler(session_module.BaseSessionHandler):
	def write_form(self, username="", password="", verify="",email="", username_error="", password_error="",verify_error="", email_error=""):
		self.response.write(signup_form % {"username":username,"password": password,"verify": verify,"email": email,"username_error": username_error,"password_error": password_error,	"verify_error": verify_error,"email_error": email_error})

	def get(self):
		self.write_form()

	def post(self):
		user_username = self.request.get('username')
		user_password = self.request.get('password')
		user_verify = self.request.get('verify')
		user_email = self.request.get('email')
		sani_username = escape_html(user_username)
		sani_password = escape_html(user_password)
		sani_verify = escape_html(user_verify)
		sani_email = escape_html(user_email)
		username_error = ""
		password_error = ""
		verify_error = ""
		email_error = ""

		error = False
		if not valid_username(user_username):
			username_error = "Nombre incorrecto!"
			error = True
		if not valid_password(user_password):
			password_error = "Password incorrecto!"
			error = True
		if not user_verify or not user_password == user_verify:
			verify_error = "Password no coincide!"
			error = True
		if not valid_email(user_email):
			email_error = "Email incorrecto!"
			error = True

		if error:
			self.write_form(sani_username, sani_password, sani_verify, sani_email, username_error, password_error,verify_error, email_error)
		else:
			user = Usuario.query(Usuario.nombre == user_username, Usuario.email == user_email).count()
			if user == 0:
				u = Usuario()
				u.nombre = user_username
				u.email = user_email
				u.password = user_password
				u.put()
				self.session['email']=user_email
				self.response.write(inicio)
			else:
				self.write_form(sani_username, sani_password, sani_verify, sani_email, username_error, password_error,verify_error, email_error)
				self.response.out.write("Hola: %s <p> Ya estabas registrado" % user_username)
		
class LoginHandler(session_module.BaseSessionHandler):
	def write_form(self, password="", email="",password_error="", email_error=""):
		self.response.write(login_form % {"password": password,"email": email,"password_error": password_error,"email_error": email_error})
	def get(self):
		self.write_form()
	def post(self):
		user_password = self.request.get('contrasena')
		user_email = self.request.get('usuario')
		sani_password = escape_html(user_password)
		sani_email = escape_html(user_email)
		password_error = ""
		email_error = ""

		error = False
		if not valid_password(user_password):
			password_error = "Password incorrecto!"
			error = True
		if not valid_email(user_email):
			email_error = "Email incorrecto!"
			error = True

		if error:
			self.write_form(sani_password, sani_email, password_error,email_error)
		else:
			user = Usuario.query(Usuario.email == user_email, Usuario.password == user_password).count()
			if user != 0:
				self.response.write(inicio)
			else:
				self.response.out.write("Hola: %s <p> no estas registrado" % user_email)

class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write(inicio)

class Usuario(ndb.Model):
	nombre = ndb.StringProperty()
	password = ndb.StringProperty()
	email = ndb.StringProperty()

class Pregunta(ndb.Model):
	nombre = ndb.StringProperty()
	respuesta = ndb.StringProperty()
	categoria = ndb.StringProperty()
	dificultad = ndb.IntegerProperty()

app = webapp2.WSGIApplication([
	('/Registro', RegistroHandler),
	('/Login', LoginHandler),
	('/AnadirPreguntas', AnadirPreguntaHandler),
	('/VerPreguntas', VerPreguntaHandler),
	('/', MainHandler),
], 
config = session_module.myconfig_dict,
debug=True)

