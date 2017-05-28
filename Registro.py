signup_form='''<html>  <head>    <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
    <title>Introduzca sus datos:</title>    <style type="text/css">      
	.label {text-align: right}      .error {color: red}    </style>  
</head>   <body>  <h1>DSSW-Tarea 2</h1>    <h2>Rellene los campos por favor:</h2>    
<form method="post">
<table>        <tr>          <td class="label">
            Nombre de usuario
			</td>
			<td>
            <input type="text" name="username" value="%(username)s" placeholder="Tu nombre...">          </td>          <td class="error">%(username_error)s
</td>        </tr>         <tr>          <td class="label">            Password          
</td>          <td>            <input type="password" name="password" value="%(password)s" autocomplete="off">          </td>          <td class="error">            %(password_error)s
</td>                       </td>        
</tr>         <tr>          <td class="label">            Repetir Password          </td>          
<td>            <input type="password" name="verify" value="%(verify)s" placeholder="El mismo de antes">          </td>          <td class="error">            %(verify_error)s          </td>        </tr>         <tr>          <td class="label">            
Email          </td>          <td>            <input type="text" name="email" value="%(email)s">          </td>          <td class="error">            %(email_error)s          </td>        </tr>      </table>       <input type="submit">    </form>  </body> </html>'''
class Registro(webapp2.RequestHandler):
	def get(self):
		self.response.write(signup_form)