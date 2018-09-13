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


from __init__ import app, api
from models import *

queries = Blueprint('queries', __name__)


def tokens(k):
    """tokens for aunthentication"""
    @wraps(k)
    def decorators(*args, **kwargs):
        """decorators for pursing token to different functions"""
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid'})
        return k(*args, **kwargs)
    return decorators


'''class UrlValidation():
    """url validator"""
    headers = {"Authorization": [DataRequired(), Resource]}

#this class allows a logged in user to post a question'''


class PostQuestion(Resource):
    """posting questions"""
    @tokens
    def post(self):
        """posts a question"""
        title = request.get_json()['title'].strip()
        question = request.get_json()['question'].strip()
        data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
        user_id = data['user_id']

        if not question:
            return{"message": "post a question"}
                
        try:
            Questions.check_question(question)
            if cursor.fetchone() is not None:
                return{"this question exists": question}, 409
            Questions.post_question(title, question, user_id)
        except:
            return{"message": "unable to post a question"}, 500
        connection.commit()
        return {"title": title, "question": question, "user_id": user_id}, 200

#this class allows users to get a single question using the question ID


class GetQuestion(Resource):
    """fetch questions"""
    @tokens
    def get(self, question_id):
        """gets a question"""
        data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
        user_id = data['user_id']

        try:
            
                Questions.get_question(question_id)
                try:
                    Questions.get_question(question_id)
                    result = cursor.fetchone()
                    if result is None:
                        return {"message": "question_id does not exist"}, 404
                    else:
                        user_id = result[4]
                        title = result[1]
                        question = result[2]
                        question_date = result[3]
                        question_id = result[0]
                        return jsonify({"user_id": user_id, "title": title, "question": question,\
                         "question_date": question_date, "question_id": question_id})
                except:
                    return{"message": "unable to fetch entry"}, 500
                connection.commit()
        finally:
            pass

#this class allows a user to post an answer to a question using the question id then retrieving the question


class PostAnswer(Resource):
    """post answer"""
    @tokens
    def post(self, question_id):
        """post answer using the question ID"""
        data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
        user_id = data['user_id']
        answer = request.get_json()['answer']
        if not answer:
            return {"message": "post an answer"}
        try:         
                Questions.get_question(question_id)
                if cursor.fetchone() is None:
                    return {"message": "question does not exist"}, 404
                else:
                    Questions.post_answer(answer, user_id, question_id)
        except:
            return{"message": "the question does not exist"}, 500
        connection.commit()
        return {"question_id": question_id, "answer": answer, "user_id": user_id}, 200

#this class allows a user to retrieve all answers to a specific question using the question ID


class Getanswers(Resource):
    @tokens
    def get(self,question_id):
        data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
        user_id = data['user_id']
        
        try:
                Questions.get_answers(question_id)
                try:
                    Questions.get_answers(question_id)
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
                            questions.update({answer_id:{"question": question, "answer": answer, \
                                "answer_date": answer_date}})

                        return jsonify(questions)
                except:
                    return ({"message": "entry not found"}), 500
                connection.commit()
        finally:
            pass

#this class allows users to view all asked questions


class AllQuestions(Resource):
    """fetch all questions"""
    @tokens
    def get(self):
        """get all asked questions"""
        data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
        user_id = data['user_id']

        try:
                Questions.get_all_questions()
                try:
                    Questions.get_all_questions()
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
                            questions.update({question_id:{"title": title, "question": question, "user_id": user_id,\
                             "question_date": question_date}})

                        return jsonify(questions)
                except:
                    return jsonify({"message": "not found"}), 500
                connection.commit()
        finally:
            pass

#this class allows a user to edit their own answers


class Modify(Resource):
    """modify answer"""
    @tokens
    def put(self, question_id, answer_id):
        """a user can only modify an answer posted by them"""
        data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
        user_id = data['user_id']
        answer = request.get_json()['answer'].strip()
        Questions.get_user_id_and_answer_id(answer_id, question_id, user_id)
        result = cursor.fetchone()
        if result is not None:
            Questions.modify_answer(question_id, answer, answer_id)
        else:
            return {"message": "entry does not exist"}, 404
        connection.commit()
        return{"answer": answer, "question_id": question_id, "answer_id": answer_id}, 201

#this class allows authors of questions to delete their own questions


class Remove(Resource):
    """delete a question"""
    @tokens
    def delete(self, question_id):
        """a user can only delete a question posted by them"""
        data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
        user_id = data['user_id']
        
        try:
                Questions.get_user_id(question_id, user_id)
                result = cursor.fetchone()
                if result is None:
                    return {"message": "question does not exist"}, 404
                else:
                    Questions.delete_question(user_id, question_id)
        except:
            return {"message": "unable to delete question"}, 500
        connection.commit()
        return {"question": "question succesfully deleted"}


class SingleUserQuestions(Resource):
    """all questions asked by an individual user"""
    @tokens
    def get(self):
        """a user can fetch all questions asked by them"""
        data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
        user_id = data['user_id']
        try:
                Questions.get_all_questions_by_a_user(user_id)
                try:
                    Questions.get_all_questions_by_a_user(user_id)
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
                            questions.update({question_id: {"title": title, "question": question, "user_id": user_id,\
                             "question_date": question_date}})

                        return jsonify(questions)
                except:
                    return jsonify({"message": "not found"}), 500
                connection.commit()
        finally:
            pass


class SearchTitles(Resource):
    """search by title"""
    @tokens
    def get(self, title):
        """get all questions under the same title"""
        data = jwt.decode(request.headers.get('x-access-token'), app.config['SECRET_KEY'])
        user_id = data['user_id']
        try:
                Questions.get_questions_by_title(title)
                try:
                    Questions.get_questions_by_title(title)
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
                            questions.update({question_id: {"title": title, "question": question, "user_id": user_id,\
                             "question_date": question_date}})

                        return jsonify(questions)
                except:
                    return jsonify({"message": "not found"}), 500
                connection.commit()
        finally:
            pass

api.add_resource(PostQuestion, '/api/v1/questions')
api.add_resource(GetQuestion, '/api/v1/question/<int:question_id>')
api.add_resource(PostAnswer, '/api/v1/questions/<int:question_id>/answers')
api.add_resource(Getanswers, '/api/v1/questions/<int:question_id>')
api.add_resource(AllQuestions, '/api/v1/questions')
api.add_resource(Modify, '/api/v1/questions/<int:question_id>/answers/<int:answer_id>')
api.add_resource(Remove, '/api/v1/questions/<int:question_id>')
api.add_resource(SingleUserQuestions, '/api/v1/allquestions')
api.add_resource(SearchTitles, '/api/v1/questions/<string:title>')

