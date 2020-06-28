import os
from flask import Flask
from flask_pymongo import flask_pymongo
from bson.objectid import objectid

# new instance of flask
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'task_manager'  # optional
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')

@app.route('/')
def hello():
    return 'hello world'

if __name__ == "__main__":
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT')), debug=True)
