import os
import datetime
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort

app = Flask(__name__, template_folder='./templates')

@app.route("/")
def home():
    return render_template('login.html')

@app.route("/goals")
def goals():
    return render_template('Goals.html')

@app.route("/activities")
def activities():
    return render_template('Activities.html')

@app.route("/intellect")
def intellect():
    return render_template('Intellect.html')

if __name__ == "__main__":
    app.secret_key = "whatever"
    app.run(port=5432, host="0.0.0.0")
