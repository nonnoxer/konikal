import os

settings = {}

custom = {
    "title": "konikal",
    "header": "konikal",
    "subheader": "a website generator",
    "creator": "Natanael Tan",
    "website": "https://github.com/nonnoxer"
}

body = {}
body["login"] = """
    <form action="/logined" method="POST">
        <input type="name" name="username" placeholder="Username"><br>
        <input type="password" name="password" placeholder="Password"><br>
        <input type="submit" value="Login">
    </form>
    """
body["signup"] = """
    <form action="/signuped" method="POST">
        <input type="name" name="username" placeholder="Username"><br>
        <input type="password" name="password" placeholder="Password"><br>
        <input type="submit" value="Signup">
    </form>
    """
DATABASE_URL = "postgres://biqwifvhumknfy:4662193c2ba441b1ca2f0797fbde1141f990b9a65b845702bc15138b948ab528@ec2-50-16-197-244.compute-1.amazonaws.com:5432/dsl3qjvslamil"

def env():
    os.environ["DATABASE_URL"] = DATABASE_URL
