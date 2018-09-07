from flask import Flask
from flask import jsonify
from flask import request
from flask_restful import Api, Resource
import unittest
import json


import app
from app import *


class TestQuestions(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()

	#test homepage
	def test_Home(self):
		self.assertEqual(app.test_client().get('/api/v1/',).status_code,200)

	#test signup status codes
	def test_register(self):
		response=(app.test_client().get('/stackoverflowlite.com/api/v1/auth/signup',).status_code,200)
		response2=(app.test_client().get('/stackoverflowlite.com/api/v1/auth/signup',).status_code,409)
		
	#test user login for unregistered user
	def test_unregistered_user_login(self):
		username = "milamish"
		password = "mish"
		users = {"username": username, "password": password}
		user=json.dumps({"username":"milamish","password":"Milamish8"})
		header={"content-type":"application/json"}
		res=app.test_client().post( '/stackoverflowlite.com/api/v1/auth/login',data=user, headers=header )
		result = json.loads(res.data.decode())
		self.assertEqual(res.status_code, 500)
		self.assertTrue(result['message'], "Internal Server Error")

	#test username conflict
	def test_username_conflict(self):
		users={}
		name = "caro"
		username = "carolyn"
		emailaddress = "caro@live.com"
		password = "Mimish6"
		message= "user already exists"
		users.update({"username":username,"name":name,"emailaddress":emailaddress, "password":password})
		register=json.dumps({"username": username,"name": name,"emailaddress":emailaddress, "password": password})
		header={"content-type":"application/json"}
		res=app.test_client().post( '/stackoverflowlite.com/api/v1/auth/signup',data=register, headers=header )
		result = json.loads(res.data.decode())
		users.update({"username":username,"name":name,"emailaddress":emailaddress, "password":password})
		register=json.dumps({"username": username,"name": name,"emailaddress":emailaddress, "password": password})
		header={"content-type":"application/json"}
		res=app.test_client().post( '/stackoverflowlite.com/api/v1/auth/signup',data=register, headers=header )
		result = json.loads(res.data.decode())
		self.assertEqual(res.status_code, 200)
		self.assertEqual(result['message'],"user exists")

	#test user signup
	def test_signedup(self):
		sign_data=json.dumps({"username":"sharlyne2454", "password":"Milamish8", "emailaddress":"shal5@yahoo.com",
			"name":"Mildred"})
		header={"content-type":"application/json"}
		signed_up=app.test_client().post('/stackoverflowlite.com/api/v1/auth/signup',data=sign_data, headers=header)
		result= json.loads(signed_up.data.decode())
		self.assertEqual(signed_up.status_code, 200)
		self.assertEqual(result,{'name': 'Mildred', 'username': 'sharlyne2454'})
		
	#test password and username match
	def test_password_username_match(self):
		users = {"username":"mish", "password":"milamish"}
		username = "carolyn"
		password = "Mimish6"
		sign_data=json.dumps({"password":password,"username":username})
		header={"content-type":"application/json"}
		match=app.test_client().post('/stackoverflowlite.com/api/v1/auth/login',data=sign_data, headers=header)
		result= json.loads(match.data.decode())
		self.assertEqual(match.status_code, 500)
		self.assertEqual(result['message'], "Internal Server Error")

	#makes sure no empty questions are posted
	def test_post_question(self):
		title = "databases"
		question="we are good"
		question_data=json.dumps({"title":title, "question":question})
		header={"content-type":"application/json"}
		question_asked=app.test_client().post('/stackoverflowlite.com/api/v1/question',data=question_data, headers=header)
		result= json.loads(question_asked.data.decode())
		self.assertEqual(question_asked.status_code, 200)
		self.assertTrue(question,result)

	#test for fetching a single question
	def test_get_question(self):
		self.assertEqual(app.test_client().get('/stackoverflowlite.com/api/v1/question/<int:ID>',).status_code,404)

	#test for posting an answer to a question
	def test_answer_question(self):
		answer = []
		query = []
		question = "we are good"
		query.append({"question":question})
		post_answer = "s"
		answer.append({"post_answer":post_answer, "question":query[0]})
		question_data=json.dumps({"post_answer":post_answer,"query":query[0]})
		header={"content-type":"application/json"}
		question_answered=app.test_client().post('/stackoverflowlite.com/api/v1/question/<int:ID>/answer',data=question_data, headers=header)
		self.assertEqual(question_answered.status_code,404)
		self.assertEqual(answer, [{'post_answer': 's', 'question': {'question': 'we are good'}}])

	def test_update_answer(self):
		query = []
		answer= []
		question="we are good"
		query.append({"question":question})
		post_answer="hi"
		answer.append({"post_answer":post_answer, "question":query[0]})
		update_answer ="mish"
		answer.append({"update_answer":update_answer, "answer":answer[0]})
		data=json.dumps({"update_answer":update_answer,"answer":answer[0]})
		header={"content-type":"application/json"}
		answer_update=app.test_client().put('/stackoverflowlite.com/api/v1/answer/<int:ID>',data=data, headers=header)
		self.assertEqual(answer_update.status_code,404)
		self.assertEqual(update_answer,"mish")

	#test to make sure the posted question is the same as the received question
	def test_question_entry(self):
		title = "OOP"
		question= "we are good"
		question_data=json.dumps({"title": title, "question":question})
		header={"content-type":"application/json"}
		post_question=app.test_client().post('/stackoverflowlite.com/api/v1/question',data=question_data, headers=header)
		result= json.loads(post_question.data.decode())
		self.assertEqual(result['message'],'question is available')

	def test_get_one_question(self):
		query=[]
		title = "codes"
		question = "is it tough?"
		query.append({"title":title, "question":question})
		get_data = json.dumps({"query":query[0]})
		header={"content-type":"application/json"}
		question_fetched = app.test_client().get('/stackoverflowlite.com/api/v1/question/<int:ID>',data=get_data, headers=header)
		self.assertEqual(question_fetched.status_code, 404)
		
	
	#test for delete function
	def test_delete_question(self):
		ID = "1"
		data = json.dumps({"query":ID})
		header = {"content-type":"application/json"}
		delete_question = app.test_client().delete('/stackoverflowlite.com/api/v1/question/<int:ID>',data=data, headers=header)
		self.assertEqual(delete_question.status_code,404)

	#testing for the users data structure
	def test_users(self):
		users = {}
		name = "mildred"
		username = "milamish"
		emailaddress = "milamish@live.com"
		password = "Mimish6"
		users.update({username:{"name": name, "emailaddress": emailaddress, "password": password}})
		register=json.dumps({"username":username,"password": password, "name": name, "emailaddress": emailaddress})
		header={"content-type":"application/json"}
		res=app.test_client().post( '/stackoverflowlite.com/api/v1/auth/signup',data=register, headers=header )
		result = json.loads(res.data.decode())
		self.assertEqual(res.status_code, 200)
		self.assertEqual(result,{"name": name,"username":username})

	#test query list structure
	def test_query(self):
		query=[]
		title = "codes"
		question = "is it tough?"
		query.append({"title":title, "question":question})
		quest = json.dumps({"title":title, "question":question})
		header={"content-type":"application/json"}
		response = app.test_client().post('/stackoverflowlite.com/api/v1/question',data = quest, headers = header)
		result = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 200)
		self.assertEqual(result['message'],'question is available')

if __name__ =='__main__':
    unittest.main()