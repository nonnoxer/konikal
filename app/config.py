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
    <form action="/login/done" method="POST">
        <input type="name" name="username" placeholder="Username"><br>
        <input type="password" name="password" placeholder="Password"><br>
        <input type="submit" value="Login">
    </form>
    """
page["signup"] = """
    <h1>Signup</h1>
    <form action="/signup/done" method="POST">
        <input type="name" name="username" placeholder="Username"><br>
        <input type="password" name="password" placeholder="Password"><br>
        <input type="submit" value="Signup">
    </form>
    """
page["user"] = """
    <h1>{user}</h1>
    <h2>Edit Username</h2>
    <form action="/editusername/done" method="POST">
        <input type="text" name="username" value="{user}" readonly hidden>
        <input type="text" name="new_username" placeholder="New username">
        <br>
        <input type="submit" value="Update">
    </form>
    <h2>Edit Password</h2>
    <form action="/editpassword/done" method="POST">
        <input type="text" name="username" value="{user}" readonly hidden>
        <input type="text" name="password" placeholder="New password">
        <br>
        <input type="submit" value="Update">
    </form>
    <h2>Delete User</h2>
    <form action="/deleteuser/done" method="POST">
        <input type="text" name="username" value="{user}" readonly hidden>
        <input type="submit" value="Delete">
    </form>
    """
admin["login"] = """
    <h1>Admin Login</h1>
    <form action="/admin/login/done" method="POST">
        <input type="text" name="username" placeholder="Username"><br>
        <input type="password" name="password" placeholder="Password"><br>
        <input type="submit" value="Login">
    </form>
    <br>
    <a href="/route">Back</a>
    """
admin["admin"] = """
    <h1>User Actions</h1>
    <ul>
        <li><a href="/admin/users">All users</a></li>
        <li><a href="/admin/users/new">New user</a></li>
    </ul>
    <h1>Post Actions</h1>
    <ul>
        <li><a href="/admin/posts">All posts</a></li>
        <li><a href="/admin/posts/new">New post</a></li>
    </ul>
    <h1>Page Actions</h1>
    <ul>
        <li><a href="/admin/pages">All pages</a></li>
        <li><a href="/admin/pages/new">New page</a></li>
    </ul>
    <p><a href="/logouted">Logout</a></p>
    """
admin["users"] = """
    <h1>Users</h1>
    <a href="/admin/users/new">New user</a></li>
    {display}
    <a href="/admin">Back</a>
    """
admin["user"] = """
    {display}
    """
admin["posts"] = """
    <h1>Posts</h1>
    <a href="/admin/posts/new">New post</a></li>
    {display}
    <a href="/admin">Back</a>
    """
admin["posts_new"] = """
    <h1>New Post</h1>
        <form action="/admin/posts/new/done" method="POST" id="editor">
            <input type="text" name="title" placeholder="Title"><br>
            <input type="text" name="slug" placeholder="Slug"><br>
            <input type="name" name="author" placeholder="Author"><br>
            <input type="date" name="date"><br>
            <div id="editor-container" onkeyup="updatecontent()"></div>
            <textarea form="editor" id="content" name="content" readonly hidden></textarea>
            <input type="submit" value="Create">
        </form>
    """
admin["post"] = """
    <h1>Edit Post</h1>
    {display}
"""
admin["pages"] = """
    <h1>Pages</h1>
    <a href="/admin/pages/new">New page</a></li>
    {display}
    <a href="/admin">Back</a>
    """
admin["pages_new"] = """
    <h1>New Page</h1>
        <form action="/admin/pages/new/done" method="POST" id="editor">
            <input type="text" name="title" placeholder="Title"><br>
            <input type="text" name="slug" placeholder="Slug"><br>
            <div id="editor-container" onkeyup="updatecontent()"></div>
            <textarea form="editor" id="content" name="content" readonly hidden></textarea>
            <input type="submit" value="Create">
        </form>
    """
admin["page"] = """
    <h1>Edit Page</h1>
    {display}
    """
adminbar["4"] = """
    """

DATABASE_URL = open("app/database_url.txt", "r").readlines()[0]
#Remove later? when publicly pushing
#DATABASE_URL = "postgres://biqwifvhumknfy:4662193c2ba441b1ca2f0797fbde1141f990b9a65b845702bc15138b948ab528@ec2-50-16-197-244.compute-1.amazonaws.com:5432/dsl3qjvslamil"
os.environ["DATABASE_URL"] = DATABASE_URL
