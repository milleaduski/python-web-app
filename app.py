import datetime
from flask import Flask
from peewee import *

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
def after_request():
	database.close()
	return response

def create_tables():
	with database:
		database.create_tables([User, Relationship, Message])
