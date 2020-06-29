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
coll_tasks = mongo.db.tasks
coll_cats = mongo.db.categories


@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    # redirect to existing template called tasks.html and call everything in tasks collection from mongo
    return render_template("tasks.html", tasks=coll_tasks.find())


@app.route('/add_task')
def add_tasks():
    """ allow user to add new task """
    return render_template("addtasks.html", categories=coll_cats.find())


@app.route('/insert_task', methods=['POST'])
def insert_task():
    """ insert the new task into mongodb """
    coll_tasks.insert_one(request.form.to_dict())  # form submitted as request object, so we send the request to a new task as a dictionary
    return redirect(url_for('get_tasks'))


@app.route('/edit_task/<task_id>')  # edit_task recieves task_id as part of its routing parameter
def edit_task(task_id):
    """ display task in editable form and allow user to edit """
    task_to_fetch = coll_tasks.find_one({"_id": ObjectId(task_id)})  # convert task id into bson, then find id in mongo db that matches it
    all_categories = coll_cats.find()
    return render_template("edittask.html", task=task_to_fetch, categories=all_categories)


@app.route('/updating_task/<task_id>', methods=["POST"])  # post hides values from url bar when being sent
def update_task(task_id):
    coll_tasks.update({'_id': ObjectId(task_id)},
    {
        # fetch values from the edit task form to send across
        'task_name':request.form.get('task_name'),
        'category_name':request.form.get('category_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent':request.form.get('is_urgent')
    })
    return redirect(url_for('get_tasks'))


@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    coll_tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))


@app.route('/categories')
def get_categories():
    return render_template('categories.html', categories=coll_cats.find())


@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    cat_to_fetch = coll_cats.find_one({"_id": ObjectId(category_id)})
    return render_template("editcategory.html", category=cat_to_fetch)


@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    coll_cats.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))


if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)