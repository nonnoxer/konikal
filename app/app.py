import os
from flask import Flask, session, render_template, request, redirect, Markup
from flask_session import Session
from sqlalchemy import create_engine, Boolean, Column, ForeignKey, Integer, Sequence, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence("users_sequence"), primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    elevation = Column(Integer, nullable=False, default=0)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, Sequence("posts_sequence"), primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    date = Column(Integer, nullable=False)
    content = Column(String, nullable=False)

class Page(Base):
    __tablename__ = "pages"
    id = Column(Integer, Sequence("pages_sequence"), primary_key=True)
    title = Column(String, nullable=False, unique=True)
    content = Column(String, nullable=False)

Base.metadata.create_all(engine)

if db.query(User).all() == []:
    db.add(User(username="admin", password="password", elevation=4))
db.commit()

@app.route("/")
def root():
    session["route"] = "/"
    return render_template("page.html", body="Main page", custom=config.custom)


@app.route("/login")
def login():
    if "user" not in session:
        return render_template("page.html", body=Markup(config.page["login"]), custom=config.custom)
    else:
        session["error"] = "alert('Already logged in');"
        return redirect("/route")

@app.route("/signup")
def signup():
    if "user" not in session:
        return render_template("page.html", body=Markup(config.page["signup"]), custom=config.custom)
    else:
        session["error"] = "alert('Already logged in');"
        return redirect("/route")

@app.route("/user/<username>")
def user(username):
    if "user" in session:
        if session["user"] == username:
            return render_template("page.html", body=Markup(config.page["user"].format(user=session["user"])), custom=config.custom)
        else:
            session["error"] = "alert('Invalid route');"
            return redirect("/route")
    else:
        session["error"] = "alert('Invalid route');"
        return redirect("/route")

@app.route("/logined", methods=["POST"])
def logined():
    username = request.form["username"]
    password = request.form["password"]
    users = db.query(User).filter_by(username=username, password=password).all()
    if users == []:
        session["error"] = "alert('Invalid login');"
        return redirect("/route")
    else:
        if users[0].elevation != 0:
            session["elevation"] = users[0].elevation
        session["user"] = username
        return redirect("/route")

@app.route("/signuped", methods=["POST"])
def signuped():
    username = request.form["username"]
    password = request.form["password"]
    users = db.query(User).filter_by(username=username).all()
    if users == []:
        db.add(User(username=username, password=password))
        db.commit()
        session["user"] = username
        return redirect("/route")
    else:
        session["error"] = "alert('Invalid signup');"
        return redirect("/route")

@app.route("/logouted")
def logouted():
    if "user" in session:
        session.pop("user")
    if "elevation" in session:
        session.pop("elevation")
    return redirect("/route")

@app.route("/route")
def route():
    if "route" in session:
        return redirect(session["route"])
    else:
        return redirect("/")

@app.route("/test")
def test():
    result = db.query(User).all()
    return str(result)

@app.route("/admin")
def admin():
    if "elevation" in session:
        return render_template("admin.html", page="Dashboard")
    else:
        return render_template("admin.html", page="Admin Login", display=Markup(config.admin["login"]))

@app.route("/adminlogined", methods=["POST"])
def adminlogined():
    username = request.form["username"]
    password = request.form["password"]
    session["elevation"] = username
    return redirect("/admin")

if __name__ == "__main__":
    app.run(debug=True) 
