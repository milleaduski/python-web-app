from flask import Flask, render_template, request, make_response, session, url_for, redirect, flash
from pprint import pprint
import os

from werkzeug.utils import secure_filename
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
		flash("You have successfully logged in", "success")
		return redirect(url_for('profileFunc', email = session['email']))

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
	flash("You have successfully logged out", "warning")
	return redirect(url_for("login"))

@app.route('/profile')
def profFunc():
	user = request.args.get('username')
	return render_template('profile.html')

# check file before save
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

ALLOWED_EXTENSION = set(['png', 'jpeg', 'jpg'])
app.config['UPLOAD_FOLDER'] = 'uploads'
@app.route('/upload', methods=["GET", "POST"])
def uploadFile():
	if request.method == 'POST':
		file = request.files['file']

		if 'file' not in request.files:
			return redirect(request.url)

		if file.filename == '': 
			return redirect(request.url)

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return "Your file has been saved.." + filename
	return render_template('upload.html')
