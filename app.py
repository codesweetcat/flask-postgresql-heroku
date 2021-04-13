from flask import Flask

app = Flask(__name__)

from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

app.config['SQLALCHEMY_DATABASE_URL'] = os.environ.get("DATABASE_URL")

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)

    def __init__(self,  name, email):
        # self.id = id
        self.name = name
        self.email = email

    def __repr__(self):
        return '<id {}>'.format(self.id)


# db.init_app()


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


@app.route("/new", methods=['POST', 'GET'])
def new():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return {"message": f"car {user.name} has been created successfully."}


@app.route("/user/<username>")
def users(username):
    user = User.query.filter_by(name=username).first()
    if user is None:
        return {"message": "error", "email": "No user found"}
    else:
        return user.email
        return {"message": "success", "email": user.email}


if __name__ == '__main__':
    app.run()
