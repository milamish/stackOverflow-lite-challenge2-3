import unittest
import json
import re
import jwt
import datetime

import os, sys
sys.path.insert(0, os.path.abspath(".."))

from  API import app 
from API.queries.views import queries


class Test_questions(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
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
        header = {"content-type": "application/json"}
        get_question = app.test_client().get('/api/v1/question/1', headers=header)
        result = json.loads(get_question.data.decode())
        self.assertEqual(result['message'], "Token is missing")

    def test_get_answers(self):
        get_question = json.dumps({"message": ""})
        self.assertEqual(app.test_client().get('/api/v1/questions/<int:question_id>',).status_code, 200)

    def test_answer_question(self):
        answer = "how is you"
        question_data = json.dumps({"answer": answer})
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

    def test_delete_answer(self):
        header = {"content-type": "application/json"}
        delete_question = app.test_client().delete('/api/v1/questions/1', headers=header)
        result = json.loads(delete_question.data.decode())
        self.assertEqual(delete_question.status_code, 200)
        self.assertEqual(result['message'], "Token is missing")

    def test_search_question(self):
        header = {"content-type": "application/json"}
        search_question = app.test_client().delete('/api/v1/questions/1', headers=header)
        result = json.loads(search_question.data.decode())
        self.assertEqual(search_question.status_code, 200)
        self.assertEqual(result['message'], "Token is missing")

    def test_question_conflict(self):
        username = "mish"
        result = "1"
        token = jwt.encode({'username': username, 'user_id': result[0], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
        token2= json.dumps(token.decode ('UTF-8'))
        question = "is it rainning?"
        title = "Weather"
        sign_data = json.dumps({"title": title, "question": question})
        header = {"content-type": "application/json", "x-access-token": token}
        postquestion = app.test_client().post('/api/v1/questions', data=sign_data, headers=header)
        result = json.loads(postquestion.data.decode())
        sign_data2 = json.dumps({"title": title, "question": question})
        postquestion2 = app.test_client().post('/api/v1/questions', data=sign_data2, headers=header)
        result2 = json.loads(postquestion2.data.decode())
        self.assertEqual(postquestion.status_code, 409)
        self.assertEqual(result, {'this question exists': 'is it rainning?'})
        
        
if __name__ == '__main__':
    unittest.main()