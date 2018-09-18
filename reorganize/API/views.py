from flask import Flask, jsonify, request, Blueprint
from flask_restful import Api, Resource
from API import api, app

main = Blueprint('main', __name__)

class Home(Resource):
    def get(self):
        return jsonify({"message":"welcome, you can post or answer a question", "Apiary documentation": "https://stackoverflowliteapi1.docs.apiary.io/#"})
api.add_resource(Home,'/api/v1/')