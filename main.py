from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eMution.db'

db = SQLAlchemy(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


@app.cli.command('db_seed')
def db_seed():
    user_1 = User(id='001', first_name='Admin',
                 last_name='iit',
                 email='admin@iit.ac.lk',
                 password=1234,
                 fav_genre='pop',
                 language='english',
                 fav_Artists='Ariana Grande')


    db.session.add(user_1)
    db.session.commit()
    print('Database Seeded')


@app.route('/')
def hello_eMution():
    return jsonify(message='Welcome to eMution'), 200


@app.route('/not_found')
def not_found():
    return jsonify(message='That resource was not found'), 404


# database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String)
    fav_genre = db.Column(db.String)
    language = db.Column(db.String)
    fav_Artists = db.Column(db.String)


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email already exists.'), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="User created successfully."), 201


if __name__ == '__main__':
    app.run()
