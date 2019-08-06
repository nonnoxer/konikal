import os
from flask import Flask, session, render_template, request, redirect, Markup
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import config
config.env()

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def root():
    return render_template("page.html", body="Main page", custom = config.custom)


@app.route("/login")
def login():
    return render_template("page.html", body=Markup(config.body["login"]), custom=config.custom)


@app.route("/signup")
def signup():
    return render_template("page.html", body=Markup(config.body["signup"]), custom=config.custom)

@app.route("/logined", methods=["POST"])
def logined():
    username = request.form["username"]
    password = request.form["password"]
    return redirect("/")

@app.route("/signuped", methods=["POST"])
def signuped():
    username = request.form["username"]
    password = request.form["password"]
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
