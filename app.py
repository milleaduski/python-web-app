import datetime
from flask import Flask, render_template, request, url_for, redirect
from peewee import *
from hashlib import md5

app = Flask(__name__)

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

	def following(self):
		return (User.select()
					.join(Relationship, on=Relationship.from_user)
					.where(Relationship.to_user == self)
					.order_by(User.username))

class Message(BaseModel):
	user = ForeignKeyField(User, backref = 'Messages')
	content = TextField()
	published_at = DateTimeField(default=datetime.datetime.now())

class Relationship(BaseModel):
	from_user	= ForeignKeyField(User, backref='relationships')
	to_user 	= ForeignKeyField(User, backref='related_to')

	class Meta:
		indexes = (
			(('from_user', 'to_user'), True)
		)

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


# ================================================================
# ========================ROUTING=================================
# ================================================================

# Homepage routing
@app.route('/')
def showHomePage():
	return render_template('index.html')

@app.route('/register', methods =['GET', 'POST'])
def registerPage():
	if request.method == 'POST' and request.form['username']:
		try:
			with database.atomic():
				user = User.create(
						username 	= request.form['username'],
						password 	= md5(request.form['password'].encode('utf-8')).hexdigest(),
						email		= request.form['email']
				)
			return redirect(url_for('showHomePage'))
		except IntegrityError:
			return 'There is something error'


	return render_template('register.html')