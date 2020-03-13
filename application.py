import os
#import requests

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


#res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "WijpmnZGmEz77ghzKZgg", "isbns": "9781632168146"})
#print(res.json())

app = Flask(__name__)

#Classes


class Users:

    counter = 1
    userList = []

    def __init__(self, user):

        self.id = Users.counter
        Users.counter += 1
        userList.append(user)


class User:

    def __init__(self, fullName, email, telephone, password):
        self.fullName = fullName
        self.email = email
        self.telephone = telephone
        self.password = password

    def print_user(self):
        print(f"Full Name: {self.fullName}")
        print(f"Full Name: {self.email}")
        print(f"Full Name: {self.telephone}")
        print(f"Full Name: {self.password}")

#users = []
names = [] # remmover depois

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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        name = request.form.get("fullName", "email")
        names.append(name)

    return render_template("register.html", names=names)



