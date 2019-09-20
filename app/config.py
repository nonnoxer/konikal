import os

settings = {}

custom = {
    "header": "Konikal",
    "subheader": "a website generator",
    "creator": "Natanael Tan",
    "website": "https://github.com/nonnoxer"
}

page = {}
admin = {}
pagebar = {}
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
page["posts"] = """
    <h1>{page}</h1>
    <table class="table">
        <tr>
            <th>Post</th>
            <th>Author</th>
            <th>Date</th>
        </tr>
        {body}
    </table>
    """
page["post"] = """
    <h1>{title}</h1>
    <p>{date}</p>
    <b>By {author}</b>
    <textarea id="content" readonly hidden>{content}</textarea>
    <div id="editor"></div>
    """
page["page"] = """
    <h1>{title}</h1>
    <textarea id="content" readonly hidden>{content}</textarea>
    <div id="editor"></div>
    """
pagebar["home"] = """
    {pagebar}
    <li class="nav-item active">
        <a class="nav-link" href="/posts">All Posts</a>
    </li>
    """
pagebar["no_home"] = """
    <li class="nav-item active">
        <a class="nav-link" href="/">Home</a>
    </li>
    {pagebar}
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
    <p><a href="/logout/done">Logout</a></p>
    """
admin["users"] = """
    <h1>Users</h1>
    <a href="/admin/users/new">New user</a></li>
    {display}
    <p><a href="/admin">Back</a></p>
    <p><a href="/logout/done">Logout</a></p>
    """
admin["users_new"] = """
    <h1>New User</h1>
    <form action="/admin/users/new/done" method="POST">
        <input type="name" name="username" placeholder="Username"><br>
        <input type="text" name="password" placeholder="Password"><br>
        <input type="range" id="elevationrange" name="elevation" value="0" min="0" max="4"
            onchange="updateelevationvalue()">
        <p id="elevationvalue">0</p>
        <input type="submit" value="Create">
    </form>
    <p><a href="/admin/users">Back</a></p>
    <p><a href="/logout/done">Logout</a></p>
    """
admin["user"] = """
    {display}
    <p><a href="/admin/users">Back</a></p>
    <p><a href="/logout/done">Logout</a></p>
    """
admin["posts"] = """
    <h1>Posts</h1>
    <a href="/admin/posts/new">New post</a></li>
    {display}
    <p><a href="/admin">Back</a></p>
    <p><a href="/logout/done">Logout</a></p>
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
    <p><a href="/admin/posts">Back</a></p>
    <p><a href="/logout/done">Logout</a></p>
    """
admin["post"] = """
    <h1>Edit Post</h1>
    {display}
    <p><a href="/admin/posts">Back</a></p>
    <p><a href="/logout/done">Logout</a></p>
"""
admin["pages"] = """
    <h1>Pages</h1>
    <a href="/admin/pages/new">New page</a></li>
    {display}
    <p><a href="/admin">Back</a></p>
    <p><a href="/logout/done">Logout</a></p>
    """
admin["pages_new"] = """
    <h1>New Page</h1>
    <form action="/admin/pages/new/done" method="POST" id="editor">
        <input type="text" name="title" placeholder="Title"><br>
        <input type="text" name="slug" placeholder="Slug"><br>
        <input type="number" name="precedence" placeholder="Precedence" value="0"><br>
        <div id="editor-container" onkeyup="updatecontent()"></div>
        <textarea form="editor" id="content" name="content" readonly hidden></textarea>
        <input type="submit" value="Create">
    </form>
    <p><a href="/admin/pages">Back</a></p>
    <p><a href="/logout/done">Logout</a></p>
    """
admin["page"] = """
    <h1>Edit Page</h1>
    {display}
    <p><a href="/admin/pages">Back</a></p>
    <p><a href="/logout/done">Logout</a></p>
    """
adminbar["4"] = """
    """

DATABASE_URL = open("app/database_url.txt", "r").readlines()[0]
os.environ["DATABASE_URL"] = DATABASE_URL
