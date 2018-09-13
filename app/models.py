import psycopg2

connection = psycopg2.connect(host='localhost', user='postgres', password='milamish8', dbname='stack')
cursor = connection.cursor()


def table():
	connection = psycopg2.connect(host='localhost', user='postgres', password='milamish8', dbname='stack')
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


class RegisterUser():
	def check_username(username):
		cursor.execute("SELECT * FROM  users WHERE username=%s;",(username,))

	def check_email_address(emailaddress):
		cursor.execute("SELECT * FROM  users WHERE emailaddress='"+emailaddress+"';",(emailaddress,))

	def register_user(fname, lname, username, emailaddress, phash):
		cursor.execute("INSERT INTO users(fname,lname,emailaddress,password,username) VALUES\
			('"+fname+"', '"+lname+"', '"+emailaddress+"', '"+str(phash)+"', '"+username+"');", ((fname,lname,username,phash,emailaddress),))

	
class Questions():
	def post_question(title, question, user_id):
		cursor.execute("INSERT INTO questions(title,question,user_id) \
			VALUES('"+title+"', '"+question+"', '"+str(user_id)+"');", ((title,question, user_id),))

	def get_question(question_id):
		cursor.execute("SELECT * FROM questions WHERE questions.question_id='"+str(question_id)+"';",(question_id,))

	def post_answer(answer, user_id, question_id):
		cursor.execute("INSERT INTO answers(answer,user_id,question_id) \
			VALUES('"+answer+"', '"+str(user_id)+"', '"+str(question_id)+"');", ((answer, user_id, question_id),))
	def get_answers(question_id):
		cursor.execute("SELECT * FROM answers WHERE question_id ='"+str(question_id)+"';", (question_id,))
		
	def get_all_questions():
		cursor.execute("SELECT * FROM questions;")

	def get_all_questions_by_a_user(user_id):
		cursor.execute("SELECT * FROM questions WHERE user_id = '"+str(user_id)+"';", (user_id,))

	def get_user_id_and_question_id(question_id, user_id):
		cursor.execute("SELECT * FROM answers WHERE answers.question_id = '"+str(question_id)+"'\
		and answers.user_id ='"+str(user_id)+"';", ((question_id, user_id),))

	def get_user_id_and_answer_id(answer_id, question_id, user_id):
		cursor.execute("SELECT * FROM answers WHERE answers.question_id = '"+str(question_id)+"' \
			and answers.answer_id ='"+str(answer_id)+"'\
		and answers.user_id ='"+str(user_id)+"';",((answer_id, question_id, user_id),))
		
	def modify_answer(question_id,answer,answer_id):
		cursor.execute("update answers SET answer = '"+answer+"' WHERE question_id = '"+str(question_id)+"' \
			and answer_id = '"+str(answer_id)+"';", ((answer, answer_id, question_id),))

	def delete_question(user_id, question_id):
		cursor.execute("DELETE FROM questions WHERE questions.question_id= '"+str(question_id)+"'\
		and questions.user_id = '"+str((user_id))+"';", ((user_id, question_id),))

	def get_user_id(question_id, user_id):
		cursor.execute("SELECT * FROM questions WHERE questions.question_id = '"+str(question_id)+"'\
		and questions.user_id = '"+str((user_id))+"'", ((user_id,question_id),))

	def check_question(question):
		cursor.execute("SELECT * FROM  questions WHERE question = %s;",(question,))

	def get_questions_by_title(title):
		cursor.execute("SELECT * FROM  questions WHERE title = %s;", (title,))