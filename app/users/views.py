from flask import Flask
from flask import Blueprint
from flask import jsonify
from flask import request
from flask_restful import Api
from flask_restful import Resource
from functools import wraps
import psycopg2
import re
import hashlib
import jwt
import datetime

from __init__ import *
from models import *

users = Blueprint('users', __name__)

def pwhash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_pwhash(password, hash):
    if pwhash(password) == hash:
        return True
    return False

#this class allows a user to create an account by signing up
class Register(Resource):
	def post(self):
		fname = request.get_json()['fname'].strip()
		lname = request.get_json()['lname'].strip()
		username = request.get_json()['username'].strip()
		emailaddress = request.get_json()['emailaddress'].strip()
		password = request.get_json()['password'].strip()
		repeatpassword = request.get_json()['repeatpassword'].strip()
		phash = pwhash(password)

		if not fname:
			return {"message" : "you must provide a name"}
		if not username:
			return {"message" : "you must provide a username"}
		if len(username) < 5 or len(username) > 22:
			return {"message" : "username must be between 5 and 22 characters"}

		if not password:
			return{"message" : "you must provide a password"}
			
		if password != repeatpassword:
			return {"message" : "password do not match"}

		if len(password) < 9 or len(password) > 20:
			return {"message" : "password must be between 9 and 20 characters"}

		if not re.match('\d.*[A-Z]|[A-Z].*\d', password):
			return {"message" : "password must contain a capital letter and a number"}

		if not emailaddress:
			return {"message" : "you must provide an email"}

		if not re.match("[^@]+@[^@]+\.[^@]+", emailaddress):
			return {"message" : "email address not valid"}
			
		try:
			check_username(username)
			if cursor.fetchone() is not None:
				return{"message" : "username taken"}, 409
			check_email_address(emailaddress)
			if cursor.fetchone() is not None:
				return {"message" : "emailaddress exists"}
			else:
				register_user(fname, lname, username, emailaddress, phash)
		except:
			return {"message" : "unable to register!"}, 500
		connection.commit()
		return {"fname":fname,"lname" : lname, "emailaddress" : emailaddress, "username" : username}
		
api.add_resource(Register, '/api/v1/auth/signup')

#this class allows a user with an account to login
class Login(Resource):
	def post(self):
		username = request.get_json()['username'].strip()
		password = request.get_json()['password'].strip()
		
		if not username:
			return {"message" : "please enter a username"}
		if not password:
			return {"message" : "please enter a password"}
		check_username(username)
		result = cursor.fetchone()
		if result is None :
			return {"message" : "your username is wrong"}
		else:
			if check_pwhash(password, result[5]):
				token = jwt.encode({'username':username, 'user_id':result[0], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
				return {"message" : "succesfuly logged in", 'token' : token.decode ('UTF-8')}
			else:
				return {'message' : 'invalid password or username'}			
		connection.commit()
		return {"message":"check your login details"}
api.add_resource(Login, '/api/v1/auth/login')
