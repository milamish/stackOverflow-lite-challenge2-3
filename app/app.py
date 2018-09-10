"""import modules"""
from flask import Flask
from flask import jsonify
from flask import request
from flask_restful import Api
from flask_restful import Resource

APP = Flask(__name__)
API = Api(APP)

USERS = {}
QUERY = []
ANSWER = []
ANSWERS = {"ANSWER": ANSWER}
QUERIES = {"QUERY": QUERY}


class Home(Resource):
    """homepage"""
    def get(self):
        """ get homepage"""
        return jsonify({"message": "welcome to stackoverflowlite, post or answer questions!"})
API.add_resource(Home, '/api/v1/')

class Signup(Resource):
    """signup user details"""
    def post(self):
        """post user details for signup"""
        name = request.get_json()['name']
        emailaddress = request.get_json()['emailaddress']
        password = request.get_json()['password']
        username = request.get_json()['username']
        try:
            if username in USERS:
                if username == USERS[username]['username']:
                    return jsonify({"message": "user already exists"}), 409
                else:
                    return jsonify({"message": "check your details"})
            else:
                USERS.update({username: {"name": name,\
                    "emailaddress": emailaddress, "password": password}})
                return jsonify({"name": name, "username": username})
        except:
            return jsonify({"message": "unable to register"})
API.add_resource(Signup, '/stackoverflowlite.com/api/v1/auth/signup')

class Login(Resource):
    """login users"""
    def post(self):
        """post login details"""
        username = request.get_json()["username"]
        password = request.get_json()["password"]
        if username in USERS:
            if password == USERS[username]["password"]:
                return jsonify({"message": "succesfuly logged in"})
            else:
                return jsonify({"message": "your password is wrong"}), 400
        else:
            return jsonify({"message": "check your username"}), 400
API.add_resource(Login, '/stackoverflowlite.com/api/v1/auth/login')

class PostQuestion(Resource):
    """post question"""
    def post(self):
        """post a question"""
        title = request.get_json()['title']
        question = request.get_json()['question']
        for question in QUERY:
            return jsonify({"message": "question is available"})
        else:
            QUERY.append({"title": title, "question": question})
            return jsonify({"title": title, "question": question})
API.add_resource(PostQuestion, '/stackoverflowlite.com/api/v1/question')

class Answer(Resource):
    """answer a qestion"""
    def post(self, ID):
        """post an answer to a qestion"""
        post_answer = request.get_json()['post_answer']
        try:
            if ID in QUERY:
                if ID != QUERY[QUERY[ID-1]]['ID']:
                    return jsonify({"message": "question does not exist"}), 404
                else:
                    return jsonify({"message": "unable to post answer"}), 500
            else:
                ANSWER.append({"post_answer": post_answer, "query": QUERY[ID-1]})
                return jsonify({"query": QUERY[ID-1], "post_answer": post_answer})
        except:
            return jsonify({"message": "question ID does not exist"})
API.add_resource(Answer, '/stackoverflowlite.com/api/v1/question/<int:ID>/answer')


class DeleteQuestion(Resource):
    """detete a question"""
    def delete(self, ID):
        """detete a question using the question ID"""
        try:
            if ID in QUERY is None:
                return jsonify({"message": "question not available"}), 404
            else:
                del QUERY[ID-1]
                return jsonify({"message": "question succesfuly deleted"})
        except TypeError:
            return jsonify({"message": "question ID does not exist"}), 404
API.add_resource(DeleteQuestion, '/stackoverflowlite.com/api/v1/question/<int:ID>')

class GetQuestions(Resource):
    """get questions"""
    def get(self):
        """get all questions"""
        try:
            if QUERIES is None:
                return jsonify({"message": "no questions available"})
            else:
                return jsonify(QUERIES)
        except TypeError:
            return jsonify({"message": "unable to fetch questions"}), 500
API.add_resource(GetQuestions, '/stackoverflowlite.com/api/v1/question')

class GetOneQuestion(Resource):
    """get one question"""
    def get(self, ID):
        """get one question using the question ID"""
        try:
            if ID in QUERY is None:
                return jsonify({"message": "question cannot be found"})
            else:
                return jsonify(QUERY[ID-1])
        except TypeError:
            return jsonify({"message": "question ID does not exist"}), 404
API.add_resource(GetOneQuestion, '/stackoverflowlite.com/api/v1/question/<int:ID>')

class GetAnswers(Resource):
    """get all answers"""
    def get(self):
        """get all questions with the answers"""
        return jsonify(ANSWERS)
API.add_resource(GetAnswers, '/stackoverflowlite.com/api/v1/answers')

class UpdateAnswer(Resource):
    """update an answer"""
    def put(self, ID):
        """update a n answer to a question using the answer ID"""
        update_answer = request.get_json()['update_answer']
        try:
            if ID in ANSWER is None:
                return jsonify({"message": "answer not available"}), 404
            else:
                ANSWER.append({"update_answer": update_answer, "answer": ANSWER[ID-1]})
                return jsonify({"update_answer": update_answer, "answer": ANSWER[ID-1]})
        except TypeError:
            return jsonify({"message": "Answer ID does not exist"}), 404
API.add_resource(UpdateAnswer, '/stackoverflowlite.com/api/v1/answer/<int:ID>')

if __name__ == "__main__":
    APP.run(debug=True)
