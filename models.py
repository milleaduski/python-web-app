import datetime
from peewee import *

DATABASE = SqliteDatabase('comments.db')

class Message(Model):
	context = TextField()
	create_at = DateTimeField(default=datetime.datetime.now())

	class Meta:
		database = DATABASE

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Message], safe=True)
	DATABASE.close()