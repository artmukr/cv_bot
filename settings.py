import logging

from flask import Flask
from flask_restful import Api
from pymongo import MongoClient


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

api = Api(app)

client = MongoClient('localhost')
db = client.mydb
table = db.vacancies

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

if __name__ == '__main__':
    from main import *
    app.run(port=5000)
