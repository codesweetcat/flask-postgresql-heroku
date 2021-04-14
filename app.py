
from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL?sslmode=require').replace('postgres://', 'postgresql://')
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
    return os.environ.get("DATABASE_URL")


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


@app.route("/new", methods=['POST', 'GET'])
def new():

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            # role
            # username
            # password
            # extra_properties
            # email
            # new_user = User(role=data['role'], username=data['username'],
            #                 password=data['password'], extra_properties=data['extra_properties'],
            #                 email=data['email']
            #                 )

            new_user = User(name=data['name'],
                            email=data['email']
                            )
            db.session.add(new_user)
            db.session.commit()
            return {"message": f"car {new_user.username} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        users = User.query.all()
        results = [
            {
                # "role": user.role,
                # "username": user.username,
                # "password": user.password,
                # "extra_properties": user.extra_properties,
                "email": user.email,
                "name": user.name

            } for user in users]

        return {"count": len(results), "users": results}


# @app.route("/user/<username>")
# def check_user(username):
#     user = User.query.filter_by(name=username).first()
#     if user is None:
#         return {"message": "error", "email": "No user found"}
#     else:
#         return user.email
#         return {"message": "success", "email": user.email}
#

if __name__ == '__main__':
    app.run()
