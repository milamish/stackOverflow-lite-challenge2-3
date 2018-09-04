from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import datetime

app = Flask(__name__)
api= Api(app)

users = {}

class Signup(Resource):
    def post(self):
        name= request.get_json()['name']
        emailaddress= request.get_json()['emailaddress']
        password= request.get_json()['password']
        username=request.get_json()['username']
        users.update({username:{"name": name,"emailadress": emailaddress,"password": password}})
        return jsonify({"name": name},{"username":username})
api.add_resource(Signup,'/api/v1/auth/signup' )

class Login(Resource):
    def post(self):
        username=request.get_json()["username"]
        password=request.get_json()["password"]
        if username in users:
            if password==users[username]["password"]:
            	return jsonify({"message":"succesfuly logged in"})
                        
            else:
                return jsonify({"message": "your password is wrong"})
        else:
            return jsonify({"message": "check your username"})
api.add_resource(Login,'/api/v1/auth/login')

class UpdateAnswer(Resource):
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
api.add_resource(UpdateAnswer, '/stackoverflowlite.com/api/v1/answer/<int:ID>')

if __name__=="__main__":
	app.run(debug=True)