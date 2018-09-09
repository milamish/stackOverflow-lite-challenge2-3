import psycopg2
from users.views import *
from __init__ import *

connection = psycopg2.connect(host ='localhost',user='postgres',password='milamish8',dbname='questions')
cursor= connection.cursor()

def table():
	connection= psycopg2.connect(host ='localhost',user='postgres',password='milamish8',dbname='questions')
	with connection.cursor() as cursor:
		cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id serial PRIMARY KEY,\
			fname VARCHAR(100) NOT NULL,\
			lname VARCHAR(100) NOT NULL,\
			username VARCHAR(100) NOT NULL,\
			emailaddress VARCHAR(50) NOT NULL,\
			password VARCHAR(100) NOT NULL,\
			reg_date timestamp DEFAULT CURRENT_TIMESTAMP)")
		cursor.execute("CREATE TABLE IF NOT EXISTS questions(question_id serial PRIMARY KEY, \
			title VARCHAR(100) NOT NULL, \
			question VARCHAR(100) NOT NULL, \
			question_date timestamp DEFAULT CURRENT_TIMESTAMP,\
			user_id INT)")
		cursor.execute("CREATE TABLE IF NOT EXISTS answers(answer_id serial PRIMARY KEY, \
			answer VARCHAR(100) NOT NULL, \
			question_id INT REFERENCES questions(question_id) ON DELETE CASCADE ,\
			answer_date timestamp DEFAULT CURRENT_TIMESTAMP,\
			user_id INT)")
	connection.commit()

def check_username(username):
	cursor.execute("SELECT * FROM  users WHERE username=%s;",(username,))

def check_email_address(emailaddress):
	cursor.execute("SELECT * FROM  users WHERE emailaddress='"+emailaddress+"';",(emailaddress,))

def register_user(fname, lname, username, emailaddress, phash):
	cursor.execute("INSERT INTO users(fname,lname,emailaddress,password,username) VALUES\
		('"+fname+"','"+lname+"','"+emailaddress+"','"+str(phash)+"','"+username+"');",((fname,lname,username,phash,emailaddress),))

def check_question(question):
	cursor.execute("SELECT * FROM  questions WHERE question=%s;",(question,))

def post_question(title, question, user_id):
	cursor.execute("INSERT INTO questions(title,question,user_id) \
		VALUES('"+title+"','"+question+"', '"+str(user_id)+"');",((title,question, user_id),))
