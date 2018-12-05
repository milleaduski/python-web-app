from flask import Flask, render_template, request, make_response, session, url_for, redirect
from pprint import pprint

app = Flask(__name__)

app.secret_key = '34ujeifaj21mkll'
@app.route('/welcome')
def homeFunction():
		email = request.cookies.get('email_user')
		pprint(locals())
		return render_template('index.html', email = email)

@app.route('/welcome/<user>')
def paramFunc(user):
		return render_template('profile.html', userData = user)

@app.route('/login', methods=["GET", "POST"])
def login():
	if request.method == "POST":
		# resp = make_response("Your email is "+ request.form['email'])
		# resp.set_cookie('email_user', request.form['email'])
		session['email'] = request.form['email']
		# return resp

	if 'email' in session:
		email = session['email']
		return redirect(url_for('profileFunc', email = email))
	return render_template('login.html')

@app.route('/profile/<email>')
def profileFunc(email):
	return render_template('profile.html', email = email)

@app.route('/logout')
def logout():
	session.pop('email', None)
	return redirect(url_for("login"))

@app.route('/profile')
def profFunc():
	user = request.args.get('username')
	return render_template('profile.html')