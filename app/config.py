import os

settings = {}

custom = {
    "title": "konikal",
    "header": "konikal",
    "subheader": "a website generator",
    "creator": "Natanael Tan",
    "website": "https://github.com/nonnoxer"
}

dashboard = {
    "login": "login",
    "dashboard": "dashboard"
}

page = {}
admin = {}
page["login"] = """
    <h1>Login</h1>
    <form action="/logined" method="POST">
        <input type="name" name="username" placeholder="Username"><br>
        <input type="password" name="password" placeholder="Password"><br>
        <input type="submit" value="Login">
    </form>
    """
page["signup"] = """
    <h1>Signup</h1>
    <form action="/signuped" method="POST">
        <input type="name" name="username" placeholder="Username"><br>
        <input type="password" name="password" placeholder="Password"><br>
        <input type="submit" value="Signup">
    </form>
    """
page["user"] = """
    <h1>{user}</h1>
    <h2>Edit password</h2>
    <form action="/editedpassword" method="POST">
        <input type="text" name="username" value="{user}" readonly hidden>
        <input type="text" name="password" placeholder="New password">
        <br>
        <input type="submit" value="Edit">
    </form>
    <h2>Delete user</h2>
    <form action="/deleteduser" method="POST">
        <input type="text" name="username" value="{user}" readonly hidden>
        <input type="submit" value="Delete">
    </form>
    """
admin["login"] = """
    <h1>Admin Login</h1>
    <form action="/adminlogined" method="POST">
        <input type="text" name="username" placeholder="Username"><br>
        <input type="password" name="password" placeholder="Password"><br>
        <input type="submit" value="Login">
    </form>
    <br>
    <a href="/route">Back</a>
    """
admin["dashboard"] = """
    """
admin["users"] = """
    """
admin["posts"] = """
    """
admin["pages"] = """
    """
DATABASE_URL = "postgres://biqwifvhumknfy:4662193c2ba441b1ca2f0797fbde1141f990b9a65b845702bc15138b948ab528@ec2-50-16-197-244.compute-1.amazonaws.com:5432/dsl3qjvslamil"

def env():
    os.environ["DATABASE_URL"] = DATABASE_URL
