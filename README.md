[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/c26c9b378e37231fc690)
[![Build Status](https://travis-ci.org/milamish/stackOverflow-lite-challenge2-3.svg?branch=challenge2)](https://travis-ci.org/milamish/stackOverflow-lite-challenge2-3)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Maintainability](https://api.codeclimate.com/v1/badges/cfd254b6354576148c47/maintainability)](https://codeclimate.com/github/milamish/stackOverflow-lite-challenge2-3/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/milamish/stackOverflow-lite-challenge2-3/badge.svg?branch=challenge2)](https://coveralls.io/github/milamish/stackOverflow-lite-challenge2-3?branch=challenge2)

# stackOverflow-lite
is an app that allows users to post questions, answer questions, modify answers and delete their questions

install virtual environment
````

py -3 -m venv venv (for windows)
````
activate virtual environment
```
venv\Scripts\activate
```
install flask
```
pip install flask
```
intall requirements.txt
```
pip install -r requirements.txt
```
run the code

open postman to test on the functionality of the endpoints
```
home '/api/v1/'
```
```
signup'/stackoverflowlite.com/api/v1/auth/signup'
```
```
login '/stackoverflowlite.com/api/v1/auth/login'
```
```
post question '/stackoverflowlite.com/api/v1/question'
```
```
fetch one question '/stackoverflowlite.com/api/v1/question/<int:ID>'
```
```
fetch all questions '/stackoverflowlite.com/api/v1/question'
```
```
post answer '/stackoverflowlite.com/api/v1/question/<int:ID>/answer'
```
```
fetch questions with answers '/stackoverflowlite.com/api/v1/answers'
```
```
update answer '/stackoverflowlite.com/api/v1/answer/<int:ID>'
```
```
delete question '/stackoverflowlite.com/api/v1/question/<int:ID>'
```
```
copy the url then post it on postman

check on endpoint functionality by typing the required routes on postman and the methods as well
```