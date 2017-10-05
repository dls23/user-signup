from flask import Flask, request, redirect
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader (template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    template = jinja_env.get_template('index.html')
    return template.render()

@app.route("/", methods={'POST'})
def validate():

    username = request.form['username']
    pw = request.form['password']
    verify = request.form['verify']
    email = request.form['email']

    username_error = ''
    pw_error = ''
    verify_error = ''
    email_error = ''

    if not username:
        username_error = 'Must supply a username'
    else:
        if (len(username) < 3) or (len(username) > 20) or (' ' in username):
            username_error = 'A valid username must be between 3 and 20 characters and not contain spaces'

    if not pw:
        pw_error = 'Must supply a password'
    else:
        if (len(pw) < 3) or (len(pw) > 20) or (' ' in pw):
            pw_error = 'A valid password must be between 3 and 20 characters and not contain spaces'

    if not verify:
        verify_error = 'Please verify password'

    if not pw == verify:
        pw_error = 'Passwords must match'
        
    if email:
        if (len(email) < 3) or (len(email) > 20) or (' ' in email) or (email.count('@') != 1) or (email.count('.') != 1):
            email_error = 'Please enter a valid email address'
    
    if not username_error and not pw_error and not verify_error and not email_error:
        welcome = jinja_env.get_template('welcome.html')
        return welcome.render(name=username)

    else:
        template = jinja_env.get_template('index.html')
        return template.render(username_error=username_error, pw_error=pw_error, verify_error=verify_error, email_error=email_error, username=username, email=email)

app.run()