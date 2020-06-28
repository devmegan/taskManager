import os
from flask import Flask, render_template, redirect, request, url_for
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
coll = mongo.db.tasks

@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    # redirect to existing template called tasks.html and call everything in tasks collection from mongo
    return render_template("tasks.html", tasks=coll.find())


if __name__ == "__main__":
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT')), debug=True)
