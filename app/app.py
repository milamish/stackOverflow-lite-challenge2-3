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

class GetQuestions(Resource):
    def get(self):
    	try:
    		if queries is None:
    			return jsonify({"message":"no questions available"})
    		else:
    			return jsonify(queries)
    	except:
    		return jsonify({"message":"unable to fetch questions"})
api.add_resource(GetQuestions, '/stackoverflowlite.com/api/v1/question')

class getOneQuestion(Resource):
	def get(self, ID):
		try:
			if ID in query is None:
				return jsonify({"message":"question cannot be found"})
			else:
				return jsonify(query[ID-1])
		except:
			return jsonify({"message":"question ID does not exist"})
			
api.add_resource(getOneQuestion, '/stackoverflowlite.com/api/v1/question/<int:ID>')


if __name__=="__main__":
	app.run(debug=True)