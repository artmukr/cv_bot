import logging

from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb:///localhost:27017/vacancies'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

api = Api(app)
mongo = PyMongo(app)

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)
