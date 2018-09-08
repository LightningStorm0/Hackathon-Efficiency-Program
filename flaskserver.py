import os
import datetime
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_sqlalchemy import SQLAlchemy
from secrets_config import FlaskConfig, PostgresConfig

app = Flask(__name__, template_folder='./templates')
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@{}/{}".format(
    PostgresConfig.username,
    PostgresConfig.password,
    PostgresConfig.host, 
    PostgresConfig.db
)

db = SQLAlchemy(app)

class User(db.Model):
    uid = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text)
    tag = db.Column(db.Integer)
    birthday = db.Column(db.Date)
    email = db.Column(db.Text)
    email_confirmed = db.Column(db.Boolean)
    goals = db.relationship('Goal', backref='user')

class Goal(db.Model):
    goal_id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text)
    done_by = db.Column(db.DateTime)
    uid = db.Column(db.BigInteger, db.ForeignKey('user.uid'))
    steps = db.relationship('Step', backref='goal')

class Step(db.Model):
    step_id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text)
    desc = db.Column(db.Text)
    done = db.Column(db.Boolean)
    goal_id = db.Column(db.BigInteger, db.ForeignKey('goal.goal_id'))

@app.route("/")
def home():
    return render_template('about/login.html')

@app.route("/about")
def about():
    return render_template('about/about.html')

@app.route("/goals")
def goals():
    goals = User.query.filter_by(uid=238164492943360).first().goals
    return render_template('app/Goals.html', goals=goals)

@app.route("/activities")
def activities():
    return render_template('app/Activities.html')

@app.route("/intellect")
def intellect():
    return render_template('app/Intellect.html')

if __name__ == "__main__":
    app.secret_key = FlaskConfig.secret_key
    app.run(port=5432, host="0.0.0.0")
