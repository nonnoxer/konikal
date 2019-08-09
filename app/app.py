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

db.execute("""CREATE TABLE IF NOT EXISTS users(
    id SERIAL,
    username VARCHAR PRIMARY KEY,
    password VARCHAR NOT NULL,
    email VARCHAR,
    admin BOOLEAN
    );""")

@app.route("/")
def root():
    session["route"] = "/"
    return render_template("page.html", body="Main page", custom = config.custom)


@app.route("/login")
def login():
    return render_template("page.html", body=Markup(config.body["login"]), custom=config.custom)


@app.route("/signup")
def signup():
    return render_template("page.html", body=Markup(config.body["signup"]), custom=config.custom)

@app.route("/user/<username>")
def user(username):
    if "user" in session:
        if session["user"] == username:
            return render_template("page.html", body=Markup(config.body["user"]), custom=config.custom)
        else:
            session["error"] = "alert('Invalid route');"
            return redirect(session["route"])
    else:
        session["error"] = "alert('Invalid route');"
        return redirect(session["route"])

@app.route("/logined", methods=["POST"])
def logined():
    username = request.form["username"]
    password = request.form["password"]
    users = db.execute(
        "SELECT * FROM users WHERE username=:username AND password=:password;",
        {"username": username, "password": password}
        ).fetchall()
    if users == []:
        session["error"] = "alert('Invalid login');"
        return redirect(session["route"])
    else:
        if users[0][3]:
            session["admin"] = username
        session["user"] = username
        return redirect(session["route"])

@app.route("/signuped", methods=["POST"])
def signuped():
    username = request.form["username"]
    password = request.form["password"]
    users = db.execute(
        "SELECT * FROM users WHERE username=:username;",
        {"username": username}
    ).fetchall()
    if users == []:
        db.execute(
            "INSERT INTO users (username, password) VALUES (:username, :password);",
            {"username": username, "password": password}
            )
        db.commit()
        session["user"] = username
        return redirect(session["route"])
    else:
        session["error"] = "alert('Invalid signup');"
        return redirect(session["route"])

@app.route("/logouted")
def logouted():
    session.pop("user")
    return redirect(session["route"])

@app.route("/test")
def test():
    result = db.execute("SELECT * FROM users;").fetchall()
    return str(result)

if __name__ == "__main__":
    app.run(debug=True)
