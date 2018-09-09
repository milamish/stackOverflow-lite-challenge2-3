from flask import Flask, Blueprint, jsonify, request
from functools import wraps
from flask_restful import Api, Resource
import psycopg2
import jwt
import datetime


from __init__ import *
from models import *

queries = Blueprint('queries', __name__)


def tokens(k):
    @wraps(k)
    def decorators(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message' : 'Token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid'})
        return k(*args, **kwargs)
    return decorators
    
#this class allows a logged in user to post a question
class PostQuestion(Resource):
	@tokens
	def post(self):
		title = request.get_json()['title'].strip()
		question= request.get_json()['question'].strip()
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		user_id=data['user_id']

		if not question:
			return{"message":"post a question"}
				
		try:
			check_question(question)
			if cursor.fetchone() is not None:
				return{"this question exists":question}, 409
			post_question(title,question,user_id)
		except:
			return{"message":"unable to post a question"}, 500
		connection.commit()
		return {"title":title,"question":question,"user_id":user_id}, 200

api.add_resource(PostQuestion, '/api/v1/question')