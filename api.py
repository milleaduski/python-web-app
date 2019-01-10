from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

users = {}

class User(Resource):
	def get(self, user_id):
		return {'name' : users[user_id]}

	def put(self, user_id):
		users[user_id] = request.form['user']
		return {'name' : users[user_id]}

api.add_resource(User, '/user/<string:user_id>')

if __name__ == '__main__':
	app.run(debug = True)