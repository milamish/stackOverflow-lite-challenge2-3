from flask import Flask
from flask import jsonify
from flask import request
from flask_restful import Api
from flask_restful import Resource

app = Flask(__name__)
api= Api(app)

users = {}
query = []
answer = []
answers = {"answer" : answer}
queries = {"query" : query}

class Home(Resource):
    def get(self):
        return jsonify({"message":"welcome to stackoverflowlite, post or answer questions!"})
api.add_resource(Home, '/api/v1/')

class Signup(Resource):
    def post(self):
        """post user details for signup"""
        name = request.get_json()['name']
        emailaddress = request.get_json()['emailaddress']
        password = request.get_json()['password']
        username = request.get_json()['username']
        try:
            if username in users:
                if username == users[username]['username']:
                    return jsonify({"message" : "user already exists"}), 409
                else:
                    return jsonify({"message":"check your details"})
                   
            else:
                users.update({username:{"name":name , "emailaddress":emailaddress, "password":password}})
                return jsonify({"name":name, "username":username})
        except:
            return jsonify({"message":"user exists"})
               
            
api.add_resource(Signup , '/stackoverflowlite.com/api/v1/auth/signup')

class Login(Resource):
    def post(self):
        """post login details"""
        username = request.get_json()["username"]
        password = request.get_json()["password"]
        if username in users:
            if password == users[username]["password"]:
                return jsonify({"message":"succesfuly logged in"})           
            else:
                return jsonify({"message": "your password is wrong"}), 400
        else:
            return jsonify({"message": "check your username"}), 400
api.add_resource(Login ,'/stackoverflowlite.com/api/v1/auth/login')

class PostQuestion(Resource):
    def post(self):
        """post a question"""
        title = request.get_json()['title']
        question = request.get_json()['question']
        for question in query:
            return jsonify({"message" : "question is available"})
        else:
            query.append({"title" : title,"question" : question})
            return jsonify({"title" : title, "question" : question})    
api.add_resource(PostQuestion,'/stackoverflowlite.com/api/v1/question')

class Answer(Resource):
    def post(self , ID):
        """post an answer to a qestion"""
        post_answer = request.get_json()['post_answer']
        try:
            if ID in query:
                if ID != query[query[ID-1]]['ID']:
                    return jsonify({"message" : "question does not exist"}), 400
                else:
                    return jsonify({"message" : "unable to post answer"}), 500
            else:
                answer.append({"post_answer" : post_answer, "query" : query[ID-1]})
                return jsonify({"query" : query[ID-1] , "post_answer":post_answer})
        except:
            return jsonify({"message" : "question ID does not exist"})
api.add_resource(Answer , '/stackoverflowlite.com/api/v1/question/<int:ID>/answer')


class DeleteQuestion(Resource):
    def delete(self , ID):
        """detete a question using the question ID"""
        try:
            if ID in query is None:
                return jsonify({"message":"question not available"}), 400
            else:
                del query[ID-1]
                return jsonify({"message":"question succesfuly deleted"})
        except:
            return jsonify({"message":"question ID does not exist"}), 400
api.add_resource(DeleteQuestion , '/stackoverflowlite.com/api/v1/question/<int:ID>')

class GetQuestions(Resource):
    def get(self):
        """get all questions"""
        try:
            if queries is None:
                return jsonify({"message" : "no questions available"})
            else:
                return jsonify(queries)
        except:
            return jsonify({"message" : "unable to fetch questions"}), 500
api.add_resource(GetQuestions , '/stackoverflowlite.com/api/v1/question')

class GetOneQuestion(Resource):
    def get(self , ID):
        """get one question using the question ID"""
        try:
            if ID in query is None:
                return jsonify({"message":"question cannot be found"})
            else:
                return jsonify(query[ID-1])
        except:
            return jsonify({"message" : "question ID does not exist"}), 400
            
api.add_resource(GetOneQuestion , '/stackoverflowlite.com/api/v1/question/<int:ID>')

class GetAnswers(Resource):
    def get(self):
        """get all questions with the answers"""
        return jsonify(answers)
api.add_resource(GetAnswers , '/stackoverflowlite.com/api/v1/answers')

class UpdateAnswer(Resource):
    def put(self, ID):
        """update a n answer to a question using the answer ID"""
        update_answer = request.get_json()['update_answer']
        try :
            if ID in answer is None:
                return jsonify({"message" : "answer not avaiable"}), 400    
            else:
                answer.append({"update_answer" : update_answer , "answer" : answer[ID-1]})
                return jsonify({"update_answer" : update_answer, "answer" : answer[ID-1]})
        except :
                return jsonify({"message" : "Answer ID does not exist"}), 400
api.add_resource(UpdateAnswer , '/stackoverflowlite.com/api/v1/answer/<int:ID>')

if __name__=="__main__":
    app.run(debug=True)