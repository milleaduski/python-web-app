from flask import jsonify
from flask_restful import Resource

import models

class MessageList(Resource):
	def get(self):
		# Get all data from table
		data = {}
		messages = models.Message.select()
		for row in messages:
			data[row.id] = {'context': row.context}
		return jsonify({'messages' : data})