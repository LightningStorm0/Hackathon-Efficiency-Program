import os
import datetime
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SelectField, DateField
from flask_sqlalchemy import SQLAlchemy
from secrets_config import FlaskConfig, PostgresConfig
from werkzeug.security import generate_password_hash, check_password_hash
from snowflakes import get_snowflake
import random

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
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    tag = db.Column(db.Integer)
    pw_hash = db.Column(db.Text)
    dob = db.Column(db.Date)
    gender = db.Column(db.Enum('Male', 'Female', 'Other', name='gender'))
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

class RegistrationForm(Form):
    username = StringField('Username:', [validators.Length(min=4, max=25)])
    first_name = StringField('First Name:')
    last_name = StringField('Last Name:')
    dob = DateField('Date of Birth:')
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    email = StringField('Email Address:', [validators.Email()])
    password = PasswordField('Create Password:', [
        validators.DataRequired(),
        validators.Length(min=8),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password:')

class SignInForm(Form):
    email = StringField('Email Address:', [validators.Email()])
    password = PasswordField('Password:', [
        validators.DataRequired()
    ])

@app.route("/", methods=['GET','POST'])
def home():
    form = SignInForm(request.form)
    if request.method == 'POST' and form.validate():
        login_user = User.query.filter_by(email=form.email.data).first()
        if check_password_hash(login_user.pw_hash, form.password.data):
            session['uid'] = login_user.uid
            return redirect(url_for('goals'))
    return render_template('about/login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        new_user = User(
            uid=get_snowflake('user'),
            name=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            tag=random.randint(1,9999),
            dob=form.dob.data,
            gender=form.gender.data,
            email=form.email.data,
            pw_hash=generate_password_hash(form.password.data),
            email_confirmed=False
        )
        print(new_user)
        db.session.add(new_user)
        flash('Registration complete.')
        return redirect(url_for('home'))

    return render_template('about/register.html', form=form)

@app.route("/about")
def about():
    return render_template('about/about.html')

@app.route("/goals")
def goals():
    goals = User.query.filter_by(uid=session['uid']).first().goals
    return render_template('app/Goals.html', goals=goals)

@app.route("/activities")
def activities():
    return render_template('app/Activities.html')

@app.route("/intellect")
def intellect():
    questions = [{"id":"129","date": datetime.date(2018, 9, 8),"type":"riddle","question":"This five letter word becomes shorter when you add two letters to it. What is the word?","answer":"Short"},{"id":"128","date": datetime.date(2018, 9, 8),"type":"math","question":"Factor: 6x^2 - 11x - 10","answer":"(2x-5)(3x+2)"}]
    questions2=[]
    for i in questions:
        if i["date"] == datetime.date.today():
            questions2.append(i)
    return render_template('app/Intellect.html', q2=questions2)

@app.route("/logout")
def logout():
    session.pop('uid', None)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.secret_key = FlaskConfig.secret_key
    app.run(port=5432, host="0.0.0.0")
