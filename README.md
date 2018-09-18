[![Build Status](https://travis-ci.org/milamish/stackOverflow-lite-challenge2-3.svg?branch=challenge3)](https://travis-ci.org/milamish/stackOverflow-lite-challenge2-3)
[![Maintainability](https://api.codeclimate.com/v1/badges/cfd254b6354576148c47/maintainability)](https://codeclimate.com/github/milamish/stackOverflow-lite-challenge2-3/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/milamish/stackOverflow-lite-challenge2-3/badge.svg?branch=challenge3)](https://coveralls.io/github/milamish/stackOverflow-lite-challenge2-3?branch=challenge3)

# stackOverflow-lite

stackOverflow-lite is a a platform whereby users interact with each other through posting and answering questions

```
features include
```
```
	*post question
	*answer question
	*modify question
	*delete question
	*upvote/downvote a question
	*fetch one question with all answers
	*fetch all question
	*search for a question
```
check <a href= "https://stackoverflowliteapi1.docs.apiary.io/#">here</a> for documentation, you can access
the hosted app on <a href= "https://stacklit2.herokuapp.com/api/v1/">heroku</a> and on<a href= "https://www.pivotaltracker.com/n/projects/2193473">pivortal tracker</a> for the stories.

heroku "https://stacklit2.herokuapp.com/api/v1/" <br>
Apiary documentation "https://stackoverflowliteapi1.docs.apiary.io/#"


<h2><strong>to run this app</strong></h2>

set up database environment for the app
```
install postgress database on your computer
```
create a virtual environment
```
pip install py -3 -m venv venv(for windows)
```
activate virtual environment
```
venv\Scripts\activate(for windows)
```
pip install requirements
```
pip install -r requirements.txt
```
<h2><strong>to set app models</strong></h2>
create database 'stack' with user 'postgres' and password 'milamish8'
start the app (run.py) and the relations will automatically be created on the database


<h2><strong>test the functionality of the endpoints on postman</strong></h2>

functionality              | Endpoint                                                 |      method           |
---------------------------|----------------------------------------------------------|-----------------------|
signup                     | /api/v1/auth/signup                                      |       POST            |
---------------------------|----------------------------------------------------------|-----------------------|
login                      |/api/v1/auth/login                                        |       POST            |
|                          |                                                          |
post question              |/api/v1/questions                                         |       POST            |
|                          |                                                          |
get a question             |/api/v1/question/<int:question_id>                        |       GET             |
|                          |                                                          |
post an answer             |/api/v1/questions/<int:question_id>/answers               |       POST            |
|                          |                                                          |
get an answered question   |/api/v1/questions/<int:question_id>                       |       GET             |
|                          |                                                          |
fetch all questions        |/api/v1/questions                                         |       GET             |
|                          |                                                          |
modify an answer           |api/v1/questions/<int:question_id>/answers/<int:answer_id>|       PUT             |
|                          |                                                          |
delete an question         |/api/v1/questions/<int:question_id>                       |       DELETE          |
|                          |                                                          |
search a quetsion by title |/api/v1/questions/<string:title>                          |       GET             |
|                          |                                                          |
get all questions by a user|/api/v1/allquestions                                      |       GET             |
|                          |                                                          |
