from flask import Flask

app = Flask(__name__)

@app.route('/welcome')
def myFunction():
		return 'REstart server'

@app.route('/welcome/<user>')
def paramFunc(user):
		return 'Welcome %s' %user

@app.route('/profile/<int:user_id>')
def profileFunc(user_id):
		return 'Your id is %d' %user_id