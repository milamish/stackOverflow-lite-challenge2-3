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

#this class allows users to get a single question using the question ID
class GetQuestion(Resource):
	@tokens
	def get(self, question_id):
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		user_id=data['user_id']

		try:
			
				get_question(question_id)
				try:
					get_question(question_id)
					result=cursor.fetchone()
					if result is None:
						return {"message":"question_id does not exist"}, 404
					else:
						user_id=result[4]
						title = result[1]
						question=result[2]
						question_date= result[3]
						question_id=result[0]
						return jsonify({"user_id":user_id,"title":title, "question":question, "question_date":question_date, "question_id":question_id})
				except:
					return{"message": "unable to fetch entry"}, 500
				connection.commit()
		finally:
			pass
api.add_resource(GetQuestion, '/api/v1/question/<int:question_id>')