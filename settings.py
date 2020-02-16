import logging

from flask import Flask
from flask_restful import Api
from pymongo import MongoClient


app = Flask(__name__)
# app.config['MONGO_URI'] = 'mongodb:///localhost:27017/vacancies'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

api = Api(app)

client = MongoClient('localhost')
db = client.mydb
table = db.vacancies

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)

if __name__ == '__main__':
    from main import *
    app.run(port=5000)
