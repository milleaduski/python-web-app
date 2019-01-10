import datetime
from peewe import *

DATABASE = SqliteDatabase('coments.db')

class Message(Model):
	context = TextField()
	create_at = DateTimeField(default=datetime.datetime.now())

class meta:
	database = DATABASE

def initialize():
	DATABASE.connect()
	DATABASE.create_tables(Message, safe = True)
	DATABASE.close()