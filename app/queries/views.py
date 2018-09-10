from flask import Flask
from flask import Blueprint
from flask import jsonify
from flask import request
from functools import wraps
from flask_restful import Api
from flask_restful import Resource
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
            return jsonify({'message': 'Token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid'})
        return k(*args, **kwargs)
    return decorators
    
#this class allows a logged in user to post a question
class PostQuestion(Resource):
	@tokens
	def post(self):
		title = request.get_json()['title'].strip()
		question = request.get_json()['question'].strip()
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		user_id = data['user_id']

		if not question:
			return{"message": "post a question"}
				
		try:
			check_question(question)
			if cursor.fetchone() is not None:
				return{"this question exists": question}, 409
			post_question(title, question, user_id)
		except:
			return{"message": "unable to post a question"}, 500
		connection.commit()
		return {"title": title, "question": question, "user_id": user_id}, 200
api.add_resource(PostQuestion, '/api/v1/questions')

#this class allows users to get a single question using the question ID
class GetQuestion(Resource):
	@tokens
	def get(self, question_id):
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		user_id = data['user_id']

		try:
			
				get_question(question_id)
				try:
					get_question(question_id)
					result = cursor.fetchone()
					if result is None:
						return {"message": "question_id does not exist"}, 404
					else:
						user_id = result[4]
						title = result[1]
						question = result[2]
						question_date = result[3]
						question_id = result[0]
						return jsonify({"user_id": user_id, "title": title, "question": question, "question_date": question_date, "question_id": question_id})
				except:
					return{"message": "unable to fetch entry"}, 500
				connection.commit()
		finally:
			pass
api.add_resource(GetQuestion, '/api/v1/question/<int:question_id>')

#this class allows a user to post an answer to a question using the question id then retrieving the question
class PostAnswer(Resource):
	@tokens
	def post(self, question_id):
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		user_id = data['user_id']
		answer = request.get_json()['answer']
		if not answer:
			return {"message": "post an answer"}
		try:
			
				get_question(question_id)
				if cursor.fetchone() is None:
					return {"message": "question does not exist"}, 404
				else:
					post_post_answer(answer, user_id, question_id)
		except:
			return{"message": "the question does not exist"}, 500
		connection.commit()
		return {"question_id": question_id, "answer": answer, "user_id": user_id}, 200
api.add_resource(PostAnswer, '/api/v1/questions/<int:question_id>/answers')

#this class allows a user to retrieve all answers to a specific question using the question ID
class Getanswers(Resource):
	@tokens
	def get(self,question_id):
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		user_id = data['user_id']
		
		try:
				get_answers(question_id)
				try:
					get_answers(question_id)
					result = cursor.fetchall()
					questions = {}
					if len(result) == 0:
						return {"message": "no answers found"}, 404
					else:
						for row in result:
							answer_id=row[0]
							answer=row[1]
							question=row[2]
							answer_date=row[4]
							questions.update({answer_id:{"question": question, "answer": answer, "answer_date": answer_date}})

						return jsonify(questions)
				except:
					return ({"message": "entry not found"}), 500
				connection.commit()
		finally:
			pass
api.add_resource(Getanswers, '/api/v1/questions/<int:question_id>')

#this class allows users to view all asked questions
class AllQuestions(Resource):
	@tokens
	def get(self):
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		user_id = data['user_id']

		try:
				get_all_questions()
				try:
					get_all_questions()
					result = cursor.fetchall()
					questions = {}
					if len(result) == 0:
						return {"message": "no questions found"}, 404
					else:
						for row in result:
							question_id = row[0]
							title = row[1]
							question = row[2]
							question_date = row[3]
							user_id = row[4]
							questions.update({question_id:{"title": title, "question": question, "user_id": user_id, "question_date": question_date}})

						return jsonify(questions)
				except:
					return jsonify({"message": "not found"}), 500
				connection.commit()
		finally:
			pass
api.add_resource(AllQuestions, '/api/v1/questions')

#this class allows a user to edit their own answers
class Modify(Resource):
	@tokens
	def put (self, question_id, answer_id):
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		user_id = data['user_id']
		answer = request.get_json()['answer'].strip()
		get_user_id_and_question_id(answer_id, question_id, user_id)
		result = cursor.fetchone()
		if result is not None:
			modify_answer(question_id, answer, answer_id)
		else:
			return {"message": "entry does not exist"}, 404
		connection.commit()
		return{"answer": answer, "question_id": question_id, "answer_id": answer_id}, 201
api.add_resource(Modify, '/api/v1/questions/<int:question_id>/answers/<int:answer_id>')

#this class allows authors of questions to delete their own questions
class Remove(Resource):
	@tokens
	def delete(self, question_id):
		data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
		user_id=data['user_id']
		
		try:
				get_user_id(question_id,user_id)
				result=cursor.fetchone()
				if result is None:
					return {"message": "question does not exist"}, 404
				else:
					delete_question(user_id, question_id)
		except:
			return {"message": "unable to delete question"}, 500
		connection.commit()
		return {"question": "question succesfully deleted"}
api.add_resource(Remove, '/api/v1/questions/<int:question_id>')