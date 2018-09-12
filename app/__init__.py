from flask import Flask, request, jsonify, Blueprint
from flask_restful import Api, Resource
import flask_restful
import psycopg2

app = Flask(__name__)
app.config ['SECRET_KEY'] = 'mish'
api=Api(app)

from users.views import users
from queries.views import queries
from views import main
from models import *
from tests.test_questions import *
from tests.test_users import *

app.register_blueprint(users)
app.register_blueprint(queries)
app.register_blueprint(main)
