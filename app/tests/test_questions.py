from __init__ import app, Api
import unittest
import json
import re

import os, sys
sys.path.insert(0, os.path.abspath(".."))


class Test_questions(unittest.TestCase):
	def setUp(self):
		''''mish'''
	
	def test_post_question(self):
		title = "peolpe"
		question = "how is you"
		question_data = json.dumps({"title": title, "question": question})
		header = {"content-type": "application/json"}
		question_asked = app.test_client().post('/api/v1/questions', data=question_data, headers=header)
		result = json.loads(question_asked.data.decode())
		self.assertEqual(question_asked.status_code, 200)
		self.assertEqual(result['message'],"Token is missing")

	def test_get_question(self):
		get_question = json.dumps({"message": ""})
		self.assertEqual(app.test_client().get('/api/v1/question/<int:question_id>',).status_code, 404)

	def test_get_answers(self):
		get_question = json.dumps({"message": ""})
		self.assertEqual(app.test_client().get('/api/v1/questions/<int:question_id>',).status_code, 200)

	def test_answer_question(self):
		answer = "how is you"
		question_data = json.dumps({"answer": "how is you"}) 
		header = {"content-type": "application/json"}
		question_answered = app.test_client().post('/api/v1/questions/<int:question_id>/answers', data=question_data, headers=header)
		self.assertEqual(question_answered.status_code, 404)

	def test_question_entry(self):
		question = ""
		title = ""
		sign_data = json.dumps({"title": title, "question": question})
		header = {"content-type": "application/json"}
		postquestion = app.test_client().post('/api/v1/questions', data=sign_data, headers=header)
		result = json.loads(postquestion.data.decode())
		self.assertEqual(postquestion.status_code, 200)
		self.assertEqual(result['message'], "Token is missing")

	def test_modify_answer(self):
		answer = "peolple"
		mod_data = json.dumps({"answer": ""})
		header = {"content-type": "application/json"}
		modify_answer = app.test_client().put('/api/v1/questions/<int:question_id>/answers/<int:answer_id>',data=mod_data, headers=header)
		self.assertEqual(modify_answer.status_code, 404)
		self.assertEqual(answer, answer)

if __name__ == '__main__':
	unittest.main()