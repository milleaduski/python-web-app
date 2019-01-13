from flask import Flask, request
from flask_restful import Resource, Api

import models
import messages

app = Flask(__name__)
api = Api(app)

api.add_resource(messages.MessageList, '/messages')

if __name__ == '__main__':
	models.initialize()
	app.run(debug = True)