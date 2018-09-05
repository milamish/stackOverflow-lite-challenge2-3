from flask import *
from flask_restful import Api, Resource
import unittest
import json

import app
from app import *

class Test_questions(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()

	#test user login for unregistered user
	def test_unregistered_user_login(self):
		user=json.dumps({"username":"milamish","password":"Milamish8"})
		header={"content-type":"application/json"}
		res=app.test_client().post( '/stackoverflowlite.com/api/v1/auth/login',data=user, headers=header )
		result = json.loads(res.data.decode())
		self.assertEqual(res.status_code, 200)
		self.assertEqual(result['message'], "check your username")

	#test user signup
	def test_signedup(self):
		sign_data=json.dumps({"username":"sharlyne2454", "password":"Milamish8", "emailaddress":"shal5@yahoo.com",
			"name":"Mildred"})
		header={"content-type":"application/json"}
		signedup=app.test_client().post('/stackoverflowlite.com/api/v1/auth/signup',data=sign_data, headers=header)
		result= json.loads(signedup.data.decode())
		self.assertEqual(signedup.status_code, 200)
		self.assertEqual(result,[{'name': 'Mildred'}, {'username': 'sharlyne2454'}])
		
	#test password and username match
	def test_password_username_match(self):
		password = "Milamish8"
		username = "Milamish"
		sign_data=json.dumps({"password":password,"username":username})
		header={"content-type":"application/json"}
		match=app.test_client().post('/stackoverflowlite.com/api/v1/auth/login',data=sign_data, headers=header)
		result= json.loads(match.data.decode())
		self.assertEqual(match.status_code, 200)
		self.assertEqual(result['message'],"check your username")

	#makes sure no empty questions are posted
	def test_post_question(self):
		question="we are good"
		question_data=json.dumps({"question":question})
		header={"content-type":"application/json"}
		question_asked=app.test_client().post('/stackoverflowlite.com/api/v1/question',data=question_data, headers=header)
		result= json.loads(question_asked.data.decode())
		self.assertEqual(question_asked.status_code, 200)
		self.assertTrue(question,result)

	#test for fetching a single question
	def test_get_question(self):
		get_question=json.dumps({"message":""})
		self.assertEqual(app.test_client().get('/stackoverflowlite.com/api/v1/question/<int:ID>',).status_code,404)

	#test for posting an answer to a question
	def test_answer_question(self):
		answer="s"
		question_data=json.dumps({"answer":answer})
		header={"content-type":"application/json"}
		question_answered=app.test_client().post('/stackoverflowlite.com/api/v1/question/<int:ID>/answer',data=question_data, headers=header)
		self.assertEqual(question_answered.status_code,404)
		self.assertTrue(answer)

	#test to make sure the posted question is the same as the received question
	def test_question_entry(self):
		question= "we are good"
		question_data=json.dumps({"question":question})
		header={"content-type":"application/json"}
		postquestion=app.test_client().post('/stackoverflowlite.com/api/v1/question',data=question_data, headers=header)
		result= json.loads(postquestion.data.decode())
		self.assertEqual(result,{'question': 'we are good'})
	
	#test for delete function
	def test_delete_question(self):
		ID = "1"
		data = json.dumps({"query":ID})
		header = {"content-type":"application/json"}
		delete_question = app.test_client().delete('/stackoverflowlite.com/api/v1/question/<int:ID>',data=data, headers=header)
		self.assertEqual(delete_question.status_code,404)
	


if __name__ =='__main__':
    unittest.main()