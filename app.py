import datetime
from functools import wraps
from flask import Flask, render_template, request, url_for, redirect, session, flash, abort
from peewee import *
from hashlib import md5

app = Flask(__name__)
app.secret_key = 'so_secret_123456789'

DATABASE = 'tweets.db'
database = SqliteDatabase(DATABASE)

class BaseModel(Model):
	class Meta:
		database = database


class User(BaseModel):
	username = CharField(unique=True)
	password = CharField()
	email = CharField(unique=True)
	join_at = DateTimeField(default=datetime.datetime.now())

	def following(self):
		return (User.select()
					.join(Relationship, on=Relationship.to_user)
					.where(Relationship.from_user == self)
					.order_by(User.username))

	def followers(self):
		return (User.select()
					.join(Relationship, on=Relationship.from_user)
					.where(Relationship.to_user == self)
					.order_by(User.username))

	def is_following(self, user):
		return (Relationship.select()
				.where( (Relationship.from_user == self) & (Relationship.to_user == user) )
				.exists())


class Message(BaseModel):
	user = ForeignKeyField(User, backref = 'messages')
	content = TextField()
	published_at = DateTimeField(default=datetime.datetime.now())



class Relationship(BaseModel):
	from_user	= ForeignKeyField(User, backref='relationships')
	to_user 	= ForeignKeyField(User, backref='related_to')

	class Meta:
		indexes = (
			(('from_user', 'to_user'), True)
		)

def not_login(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if session.get('logged_in'):
			return redirect(url_for('showHomePage'))
		return f(*args, **kwargs)
	return decorated_function

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if not session.get('logged_in'):
			return redirect(url_for('loginPage'))
		return f(*args, **kwargs)
	return decorated_function

@app.before_request
def before_request():
	database.connect()

@app.after_request
def after_request(response):
	database.close()
	return response

def create_tables():
	with database:
		database.create_tables([User, Relationship, Message])

def auth_user(user):
	session['logged_in'] = True
	session['user_id']	 = user.id
	session['username']	 = user.username
	flash('You have successfully logged in '+ session['username'])

def get_current_user():
	if session.get('logged_in'):
		return User.get(User.id ==  session['user_id'])

# ================================================================
# ========================ROUTING=================================
# ================================================================

# Homepage routing
@app.route('/')
@login_required
def showHomePage():
	user = get_current_user()
	messages = (Message.select()
				.where((Message.user << user.following()) |
					(Message.user == user.id)
				)
				.order_by(Message.published_at.desc()).limit(3)
		)
	return render_template('index.html', messages = messages)

@app.route('/register', methods =['GET', 'POST'])
@not_login
def registerPage():
	if request.method == 'POST' and request.form['username']:
		try:
			with database.atomic():
				user = User.create(
						username 	= request.form['username'],
						password 	= md5(request.form['password'].encode('utf-8')).hexdigest(),
						email		= request.form['email']
				)
				auth_user(user)
			return redirect(url_for('showHomePage'))
		except IntegrityError:
			return 'There is something error'
	return render_template('register.html')

@app.route('/login', methods =['GET', 'POST'])
def loginPage():
	if request.method == 'POST' and request.form['username']:
		try:
			hashed_pass = md5(request.form['password'].encode('utf-8')).hexdigest()
			user = User.get(
				(User.username == request.form['username']) &
				(User.password == hashed_pass)
			)
		except User.DoesNotExist:
			return 'User doesnt Exist'
		else:
			auth_user(user)
			current_user = get_current_user()
			return redirect(url_for('showHomePage'))
	return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('logout was successful')
	return redirect(url_for('showHomePage'))

@app.route('/add-post', methods =['GET', 'POST'])
@login_required
def createPost():
	user = get_current_user()
	if request.method == 'POST' and request.form['content']:
		message = Message.create(
			user 		 = user,
			content 	 = request.form['content']
		)
		flash('Your status has been updated successfully')
		# Before
		# return redirect(url_for('showHomePage'))
		return redirect(url_for('userProfile', username = user.username))
	return render_template('newPost.html')


@app.route('/user/<username>')
def userProfile(username):
	try:
		user = User.get(User.username == username)
	except User.DoesNotExist:
		abort(404)
	messages = user.messages.order_by(Message.published_at.desc())
	return render_template('profile.html', messages = messages, user=user)

@app.route('/user_follow/<username>', methods =['POST'])
def userFollow(username):
	try:
		user = User.get(User.username == username)
	except User.DoesNotExist:
		abort(404)
	# Atomic transaction
	try:
		with database.atomic():
			Relationship.create(
				from_user = get_current_user(),
				to_user = user
			)
	except IntegrityError:
		pass
	flash("you have followed "+ username)
	return redirect(url_for('userProfile', username=username))

@app.route('/user_unfollow/<username>', methods =['POST'])
def userUnfollow(username):
	try:
		user = User.get(User.username == username)
	except User.DoesNotExist:
		abort(404)

	(Relationship.delete()
		.where(
			(Relationship.from_user == get_current_user()) &
			(Relationship.to_user == user))
		.execute())

	flash("you have unfollowed "+ username)
	return redirect(url_for('userProfile', username=username))

@app.route('/user/<username>/following')
def showFollowing(username):
	try:
		user = User.get(User.username == username)
	except User.DoesNotExist:
		abort(404)
	return render_template('userList.html', users = user.following())

@app.route('/user/<username>/followers')
def showFollowers(username):
	try:
		user = User.get(User.username == username)
	except User.DoesNotExist:
		abort(404)
	return render_template('userList.html', users = user.followers())


@app.context_processor
def _inject_user():
	return {'active_user': get_current_user()}