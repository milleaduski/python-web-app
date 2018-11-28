from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/welcome')
def homeFunction():
		return render_template('index.html')

@app.route('/welcome/<user>')
def paramFunc(user):
		return render_template('profile.html', userData = user)

@app.route('/login', methods=["GET", "POST"])
def login():
	if request.method == "POST":
		return "Your email is "+ request.form['email']
	
	return render_template('login.html')

@app.route('/profile/<int:user_id>')
def profileFunc(user_id):
		return 'Your id is %d' %user_id

@app.route('/profile')
def profFunc():
	user = request.args.get('username')
	return render_template('profile.html')