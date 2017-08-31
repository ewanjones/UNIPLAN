import os
import sqlite3
from flask import Flask, render_template, url_for, request, redirect
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form
from dbconnect import connection	# Own file!

# -------
# SETUP
# -------

# create application instance
app = Flask(__name__)
app.config.from_object(__name__)


class RegistrationForm(Form):
	first_name = TextField('First Name', [validators.Length(min=4, max=20)])
	last_name = TextField('Last Name', [validators.Length(min=4, max=20)])
	email = TextField('Username', [validators.Length(min=4, max=50),
								   validators.Email(message='This is not a valid email address, please try again.')])
	password = TextField('Email Address', [validators.Length(min=3, max=20),
										   validators.Required(),
										   validators.EqualTo('confirm', message='Passwords do not match, please try again.')])
	accept_tos = BooleanField('I accept the Terms and Conditions')


# -------
# PAGES
# -------
@app.route('/login/', methods=['GET', 'POST'])
def login():
	error = ''
	try:
		if request.method == "POST":
			attempted_username = request.form['username']
			attempted_password = request.form['password']

			if attempted_username == 'admin' and attempted_password == 'password':
				return redirect(url_for('dashboard'))
			else:
				error = "Invalid credentials - try again!"
		
		return render_template("login.html", error = error)

	except:
		return render_template("login.html", error = error)




@app.route('/register/', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		try:
			c, conn = connection()
			return('okay!')
		except exception as e:
			return(str(e))
	return render_template("register.html")





@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html')




@app.route('/modules/')
def modules():
    return render_template('modules.html')



if __name__ == "__main__":
	app.run()

