from flask import *
import unittest
import json
import re

import os,sys
sys.path.insert(0, os.path.abspath(".."))

from __init__ import *

class Test_Users(unittest.TestCase):
	def setUp(self):
		pass
		
	def test_Home(self):
		home=json.dumps({"message":"you can post your question"})
		self.assertEqual(app.test_client().get('/api/v1/',).status_code,200)

	def test_login(self):
		m=app.test_client()
		response=(m.post('/api/v1/auth/login',).status_code, 500)
		sign_data=json.dumps({})

	def test_unregistered_user_login(self):
		noneuser=json.dumps({"username":"milithree","password":"Milamish8"})
		header={"content-type":"application/json"}
		res=app.test_client().post( '/api/v1/auth/login',data=noneuser, headers=header )
		result = json.loads(res.data.decode())
		self.assertEqual(res.status_code, 400)
		self.assertEqual(result['message'], "your username is wrong")

	def test_signedup(self):
		sign_data=json.dumps({"username":"sharlyne2454", "password":"Milamish8", "emailaddress":"shal5@yahoo.com",
		 "repeatpassword":"Milamish8", "fname":"Mildred", "lname":"mill"})
		header={"content-type":"application/json"}
		signedup=app.test_client().post('/api/v1/auth/signup',data=sign_data, headers=header)
		result= json.loads(signedup.data.decode())
		self.assertEqual(signedup.status_code, 409)
		self.assertEqual(result['message'], "username taken")

	def test_password_match(self):
		password = "Milamish8"
		repeatpassword = "Milamish8"
		sign_data=json.dumps({"password":"Milamish8","repeatpassword":"Milamish8"})
		header={"content-type":"application/json"}
		passwordmatch=app.test_client().post('/api/v1/auth/signup',data=sign_data, headers=header)
		result= json.loads(passwordmatch.data.decode())
		self.assertTrue(password==repeatpassword, True)

	def test_wrong_password(self):
		password = "Milamish8"
		repeatpassword = "Milam"
		username = "sharlyne2454"
		fname = "mildred"
		lname = "Amiani"
		emailaddress = "milamish@gmail.com"
		sign_data=json.dumps({"username":username, "password":password, "emailaddress":emailaddress,
		 "repeatpassword":repeatpassword, "fname":fname, "lname":fname})
		header={"content-type":"application/json"}
		signedup=app.test_client().post('/api/v1/auth/signup',data=sign_data, headers=header)
		result= json.loads(signedup.data.decode())
		sign_in=json.dumps({"password":password,"username":username})
		header={"content-type":"application/json"}
		passwordmatch=app.test_client().post('/api/v1/auth/login',data=sign_in, headers=header)
		result2= json.loads(passwordmatch.data.decode())
		self.assertEqual(result['message'],"password do not match")
		self.assertEqual(result2['message'], "succesfuly logged in")
		
	def test_password_characters(self):
		password = "Milamish89"
		length = (len(password) < 9 or len(password) > 20)
		match= re.match('\d.*[A-Z]|[A-Z].*\d',password)
		sign_data=json.dumps({"password":"Milamish89"})
		header={"content-type":"application/json"}
		passwordcharacter=app.test_client().post('/api/v1/auth/signup',data=sign_data, headers=header)
		result= json.loads(passwordcharacter.data.decode())
		self.assertEqual(length, False)
		self.assertEqual(match, match)


if __name__ =='__main__':
    unittest.main()
