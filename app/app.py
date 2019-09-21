import os
from datetime import date as datetime

from flask import Flask, Markup, redirect, render_template, request, session
from flask_session import Session
from sqlalchemy import Column, Integer, Sequence, String, create_engine
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
    precedence = Column(Integer, nullable=False)
    content = Column(String, nullable=False)


Base.metadata.create_all(engine)

if (
    db.query(User).all() == []
    and db.query(Post).all() == []
    and db.query(Page).all() == []
):
    db.add(User(username="admin", password="password", elevation=4))
    db.add(
        Post(
            title="Hello world!",
            slug="hello-world",
            author="Konikal",
            year=datetime.today().strftime("%Y"),
            month=datetime.today().strftime("%m"),
            date=datetime.today().strftime("%d"),
            content="""{"ops":[{"insert":"Welcome to Konikal. This is your first post. Edit or delete it, then start posting!"}]}""",
        )
    )
    db.add(
        Page(
            title="Home",
            slug="home",
            precedence="1",
            content="""{"ops":[{"insert":"Welcome to Konikal. This is your home page. Edit or delete it, then start posting!"}]}""",
        )
    )
db.commit()

###############################################################################

# Main page
@app.route("/")
def root():
    session["route"] = "/"
    pagebar = ""
    pages = db.query(Page).order_by(Page.precedence.desc()).all()
    for i in pages:
        pagebar += """
            <li class="nav-item active">
                <a class="nav-link" href="/{slug}">{title}</a>
            </li>
            """.format(
            title=i.title, slug=i.slug
        )
    home = db.query(Page).filter_by(slug="home").first()
    if home is not None:
        return render_template(
            "page.html",
            pagebar=Markup(config.pagebar["home"].format(pagebar=pagebar)),
            body=Markup(
                config.page["page"].format(title=home.title, content=home.content)
            ),
            custom=config.custom,
        )
    else:
        body = ""
        posts = (
            db.query(Post)
            .order_by(
                Post.year.desc(), Post.month.desc(), Post.date.desc(), Post.id.desc()
            )
            .all()
        )
        if posts != []:
            for i in posts:
                body += """
                    <tr>
                        <td><a href="/posts/{year}/{month}/{date}/{slug}">{title}</a></td>
                        <td>By {author}</td>
                        <td><a href="/posts/{year}/{month}/{date}">{date}</a>-<a href="/posts/{year}/{month}">{month}</a>-<a href="/posts/{year}">{year}</a></td>
                    </tr>
                    """.format(
                    title=i.title,
                    slug=i.slug,
                    author=i.author,
                    year=i.year,
                    month=i.month,
                    date=i.date,
                )
        else:
            body = "No posts"
        return render_template(
            "page.html",
            pagebar=Markup(config.pagebar["no_home"].format(pagebar=pagebar)),
            body=Markup(config.page["posts"].format(page="All Posts", body=body)),
            custom=config.custom,
        )


# Redirect route
@app.route("/route")
def route():
    if "route" in session:
        if session["route"].find("/user/") != -1:
            return redirect("/")
        else:
            return redirect(session["route"])
    else:
        return redirect("/")


# All posts page
@app.route("/posts")
def posts():
    body = ""
    posts = (
        db.query(Post)
        .order_by(Post.year.desc(), Post.month.desc(), Post.date.desc(), Post.id.desc())
        .all()
    )
    pagebar = ""
    pages = db.query(Page).order_by(Page.precedence.desc()).all()
    for i in pages:
        pagebar += """
            <li class="nav-item active">
                <a class="nav-link" href="/{slug}">{title}</a>
            </li>
            """.format(
            title=i.title, slug=i.slug
        )
    home = db.query(Page).filter_by(slug="home").first()
    if posts != []:
        for i in posts:
            body += """
                <tr>
                    <td><a href="/posts/{year}/{month}/{date}/{slug}">{title}</a></td>
                    <td>By {author}</td>
                    <td><a href="/posts/{year}/{month}/{date}">{date}</a>-<a href="/posts/{year}/{month}">{month}</a>-<a href="/posts/{year}">{year}</a></td>
                </tr>
                """.format(
                title=i.title,
                slug=i.slug,
                author=i.author,
                year=i.year,
                month=i.month,
                date=i.date,
            )
    else:
        body = "No posts"
    if home is not None:
        pagebar = Markup(config.pagebar["home"].format(pagebar=pagebar))
    else:
        pagebar = Markup(config.pagebar["no_home"].format(pagebar=pagebar))
    session["route"] = "/posts"
    return render_template(
        "page.html",
        pagebar=pagebar,
        body=Markup(config.page["posts"].format(page="All Posts", body=body)),
        custom=config.custom,
    )


# Year posts page
@app.route("/posts/<year>")
def posts_year(year):
    body = ""
    posts = (
        db.query(Post)
        .filter_by(year=year)
        .order_by(Post.month.desc(), Post.date.desc(), Post.id.desc())
        .all()
    )
    pagebar = ""
    pages = db.query(Page).order_by(Page.precedence.desc()).all()
    for i in pages:
        pagebar += """
            <li class="nav-item active">
                <a class="nav-link" href="/{slug}">{title}</a>
            </li>
            """.format(
            title=i.title, slug=i.slug
        )
    home = db.query(Page).filter_by(slug="home").first()
    if posts != []:
        for i in posts:
            body += """
                <tr>
                    <td><a href="/posts/{year}/{month}/{date}/{slug}">{title}</a></td>
                    <td>By {author}</td>
                    <td><a href="/posts/{year}/{month}/{date}">{date}</a>-<a href="/posts/{year}/{month}">{month}</a>-<a href="/posts/{year}">{year}</a></td>
                </tr>
                """.format(
                title=i.title,
                slug=i.slug,
                author=i.author,
                year=year,
                month=i.month,
                date=i.date,
            )
    else:
        body = "No posts"
    if home is not None:
        pagebar = Markup(config.pagebar["home"].format(pagebar=pagebar))
    else:
        pagebar = Markup(config.pagebar["no_home"].format(pagebar=pagebar))
    session["route"] = "/posts/{year}".format(year=year)
    return render_template(
        "page.html",
        pagebar=pagebar,
        body=Markup(config.page["posts"].format(page=year, body=body)),
        custom=config.custom,
    )


# Month posts page
@app.route("/posts/<year>/<month>")
def posts_year_month(year, month):
    body = ""
    posts = (
        db.query(Post)
        .filter_by(year=year, month=month)
        .order_by(Post.date.desc(), Post.id.desc())
        .all()
    )
    pagebar = ""
    pages = db.query(Page).order_by(Page.precedence.desc()).all()
    for i in pages:
        pagebar += """
            <li class="nav-item active">
                <a class="nav-link" href="/{slug}">{title}</a>
            </li>
            """.format(
            title=i.title, slug=i.slug
        )
    home = db.query(Page).filter_by(slug="home").first()
    if posts != []:
        for i in posts:
            body += """
                <tr>
                    <td><a href="/posts/{year}/{month}/{date}/{slug}">{title}</a></td>
                    <td>By {author}</td>
                    <td><a href="/posts/{year}/{month}/{date}">{date}</a>-<a href="/posts/{year}/{month}">{month}</a>-<a href="/posts/{year}">{year}</a></td>
                </tr>
                """.format(
                title=i.title,
                slug=i.slug,
                author=i.author,
                year=year,
                month=month,
                date=i.date,
            )
    else:
        body = "No posts"
    if home is not None:
        pagebar = Markup(config.pagebar["home"].format(pagebar=pagebar))
    else:
        pagebar = Markup(config.pagebar["no_home"].format(pagebar=pagebar))
    session["route"] = "/posts/{year}/{month}".format(year=year, month=month)
    return render_template(
        "page.html",
        pagebar=pagebar,
        body=Markup(
            config.page["posts"].format(
                page="{month}-{year}".format(month=month, year=year), body=body
            )
        ),
        custom=config.custom,
    )


# Date posts page
@app.route("/posts/<year>/<month>/<date>")
def posts_year_month_date(year, month, date):
    body = ""
    posts = (
        db.query(Post)
        .filter_by(year=year, month=month, date=date)
        .order_by(Post.id.desc())
        .all()
    )
    pagebar = ""
    pages = db.query(Page).order_by(Page.precedence.desc()).all()
    for i in pages:
        pagebar += """
            <li class="nav-item active">
                <a class="nav-link" href="/{slug}">{title}</a>
            </li>
            """.format(
            title=i.title, slug=i.slug
        )
    home = db.query(Page).filter_by(slug="home").first()
    if posts != []:
        for i in posts:
            body += """
                <tr>
                    <td><a href="/posts/{year}/{month}/{date}/{slug}">{title}</a></td>
                    <td>By {author}</td>
                    <td><a href="/posts/{year}/{month}/{date}">{date}</a>-<a href="/posts/{year}/{month}">{month}</a>-<a href="/posts/{year}">{year}</a></td>
                </tr>
                """.format(
                title=i.title,
                slug=i.slug,
                author=i.author,
                year=year,
                month=month,
                date=date,
            )
    else:
        body = "No posts"
    if home is not None:
        pagebar = Markup(config.pagebar["home"].format(pagebar=pagebar))
    else:
        pagebar = Markup(config.pagebar["no_home"].format(pagebar=pagebar))
    session["route"] = "/posts/{year}/{month}/{date}".format(
        year=year, month=month, date=date
    )
    return render_template(
        "page.html",
        pagebar=pagebar,
        body=Markup(
            config.page["posts"].format(
                page="{date}-{month}-{year}".format(date=date, month=month, year=year),
                body=body,
            )
        ),
        custom=config.custom,
    )


# Post page
@app.route("/posts/<year>/<month>/<date>/<slug>")
def posts_year_month_date_slug(year, month, date, slug):
    post = (
        db.query(Post).filter_by(year=year, month=month, date=date, slug=slug).first()
    )
    pagebar = ""
    pages = db.query(Page).order_by(Page.precedence.desc()).all()
    for i in pages:
        pagebar += """
            <li class="nav-item active">
                <a class="nav-link" href="/{slug}">{title}</a>
            </li>
            """.format(
            title=i.title, slug=i.slug
        )
    home = db.query(Page).filter_by(slug="home").first()
    if post is not None:
        session["route"] = "/posts/{year}/{month}/{date}/{slug}".format(
            year=year, month=month, date=date, slug=slug
        )
        if home is not None:
            pagebar = Markup(config.pagebar["home"].format(pagebar=pagebar))
        else:
            pagebar = Markup(config.pagebar["no_home"].format(pagebar=pagebar))
        return render_template(
            "page.html",
            pagebar=pagebar,
            body=Markup(
                config.page["post"].format(
                    title=post.title,
                    date="""<a href="/posts/{year}/{month}/{date}">{date}</a>-<a href="/posts/{year}/{month}">{month}</a>-<a href="/posts/{year}">{year}</a>""".format(
                        date=date, month=month, year=year
                    ),
                    author=post.author,
                    content=post.content,
                )
            ),
            custom=config.custom,
        )
    else:
        session["error"] = "alert('Invalid route: Post does not exist');"
        return redirect(session["route"])


# Page page
@app.route("/<slug>")
def slug(slug):
    page = db.query(Page).filter_by(slug=slug).first()
    pagebar = ""
    pages = db.query(Page).order_by(Page.precedence.desc()).all()
    for i in pages:
        pagebar += """
            <li class="nav-item active">
                <a class="nav-link" href="/{slug}">{title}</a>
            </li>
            """.format(
            title=i.title, slug=i.slug
        )
    home = db.query(Page).filter_by(slug="home").first()
    if page is not None:
        if slug == "home":
            return redirect("/")
        else:
            session["route"] = "/{slug}".format(slug=slug)
            if home is not None:
                pagebar = Markup(config.pagebar["home"].format(pagebar=pagebar))
            else:
                pagebar = Markup(config.pagebar["no_home"].format(pagebar=pagebar))
            session["route"] = "/{slug}".format(slug=slug)
            return render_template(
                "page.html",
                pagebar=pagebar,
                body=Markup(
                    config.page["page"].format(title=page.title, content=page.content)
                ),
                custom=config.custom,
            )
    else:
        session["error"] = "alert('Invalid route: Page does not exist');"
        return redirect(session["route"])


# Login page
@app.route("/login")
def login():
    if "user" not in session:
        pagebar = ""
        pages = db.query(Page).order_by(Page.precedence.desc()).all()
        for i in pages:
            pagebar += """
                <li class="nav-item active">
                    <a class="nav-link" href="/{slug}">{title}</a>
                </li>
                """.format(
                title=i.title, slug=i.slug
            )
        home = db.query(Page).filter_by(slug="home").first()
        if home is not None:
            pagebar = Markup(config.pagebar["home"].format(pagebar=pagebar))
        else:
            pagebar = Markup(config.pagebar["no_home"].format(pagebar=pagebar))
        return render_template(
            "page.html",
            pagebar=pagebar,
            body=Markup(config.page["login"]),
            custom=config.custom,
        )
    else:
        session["error"] = "alert('Invalid login: Already logged in');"
        return redirect("/route")


# Login processing
@app.route("/login/done", methods=["POST"])
def login_done():
    username = request.form["username"]
    password = request.form["password"]
    user = db.query(User).filter_by(username=username, password=password).first()
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
        pagebar = ""
        pages = db.query(Page).order_by(Page.precedence.desc()).all()
        for i in pages:
            pagebar += """
                <li class="nav-item active">
                    <a class="nav-link" href="/{slug}">{title}</a>
                </li>
                """.format(
                title=i.title, slug=i.slug
            )
        home = db.query(Page).filter_by(slug="home").first()
        if home is not None:
            pagebar = Markup(config.pagebar["home"].format(pagebar=pagebar))
        else:
            pagebar = Markup(config.pagebar["no_home"].format(pagebar=pagebar))
        return render_template(
            "page.html",
            pagebar=pagebar,
            body=Markup(config.page["signup"]),
            custom=config.custom,
        )
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
                pagebar = ""
                pages = db.query(Page).order_by(Page.precedence.desc()).all()
                for i in pages:
                    pagebar += """
                        <li class="nav-item active">
                            <a class="nav-link" href="/{slug}">{title}</a>
                        </li>
                        """.format(
                        title=i.title, slug=i.slug
                    )
                home = db.query(Page).filter_by(slug="home").first()
                session["route"] = "/user/{username}".format(username=username)
                if home is not None:
                    pagebar = Markup(config.pagebar["home"].format(pagebar=pagebar))
                else:
                    pagebar = Markup(config.pagebar["no_home"].format(pagebar=pagebar))
                return render_template(
                    "page.html",
                    pagebar=pagebar,
                    body=Markup(config.page["user"].format(user=session["user"])),
                    custom=config.custom,
                )
            else:
                session[
                    "error"
                ] = """
                    alert('Invalid request: Invalid user');
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
                    username=username
                ).first().username = new_username
                db.commit()
                session["user"] = new_username
                return redirect("/user/" + new_username)
            else:
                session["error"] = "alert('Invalid request: Username taken');"
                return redirect("/user/" + username)
        else:
            session["error"] = "alert('Invalid request: Invalid user');"
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
            db.query(User).filter_by(username=username).first().password = password
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


###############################################################################

# Admin redirect route
@app.route("/admin/route")
def admin_route():
    if "elevation" in session:
        if "admin_route" in session:
            return redirect("/admin_route")
        else:
            return redirect("/admin")
    else:
        session["error"] = "alert('Invalid request: Elevation required');"
        return redirect("/route")


# Admin page
@app.route("/admin")
def admin():
    if "elevation" in session:
        session["admin_route"] = "/admin"
        return render_template(
            "admin.html", page="Dashboard", display=Markup(config.admin["admin"])
        )
    else:
        return render_template(
            "admin.html", page="Admin Login", display=Markup(config.admin["login"])
        )


# Admin login processing
@app.route("/admin/login/done", methods=["POST"])
def admin_login_done():
    username = request.form["username"]
    password = request.form["password"]
    user = db.query(User).filter_by(username=username, password=password).first()
    if user is None:
        session["error"] = "alert('Invalid login');"
        return redirect("/admin")
    else:
        session["user"] = username
        if user.elevation != 0:
            session["elevation"] = user.elevation
            return redirect("/admin")
        else:
            session["error"] = "alert('Invalid request: Elevation required');"
            return redirect("/route")


# All users page
@app.route("/admin/users")
def admin_users():
    if "elevation" in session:
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
                    elevation=i.elevation,
                )
            display += "</table>"
        else:
            display = "<p>No users</p>"
        session["admin_route"] = "/admin/users"
        return render_template(
            "admin.html",
            page="Users",
            display=Markup(config.admin["users"].format(display=display)),
        )
    else:
        session["error"] = "alert('Invalid request: Elevation required');"
        return redirect("/route")


# New user page
@app.route("/admin/users/new")
def admin_users_new():
    if "elevation" in session:
        session["admin_route"] = "/admin/users/new"
        return render_template(
            "admin.html", page="New User", display=Markup(config.admin["users_new"])
        )
    else:
        session["error"] = "alert('Invalid request: Elevation required');"
        return redirect("/route")


# New user processing
@app.route("/admin/users/new/done", methods=["POST"])
def admin_users_new_done():
    if "elevation" in session:
        username = request.form["username"]
        password = request.form["password"]
        elevation = request.form["elevation"]
        users = db.query(User).filter_by(username=username).all()
        if users == []:
            db.add(User(username=username, password=password, elevation=elevation))
            db.commit()
            return redirect("/admin/users")
        else:
            session["error"] = "alert('Invalid request: User already exists');"
            return redirect("/admin/users/new")
    else:
        session["error"] = "alert('Invalid request: Elevation required');"
        return redirect("/route")


# Edit user page
@app.route("/admin/users/<username>")
def admin_users_username(username):
    if "elevation" in session:
        user = db.query(User).filter_by(username=username).first()
        if user is not None:
            display = """
                <h1>Edit user</h1>
                <form action="/admin/users/{username}/edit/done" method="POST">
                    <input type="name" name="username" value="{username}" readonly hidden>
                    <input type="text" name="new_username" value="{username}" placeholder="Username"><br>
                    <input type="password" name="password" value="{password}" placeholder="Password"><br>
                    <input type="range" id="elevationrange" name="elevation" value="{elevation}" min="0" max="4" onchange="updateelevationvalue()">
                    <p id="elevationvalue">{elevation}</p>
                    <input type="submit" value="Update">
                </form>
                <form action="/admin/users/{username}/delete/done" method="POST">
                    <input type="name" name="username" value="{username}" readonly hidden>
                    <input type="submit" value="Delete user" class="red">
                </form>
                """.format(
                username=username, password=user.password, elevation=user.elevation
            )
            session["admin_route"] = "/admin/users/{username}".format(username=username)
            return render_template(
                "admin.html",
                page=username,
                display=Markup(config.admin["user"].format(display=display)),
            )
        else:
            session["error"] = "alert('Invalid request: User does not exist');"
            return redirect("/admin/users")
    else:
        session["error"] = "alert('Invalid elevation');"
        return redirect("/route")


# Edit user processing
@app.route("/admin/users/<username>/edit/done", methods=["POST"])
def admin_users_username_edit_done(username):
    if "elevation" in session:
        new_username = request.form["new_username"]
        password = request.form["password"]
        elevation = request.form["elevation"]
        user = db.query(User).filter_by(username=username).first()
        if user is not None:
            users = db.query(User).filter_by(username=new_username).all()
            if users == []:
                user.username = new_username
            else:
                session["error"] = "alert('Username change failed: Username taken');"
            user.password = password
            user.elevation = elevation
            db.commit()
            return redirect("/admin/users")
        else:
            session["error"] = "alert('Invalid request: User does not exist');"
            return redirect("/admin/route")
    else:
        session["error"] = "alert('Invalid elevation');"
        return redirect("/route")


# Delete user processing
@app.route("/admin/users/<username>/delete/done", methods=["POST"])
def admin_users_username_delete_done(username):
    if "elevation" in session:
        user = db.query(User).filter_by(username=username).first()
        if user is not None:
            db.delete(user)
            db.commit()
            return redirect("/admin/users")
        else:
            session["error"] = "alert('Invalid request: User does not exist');"
            return redirect("/admin/users")
    else:
        session["error"] = "alert('Invalid elevation');"
        return redirect("/route")


# All posts page
@app.route("/admin/posts")
def admin_posts():
    if "elevation" in session:
        posts = (
            db.query(Post)
            .order_by(
                Post.year.desc(), Post.month.desc(), Post.date.desc(), Post.id.desc()
            )
            .all()
        )
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
                    date="{d}-{m}-{y}".format(d=i.date, m=i.month, y=i.year),
                )
            display += "</table>"
        else:
            display = "<p>No posts</p>"
        session["admin_route"] = "/admin/posts"
        return render_template(
            "admin.html",
            page="Posts",
            display=Markup(config.admin["posts"].format(display=display)),
        )
    else:
        session["error"] = "alert('Invalid request: Elevation required');"
        return redirect("/route")


# New post page
@app.route("/admin/posts/new")
def admin_posts_new():
    if "elevation" in session:
        session["admin_route"] = "/admin/posts/new"
        return render_template(
            "admin.html", page="New Post", display=Markup(config.admin["posts_new"])
        )
    else:
        session["error"] = "alert('Invalid request: Elevation required');"
        return redirect("/route")


# New post processing
@app.route("/admin/posts/new/done", methods=["POST"])
def admin_posts_new_done():
    if "elevation" in session:
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
        db.add(
            Post(
                title=title,
                slug=slug,
                author=author,
                year=year,
                month=month,
                date=date,
                content=content,
            )
        )
        db.commit()
        return redirect("/admin/posts")
    else:
        session["error"] = "alert('Invalid request: Elevation required');"
        return redirect("/route")


# Edit post page
@app.route("/admin/posts/<slug>")
def admin_posts_slug(slug):
    if "elevation" in session:
        post = db.query(Post).filter_by(slug=slug).first()
        if post is not None:
            display = """
                <form action="/admin/posts/{slug}/edit/done" method="POST" id="editor">
                    <input type="text" name="title" placeholder="Author" value="{title}
                        "><br>
                    <input type="text" name="slug" placeholder="Author" value="{slug}">
                    <br>
                    <input type="name" name="author" placeholder="Author"
                        value="{author}"><br>
                    <input type="date" name="date" value="{date}"><br>
                    <div id="editor-container" onkeyup="updatecontent()"></div>
                    <textarea form="editor" id="content" name="content" readonly
                        hidden>{content}</textarea>
                    <input type="submit" value="Update">
                </form>
                <form action="/admin/posts/{slug}/delete/done" method="POST">
                    <input type="text" name="slug" value="{slug}" readonly hidden><br>
                    <input type="submit" value="Delete post" class="red">
                </form>
                """.format(
                title=post.title,
                slug=post.slug,
                author=post.author,
                date="{y}-{m}-{d}".format(y=post.year, m=post.month, d=post.date),
                content=post.content,
            )
            session["admin_route"] = "/admin/posts/{slug}".format(slug=slug)
            return render_template(
                "admin.html",
                page=post.title,
                display=Markup(config.admin["post"].format(display=display)),
            )
        else:
            session["error"] = "alert('Invalid request: Post does not exist');"
            return redirect("/admin/posts")
    else:
        session["error"] = "alert('Invalid request: Elevation required');"
        return redirect("/route")


# Edit post processing
@app.route("/admin/posts/<slug>/edit/done", methods=["POST"])
def admin_posts_slug_edit_done(slug):
    if "elevation" in session:
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
        if post is not None:
            post.title = title
            post.slug = new_slug
            post.author = author
            post.year = year
            post.month = month
            post.date = date
            post.content = content
            db.commit()
            return redirect("/admin/posts")
        else:
            session["error"] = "alert('Invalid request: Post does not exist');"
            return redirect("/admin/posts")
    else:
        session["error"] = "alert('Invalid request: Elevation required');"
        return redirect("/route")


# Delete post processing
@app.route("/admin/posts/<slug>/delete/done", methods=["POST"])
def admin_posts_slug_delete_done(slug):
    if "elevation" in session:
        post = db.query(Post).filter_by(slug=slug).first()
        if post is not None:
            db.delete(post)
            db.commit()
            return redirect("/admin/posts")
        else:
            session["error"] = "alert('Invalid request: Post does not exist');"
            return redirect("/admin/posts")
    else:
        session["error"] = "alert('Invalid request: Elevation required');"
        return redirect("/route")


# All pages page
@app.route("/admin/pages")
def admin_pages():
    if "elevation" in session:
        pages = db.query(Page).order_by(Page.precedence.desc()).all()
        if pages != []:
            display = """
                <table class="table">
                    <tr>
                        <th>ID</th>
                        <th>Title</th>
                        <th>Slug</th>
                        <th>Precedence</th>
                        <th><th>
                    </tr>
            """
            for i in pages:
                display += """
                    <tr>
                        <td>{id}</td>
                        <td>{title}</td>
                        <td>{slug}</td>
                        <td>{precedence}</td>
                        <td><a href="/admin/pages/{slug}">Edit page</a></td>
                    </tr>
                """.format(
                    id=i.id, title=i.title, slug=i.slug, precedence=i.precedence
                )
            display += "</table>"
        else:
            display = "<p>No pages</p>"
        session["admin_route"] = "/admin/pages"
        return render_template(
            "admin.html",
            page="Pages",
            display=Markup(config.admin["pages"].format(display=display)),
        )
    else:
        session["error"] = "alert('Invalid request: Elevation required');"
        return redirect("/route")


# New page page
@app.route("/admin/pages/new")
def admin_pages_new():
    if "elevation" in session:
        session["admin_route"] = "admin/pages/new"
        return render_template(
            "admin.html", page="New Page", display=Markup(config.admin["pages_new"])
        )
    else:
        session["error"] = "alert('Invalid request: Elevation required');"
        return redirect("/route")


# New page processing
@app.route("/admin/pages/new/done", methods=["POST"])
def admin_pages_new_done():
    if "elevation" in session:
        title = request.form["title"]
        slug = request.form["slug"]
        precedence = request.form["precedence"]
        content = request.form["content"]
        db.add(Page(title=title, slug=slug, precedence=precedence, content=content))
        db.commit()
        return redirect("/admin/pages")
    else:
        session["error"] = "alert('Invalid request: Elevation required');"
        return redirect("/route")


# Edit page page
@app.route("/admin/pages/<slug>")
def admin_pages_slug(slug):
    if "elevation" in session:
        page = db.query(Page).filter_by(slug=slug).first()
        if page is not None:
            display = """
                <form action="/admin/pages/{slug}/edit/done" method="POST" id="editor">
                    <input type="text" name="title" placeholder="Title" value="{title}"><br>
                    <input type="text" name="slug" placeholder="Slug" value="{slug}"><br>
                    <input type="number" name="precedence" placeholder="Precedence" value={precedence}"><br>
                    <div id="editor-container" onkeyup="updatecontent()"></div>
                    <textarea form="editor" id="content" name="content" readonly hidden>{content}</textarea>
                    <input type="submit" value="Update">
                </form>
                <form action="/admin/pages/{slug}/delete/done" method="POST">
                    <input type="text" name="slug" value="{slug}" readonly hidden><br>
                    <input type="submit" value="Delete page" class="red">
                </form>
                """.format(
                title=page.title,
                slug=page.slug,
                precedence=page.precedence,
                content=page.content,
            )
            session["admin_route"] = "/admin/pages/{slug}".format(slug=slug)
            return render_template(
                "admin.html",
                page=page.title,
                display=Markup(config.admin["page"].format(display=display)),
            )
        else:
            session["error"] = "alert('Invalid request: Page does not exist');"
            return redirect("/admin/pages")
    else:
        session["error"] = "alert('Invalid request: Elevation required');"
        return redirect("/route")


# Edit page processing
@app.route("/admin/pages/<slug>/edit/done", methods=["POST"])
def admin_pages_slug_edit_done(slug):
    if "elevation" in session:
        title = request.form["title"]
        new_slug = request.form["slug"]
        precedence = request.form["precedence"]
        content = request.form["content"]
        page = db.query(Page).filter_by(slug=slug).first()
        if page is not None:
            page.title = title
            page.slug = new_slug
            page.precedence = precedence
            page.content = content
            db.commit()
            return redirect("/admin/pages")
        else:
            session["error"] = "alert('Invalid request: Page does not exist');"
            return redirect("/admin/pages")
    else:
        session["error"] = "alert('Invalid request: Elevation required');"
        return redirect("/route")


# Delete page processing
@app.route("/admin/pages/<slug>/delete/done", methods=["POST"])
def admin_pages_slug_delete_done(slug):
    if "elevation" in session:
        page = db.query(Page).filter_by(slug=slug).first()
        if page is not None:
            db.delete(page)
            db.commit()
            return redirect("/admin/pages")
        else:
            session["error"] = "alert('Invalid request: Page does not exist');"
            return redirect("/admin/pages")
    else:
        session["error"] = "alert('Invalid request: Elevation required');"
        return redirect("/route")


###############################################################################


if __name__ == "__main__":
    app.run(debug=True)
