from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api= Api(app)

users = {}
query=[]
answer=[]
answers={"answer":answer}
queries={"query":query}

class Signup(Resource):
    def post(self):
        name= request.get_json()['name']
        emailaddress= request.get_json()['emailaddress']
        password= request.get_json()['password']
        username=request.get_json()['username']
        users.update({username:{"name": name,"emailadress": emailaddress,"password": password}})
        return jsonify({"name": name},{"username":username})
api.add_resource(Signup,'/stackoverflowlite.com/api/v1/auth/signup' )

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
api.add_resource(Login,'/stackoverflowlite.com/api/v1/auth/login')

class PostQuestion(Resource):
    def post(self):
        question=request.get_json()["question"]
        query.append({"question":question})
        return jsonify({"question":question})
api.add_resource(PostQuestion,'/stackoverflowlite.com/api/v1/question')


if __name__=="__main__":
	app.run(debug=True)


