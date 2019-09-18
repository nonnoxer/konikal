import os
from datetime import date as datetime

from flask import Flask, Markup, redirect, render_template, request, session
from flask_session import Session
from sqlalchemy import (
    Column, Integer, Sequence, String, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

import config

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
    title = Column(String, nullable=False, unique=True)
    slug = Column(String, nullable=False, unique=True)
    author = Column(String, nullable=False)
    year = Column(String, nullable=False)
    month = Column(String, nullable=False)
    date = Column(String, nullable=False)
    content = Column(String, nullable=False)


class Page(Base):
    __tablename__ = "pages"
    id = Column(Integer, Sequence("pages_sequence"), primary_key=True)
    title = Column(String, nullable=False, unique=True)
    slug = Column(String, nullable=False, unique=True)
    content = Column(String, nullable=False)


Base.metadata.create_all(engine)

if db.query(User).all() == []:
    db.add(User(username="admin", password="password", elevation=4))
if db.query(Post).all() == []:
    db.add(Post(
        title="Hello world!",
        slug="hello-world",
        author="Konikal",
        year=datetime.today().strftime("%Y"),
        month=datetime.today().strftime("%m"),
        date=datetime.today().strftime("%d"),
        content="""{"ops":[{"insert":"Welcome to Konikal. This is your first po
            st. Edit or delete it, then start posting!"}]}"""
        ))
if db.query(Page).all() == []:
    db.add(Page(
        title="Home",
        slug="home",
        content="""{"ops":[{"insert":"Welcome to Konikal. This is your first po
            st. Edit or delete it, then start posting!"}]}"""
    ))
db.commit()

# Main page
@app.route("/")
def root():
    session["route"] = "/"
    return render_template("page.html", body="Main page", custom=config.custom)

# Redirect to previous content page after certain actions
@app.route("/route")
def route():
    if "route" in session:
        return redirect(session["route"])
    else:
        return redirect("/")

# Login page
@app.route("/login")
def login():
    if "user" not in session:
        return render_template(
            "page.html",
            body=Markup(config.page["login"]), 
            custom=config.custom)
    else:
        session["error"] = "alert('Invalid login: Already logged in');"
        return redirect("/route")

# Login processing
@app.route("/login/done", methods=["POST"])
def login_done():
    username = request.form["username"]
    password = request.form["password"]
    user = db.query(User).filter_by(
        username=username,
        password=password).first()
    if user is None:
        session["error"] = "alert('Invalid login: Invalid credentials');"
        return redirect("/login")
    else:
        if user.elevation != 0:
            session["elevation"] = user.elevation
        session["user"] = username
        return redirect("/route")

# Signup page
@app.route("/signup")
def signup():
    if "user" not in session:
        return render_template(
            "page.html",
            body=Markup(config.page["signup"]),
            custom=config.custom)
    else:
        session["error"] = "alert('Invalid signup: Already logged in');"
        return redirect("/route")

# Signup processing
@app.route("/signup/done", methods=["POST"])
def signup_done():
    username = request.form["username"]
    password = request.form["password"]
    users = db.query(User).filter_by(username=username).all()
    if users == []:
        db.add(User(username=username, password=password))
        db.commit()
        session["user"] = username
        return redirect("/route")
    else:
        session["error"] = "alert('Invalid signup: User already exists');"
        return redirect("/signup")

# Logout processing
@app.route("/logout/done")
def logout_done():
    if "user" in session:
        session.pop("user")
    if "elevation" in session:
        session.pop("elevation")
    return redirect("/route")

# User actions page
@app.route("/user/<username>")
def user_username(username):
    user = db.query(User).filter_by(username=username).first()
    if user is not None:
        if "user" in session:
            if session["user"] == username:
                session["route"] = "/user/" + username
                return render_template(
                    "page.html",
                    body=Markup(config.page["user"].format(
                            user=session["user"])),
                    custom=config.custom)
            else:
                session["error"] = """
                    alert('Invalid request: Permission required');
                    """
                return redirect("/route")
        else:
            session["error"] = "alert('Invalid request: Not logged in');"
            return redirect("/route")
    else:
        session["error"] = "alert('Invalid request: User does not exist');"
        return redirect("/route")

# Edit username processing
@app.route("/editusername/done", methods=["POST"])
def editusername_done():
    if "user" in session:
        username = request.form["username"]
        new_username = request.form["new_username"]
        if session["user"] == username:
            user = db.query(User).filter_by(username=new_username).all()
            if user == []:
                db.query(User).filter_by(
                    username=username).first().username = new_username
                db.commit()
                session["user"] = new_username
                return redirect("/user/" + new_username)
            else:
                session["error"] = "alert('Invalid request: Username taken');"
                return redirect("/user/" + username)
        else:
            session["error"] = "alert('Invalid request: Permission required');"
            return redirect("/route")
    else:
        session["error"] = "alert('Invalid request: Not logged in');"
        return redirect("/route")

# Edit password processing
@app.route("/editpassword/done", methods=["POST"])
def editpassword_done():
    if "user" in session:
        username = request.form["username"]
        password = request.form["password"]
        if session["user"] == username:
            db.query(User).filter_by(
                username=username).first().password = password
            db.commit()
            return redirect("/user/" + username)
        else:
            session["error"] = "alert('Invalid request: User does not exist');"
    else:
        session["error"] = "alert('Invalid request: Not logged in');"

# Delete user processing
@app.route("/deleteuser/done", methods=["POST"])
def deleteuser_done():
    if "user" in session:
        username = request.form["username"]
        if session["user"] == username:
            db.delete(db.query(User).filter_by(username=username).first())
            db.commit()
            session["route"] = "/"
            return redirect("/logout/done")
        else:
            session["error"] = "alert('Invalid request: User does not exist');"
    else:
        session["error"] = "alert('Invalid request: Not logged in');"

# Admin page
@app.route("/admin")
def admin():
    if "elevation" in session:
        session["route"] = "/admin"
        return render_template(
            "admin.html",
            page="Dashboard",
            display=Markup(config.admin["admin"]))
    else:
        return render_template(
            "admin.html",
            page="Admin Login",
            display=Markup(config.admin["login"]))

# Admin login processing
@app.route("/admin/login/done", methods=["POST"])
def admin_login_done():
    username = request.form["username"]
    password = request.form["password"]
    user = db.query(User).filter_by(
        username=username,
        password=password).first()
    if user is None:
        session["error"] = "alert('Invalid login');"
        return redirect("/admin")
    else:
        session["user"] = username
        if user.elevation != 0:
            session["elevation"] = user.elevation
            return redirect("/admin")
        else:
            session["error"] = "alert('Invalid elevation');"
            return redirect("/route")

# All users page
@app.route("/admin/users")
def admin_users():
    users = db.query(User).all()
    if users != []:
        display = """
            <table class="table">
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Password</th>
                    <th>Elevation</th>
                    <th></th>
                </tr>
        """
        for i in users:
            display += """
                <tr>
                    <td>{id}
                    <td>{username}</td>
                    <td>{password}</td>
                    <td>{elevation}</td>
                    <td><a href="/admin/users/{username}">Edit user</a></td>
                </tr>
            """.format(
                id=i.id,
                username=i.username,
                password=i.password,
                elevation=i.elevation)
        display += "</table>"
    else:
        display = "<p>No users</p>"
    return render_template(
        "admin.html",
        page="Users",
        display=Markup(config.admin["users"].format(display=display)))

# Edit user page
@app.route("/admin/users/<username>")
def admin_users_username(username):
    if "elevation" in session:
        if session["elevation"] == 4:
            user = db.query(User).filter_by(username=username).first()
            display = """
                <h1>{username}</h1>
                <h2>Edit username</h2>
                <form action="/editusernamed" method="POST">
                    <input type="text" name="username" value="{username}"
                        readonly hidden>
                    <input type="text" name="newname" 
                        placeholder="New username">
                    <br>
                    <input type="submit" value="Update">
                </form>
                <h2>Edit password</h2>
                <form action="/editpassworded" method="POST">
                    <input type="text" name="username" value="{username}"
                        readonly hidden>
                    <input type="text" name="password"
                        placeholder="New password">
                    <br>
                    <input type="submit" value="Update">
                </form>
                <h2>Edit elevation</h2>
                <form action="/admin/users/editelevationed" method="POST">
                    <input type="text" name="username" value="{username}" 
                        readonly hidden>
                    <input type="range" id="elevationrange" name="elevation"
                        value="{elevation}"
                        min="0" max="4" 
                        onchange="updateelevationvalue()">
                    <p id="elevationvalue">{elevation}</p>
                    <input type="submit" value="Update">
                </form>
                <h2>Delete user</h2>
                <form action="/deleteusered" method="POST">
                    <input type="text" name="username" value="{username}"
                        readonly hidden>
                    <input type="submit" value="Delete">
                </form>
                """.format(username=username, elevation=user.elevation)
            return render_template(
                "admin.html",
                page=username,
                display=Markup(config.admin["user"].format(display=display)))
        else:
            session["error"] = "alert('Invalid elevation');"
            return redirect("/route")
    else:
        session["error"] = "alert('Invalid elevation');"
        return redirect("/route")

# All posts page
@app.route("/admin/posts")
def admin_posts():
    posts = db.query(Post).all()
    if posts != []:
        display = """
            <table class="table">
                <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Slug</th>
                    <th>Author</th>
                    <th>Date</th>
                    <th></th>
                </tr>
        """
        for i in posts:
            display += """
                <tr>
                    <td>{id}</td>
                    <td>{title}</td>
                    <td>{slug}</td>
                    <td>{author}</td>
                    <td>{date}</td>
                    <td><a href="/admin/posts/{slug}">Edit post</a></td>
                </tr>
            """.format(
                id=i.id,
                title=i.title,
                slug=i.slug,
                author=i.author,
                date="{d}-{m}-{y}".format(
                    d=i.date,
                    m=i.month,
                    y=i.year))
        display += "</table>"
    else:
        display = "<p>No posts</p>"
    return render_template(
        "admin.html",
        page="Posts",
        display=Markup(config.admin["posts"].format(display=display)))

@app.route("/admin/posts/new")
def admin_posts_new():
    return render_template(
        "admin.html",
        page="New Post",
        display=Markup(config.admin["posts_new"]))

@app.route("/admin/posts/new/done", methods=["POST"])
def admin_posts_new_done():
    title = request.form["title"]
    slug = request.form["slug"]
    author = request.form["author"]
    if author == "":
        author = session["user"]
    date = request.form["date"]
    if date == "":
        today = datetime.today()
        date = today.strftime("%Y-%m-%d")
    date = date.split("-")
    year = date[0]
    month = date[1]
    date = date[2]
    content = request.form["content"]
    db.add(Post(title=title, slug=slug, author=author, year=year, month=month, date=date, content=content))
    db.commit()
    return redirect("/admin")

@app.route("/admin/posts/<slug>")
def admin_posts_slug(slug):
    post = db.query(Post).filter_by(slug=slug).first()
    display = """
        <form action="/admin/posts/{slug}/edit/done" method="POST" id="editor">
            <input type="text" name="title" placeholder="Author" value="{title}"><br>
            <input type="text" name="slug" placeholder="Author" value="{slug}"><br>
            <input type="name" name="author" placeholder="Author" value="{author}"><br>
            <input type="date" name="date" value="{date}"><br>
            <div id="editor-container" onkeyup="updatecontent()"></div>
            <textarea form="editor" id="content" name="content" readonly hidden>{content}</textarea>
            <input type="submit" value="Update">
        </form>
        <form action="/admin/posts/deletepost/done" method="POST">
            <input type="text" name="slug" value="{slug}" readonly hidden><br>
            <input type="submit" value="Delete post" class="red">
        </form>
        """.format(title=post.title, slug=post.slug, author=post.author, date="{y}-{m}-{d}".format(y=post.year, m=post.month, d=post.date), content=post.content)
    return render_template("admin.html", page=post.title, display=Markup(config.admin["post"].format(display=display)))

@app.route("/admin/posts/<slug>/edit/done", methods=["POST"])
def admin_posts_slug_edit_done(slug):
    title = request.form["title"]
    new_slug = request.form["slug"]
    author = request.form["author"]
    if author == "":
        author = session["user"]
    date = request.form["date"]
    if date == "":
        today = datetime.today()
        date = today.strftime("%Y-%m-%d")
    date = date.split("-")
    year = date[0]
    month = date[1]
    date = date[2]
    content = request.form["content"]
    post = db.query(Post).filter_by(slug=slug).first()
    post.title= title
    post.slug = new_slug
    post.author = author
    post.date = date
    post.content = content
    db.commit()
    return redirect("/admin")

@app.route("/admin/posts/deletepost/done", methods=["POST"])
def admin_posts_deletepost_done():
    slug = request.form["slug"]
    db.delete(db.query(Post).filter_by(slug=slug).first())
    db.commit()
    return redirect("/admin")

#All pages page
@app.route("/admin/pages")
def admin_pages():
    pages = db.query(Page).all()
    if pages != []:
        display = """
            <table class="table">
                <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Slug</th>
                    <th><th>
                </tr>
        """
        for i in pages:
            display += """
                <tr>
                    <td>{id}</td>
                    <td>{title}</td>
                    <td>{slug}</td>
                    <td><a href="/admin/pages/{slug}">Edit page</a></td>
                </tr>
            """.format(id=i.id, title=i.title, slug=i.slug)
        display += "</table>"
    else:
        display = "<p>No pages</p>"
    return render_template("admin.html", page="Pages", display=Markup(config.admin["pages"].format(display=display)))

@app.route("/admin/pages/new")
def admin_pages_new():
    return render_template("admin.html", page="New Page", display=Markup(config.admin["pages_new"]))

@app.route("/admin/pages/new/done", methods=["POST"])
def admin_pages_new_done():
    title = request.form["title"]
    slug = request.form["slug"]
    content = request.form["content"]
    db.add(Page(title=title, slug=slug, content=content))
    db.commit()
    return redirect("/admin")

@app.route("/admin/pages/<slug>")
def admin_pages_slug(slug):
    post = db.query(Page).filter_by(slug=slug).first()
    display = """
        <form action="/admin/pages/{slug}/edit/done" method="POST" id="editor">
            <input type="text" name="title" placeholder="Author" value="{title}"><br>
            <input type="text" name="slug" placeholder="Author" value="{slug}"><br>
            <div id="editor-container" onkeyup="updatecontent()"></div>
            <textarea form="editor" id="content" name="content" readonly hidden>{content}</textarea>
            <input type="submit" value="Update">
        </form>
        <form action="/admin/pages/deletepage/done" method="POST">
            <input type="text" name="slug" value="{slug}" readonly hidden><br>
            <input type="submit" value="Delete page" class="red">
        </form>
        """.format(title=post.title, slug=post.slug, content=post.content)
    return render_template("admin.html", page=post.title, display=Markup(config.admin["page"].format(display=display)))

@app.route("/admin/pages/<slug>/edit/done", methods=["POST"])
def admin_pages_slug_edit_done(slug):
    title = request.form["title"]
    new_slug = request.form["slug"]
    content = request.form["content"]
    page = db.query(Page).filter_by(slug=slug).first()
    page.title = title
    page.slug = new_slug
    page.content = content
    db.commit()
    return redirect("/admin")

@app.route("/admin/pages/deletepage/done", methods=["POST"])
def admin_pages_deletepage_done():
    slug = request.form["slug"]
    db.delete(db.query(Page).filter_by(slug=slug).first())
    db.commit()
    return redirect("/admin")

@app.route("/test")
def test():
    users = db.query(User).all()
    posts = db.query(Post).all()
    pages = db.query(Page).all()
    post = db.query(Post).filter_by(slug="hello-world").first()
    #return str(users) + "\n" + str(posts) + "\n" + str(pages)
    return post.year

if __name__ == "__main__":
    app.run(debug=True)
