import os
from flask import Flask
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
""" get env.py file for keys/URIs"""
from os import path
if path.exists("env.py"):
    import env
    print("env.py imported")

# new instance of flask
app = Flask(__name__)

app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

mongo = PyMongo(app)  # create an instance of PyMongo


@app.route('/')
def hello():
    return 'hello world'

@app.route('/get_tasks')
def get_tasks():
    return 'here are your tasks!'


if __name__ == "__main__":
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT')), debug=True)