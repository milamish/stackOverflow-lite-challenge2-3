from flask import Flask, request, jsonify, Blueprint,render_template
from flask_restful import Api, Resource
from flask_cors import CORS
import flask_restful
import psycopg2

app = Flask(__name__)
app.config ['SECRET_KEY'] = 'mish'
api = Api(app)
CORS(app)

from API.users.views import users
from API.queries.views import queries
from API.views import main

app.register_blueprint(users)
app.register_blueprint(queries)
app.register_blueprint(main)


@app.route("/")
def index():
    return render_template("index.html")

