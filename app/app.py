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
answers = {"answer":answer}
queries = {"query":query}

class Signup(Resource):
    def post(self):
        name = request.get_json()['name']
        emailaddress = request.get_json()['emailaddress']
        password = request.get_json()['password']
        username = request.get_json()['username']
        if username in users:
            return jsonify({"message":"user already exists"}), 409
        else:
            users.update({username:{"name": name,"emailadress": emailaddress,"password": password}})
            return jsonify({"name": name},{"username":username})
api.add_resource(Signup,'/stackoverflowlite.com/api/v1/auth/signup' )

class Login(Resource):
    def post(self):
        username = request.get_json()["username"]
        password = request.get_json()["password"]
        if username in users:
            if password == users[username]["password"]:
            	return jsonify({"message":"succesfuly logged in"})           
            else:
                return jsonify({"message": "your password is wrong"})
        else:
            return jsonify({"message": "check your username"})
api.add_resource(Login,'/stackoverflowlite.com/api/v1/auth/login')

class Post_question(Resource):
    def post(self):
        question = request.get_json()["question"]
        query.append({"question":question})
        return jsonify({"question":question})
api.add_resource(Post_question,'/stackoverflowlite.com/api/v1/question')

class Answer(Resource):
	def post(self,ID):
		post_answer = request.get_json()['post_answer']
		try:
			if ID in query:
				if ID!= query[question]['ID']:
					return jsonify({"message":"question does not exist"})
				else:
					return jsonify({"message":"unable to post answer"}), 500
			else:
				answer.append({"post_answer":post_answer, "query":query[ID-1]})
				return jsonify({"query":query[ID-1],"post_answer":post_answer})
		except:
			return jsonify({"message":"question ID does not exist"})
api.add_resource(Answer,'/stackoverflowlite.com/api/v1/question/<int:ID>/answer')


class Delete_question(Resource):
	def delete(self, ID):
		try:
			if ID in query is None:
				return jsonify({"message":"question not available"})
			else:
				del query[ID-1]
				return jsonify({"message":"question succesfuly deleted"})
		except:
			return jsonify({"message":"question ID does not exist"})
api.add_resource(Delete_question, '/stackoverflowlite.com/api/v1/question/<int:ID>')

class Get_questions(Resource):
	def get(self):
		try:
			if queries is None:
				return jsonify({"message":"no questions available"})
			else:
				return jsonify(queries)
		except:
			return jsonify({"message":"unable to fetch questions"})
api.add_resource(Get_questions, '/stackoverflowlite.com/api/v1/question')

class Get_one_question(Resource):
	def get(self, ID):
		try:
			if ID in query is None:
				return jsonify({"message":"question cannot be found"})
			else:
				return jsonify(query[ID-1])
		except:
			return jsonify({"message":"question ID does not exist"})
			
api.add_resource(Get_one_question, '/stackoverflowlite.com/api/v1/question/<int:ID>')

class Get_answers(Resource):
	def get(self):
		return jsonify(answers)
api.add_resource(Get_answers, '/stackoverflowlite.com/api/v1/answers')

class Update_answer(Resource):
	def put(self, ID):
		update_answer = request.get_json()['update_answer']
		try:
			if ID in answer is None:
				return jsonify({"message":"answer not avaiable"})	
			else:
				answer.append({"update_answer":update_answer, "answer":answer[ID-1]})
				return jsonify({"update_answer":update_answer, "answer":answer[ID-1]})
		except:
				return jsonify({"message":"Answer ID does not exist"})
api.add_resource(Update_answer, '/stackoverflowlite.com/api/v1/answer/<int:ID>')

if __name__=="__main__":
	app.run(debug=True)

