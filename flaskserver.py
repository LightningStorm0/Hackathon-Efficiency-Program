import os
import datetime
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort

app = Flask(__name__, template_folder='./templates')

@app.route("/")
def home():
    return render_template('about/login.html')

@app.route("/about")
def about():
    return render_template('about/about.html')

@app.route("/goals")
def goals():
    goals = [{"name":"clean room","done_by":"tonight","steps":[{"name":"pick up socks","descrition":"","done":True},{"name":"make bed","descrition":"","done":False}]}]
    return render_template('app/Goals.html', goals=goals)

@app.route("/activities")
def activities():
    return render_template('app/Activities.html')

@app.route("/intellect")
def intellect():
    return render_template('app/Intellect.html')

if __name__ == "__main__":
    app.secret_key = "whatever"
    app.run(port=5432, host="0.0.0.0")
