import os
from flask import Flask

# new instance of flask
app = Flask(__name__)


@app.route('/')
def hello():
    return 'hello world'


if __name__ == "__main__":
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT')), debug=True)
