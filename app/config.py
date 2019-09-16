import os

settings = {}

custom = {
    "header": "Konikal",
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
adminbar = {}
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
    <form action="/editpassworded" method="POST">
        <input type="text" name="username" value="{user}" readonly hidden>
        <input type="text" name="password" placeholder="New password">
        <br>
        <input type="submit" value="Edit">
    </form>
    <h2>Delete user</h2>
    <form action="/deleteusered" method="POST">
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
    <h1>Users</h1>
    <table class="table">
        <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Password</th>
            <th>Elevation</th>
        </tr>
        {users}
    </table>
    <a href="/admin">Back</a>
    """
admin["posts"] = """
    <h1>Posts</h1>
    <table class="table">
        <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Slug</th>
            <th>Author</th>
            <th>Date</th>
        </tr>
        {posts}
    </table>
    <a href="/admin">Back</a>
    """
admin["pages"] = """
    <h1>Pages</h1>
    <table>
        {pages}
    </table>
    <a href="/admin">Back</a>
    """
adminbar["4"] = """
    """

DATABASE_URL = open("app/database_url.txt", "r").readlines()[0]
#Remove later? when publicly pushing
DATABASE_URL = "postgres://biqwifvhumknfy:4662193c2ba441b1ca2f0797fbde1141f990b9a65b845702bc15138b948ab528@ec2-50-16-197-244.compute-1.amazonaws.com:5432/dsl3qjvslamil"
os.environ["DATABASE_URL"] = DATABASE_URL
