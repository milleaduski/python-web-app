from flask import Flask, render_template, request, make_response
from pprint import pprint

app = Flask(__name__)

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
		resp = make_response("Your email is "+ request.form['email'])
		resp.set_cookie('email_user', request.form['email'])
		return resp
	return render_template('login.html')

@app.route('/profile/<int:user_id>')
def profileFunc(user_id):
		return 'Your id is %d' %user_id

@app.route('/profile')
def profFunc():
	user = request.args.get('username')
	return render_template('profile.html')