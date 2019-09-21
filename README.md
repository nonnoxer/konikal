https://konikal.herokuapp.com/documentation

# Getting started

**Make sure you have Python installed**

###### Method 1: Using the Konikal module to create an app
Install Konikal from clone from Github (add ```--user``` as an optional tag)
```pip install -e git+https://github.com/nonnoxer/konikal#egg=konikal-0.1.0```
Create an app with Konikal (leave ```[path]``` blank for current directory, or use absolute or relative path)
```python -m konikal create [path]```
Done!

###### Method 2: Extract the app folder from the Konikal repository
Clone https://github.com/nonnoxer/konikal or download it
```git clone https://github.com/nonnoxer/konikal```
Find the app folder and copy its contents into your desired folder
Install requirements (add ```--user``` as an optional tag)
```pip install -r requirements.txt```
Done!

# Setting up

* Edit database_url.txt. By default, this will be an sqlite database stored in database.db, but if you have your own database (strongly recommended) store the database url in database_url.txt. For more information on database urls, see https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls.
* Run app.py as a development server or deploy your app to a production server. The app will start with:
  * 1 admin user, username 'admin' and password 'password' (strongly recommended to change this as soon as possible)
  * 1 starter post published on the current date, by 'Konikal'
  * 1 home page
Done!

# Customisation

* For editing style of frontend pages, go to /static/style.css. For editing style of admin pages, go to /static/admin.css
* For editing javascript of frontend pages, go to /static/script.js. For editing javascript of admin pages, go to /static/admin.js
* For editing main layout of frontend pages, go to /templates/page.html. For editing main layout of admin pages, go to /templates/admin.html
* It is harder to customise the custom display of each request as it will require editing of app.py and config.py and may potentially break the code. Only do this with enough experience. If it fails, you can re-create the python files from Konikal's repository.
* To customise the name of your app, go to config.py and edit the variable custom["header"].

# User management

* The table users has the following structure:
  * id (Integer, Sequence, Primary Key)
  * username (String, Not Null, Unique)
  * password (String, Not Null)
  * elevation (Integer, Not Null, Default 0)
* Code for user class:
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence("users_sequence"), primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    elevation = Column(Integer, nullable=False, default=0)
```
* Elevation ranges from 0 to 4, with 0 being a normal user and 4 being an admin user
* Elevation from 1 to 4 allows access to the admin dashboard, although there is no current difference between elevations of 1 to 4
* People can log in, sign up, log out, change username, change password and delete self from the frontend
* Admins can create new users, edit username, password and elevation of users, and delete users from the admin dashboard

# Post management

* The table posts has the following structure:
  * id (Integer, Sequence, Primary Key)
  * title (String, Not Null, Unique)
  * slug (String, Not Null, Unique)
  * author (String, Not Null)
  * year (String, Not Null)
  * month (String, Not Null)
  * date (String, Not Null)
  * content (String, Not Null)
* Code for post class:
```python
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
```
* Title is the displayed heading and title of the post
* Slug is the url for the post. It is recommended that it is made out only of lowercase letters and hypens or underscores
* If left blank, the year, month and date will be the current one
* Posts are displayed latest first
* Content is a stringified JSON from quill
* Posts are edited from the admin dashboard using quill, a rich text editor
* Posts are displayed using a readonly quill instance without a toolbar
