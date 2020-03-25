"""
Configs do flask:

export FLASK_APP=application.py
export FLASK_ENV=development
export DATABASE_URL=postgres://krhubjbfzkqork:964f0fe21fe054c98ada81bff1dea04b54d2c3a3097c8e64a8e8023ce9e09938@ec2-34-202-7-83.compute-1.amazonaws.com:5432/d6pft8f8cdbk97

"""
import os
import requests

from flask import Flask, session, render_template, jsonify, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from classes import *


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

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

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if db.execute("SELECT * FROM users WHERE email = :email", {"email": email}).rowcount != 0: # checking if email exist
            session['user'] = db.execute("SELECT * FROM users WHERE email = :email", {"email": email}).fetchone() # getting the id of the row
            confPassword = session['user'].password
            if password == confPassword:
                return render_template("booksPage.html", user=session['user'])
            else:
                return render_template("index.html")

    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    alertFlag = 0  # registration alert 0 = clear, 1 = success, 2 = fail
    if request.method == "POST":
        name = request.form.get("fullName")
        email = request.form.get("email")
        telephone = request.form.get("telephone")
        password = request.form.get("password")
        confPassword = request.form.get("confPassword")
        if password != confPassword:  # in case password is different
            alertFlag = 2 # caso erro

        else:
            #checking if user exists
            if db.execute("SELECT * FROM users WHERE email = :email", {"email": email}).rowcount == 0:
                try:
                    db.execute(
                        "INSERT INTO users (fullname, email, telephone, password)  VALUES (:name, :email, :telephone, :password)",
                        {"name": name, "email": email, "telephone": telephone, "password": password})
                    db.commit()
                    alertFlag = 1
                except:
                    alertFlag = 2
                    return render_template("register.html", alertFlag=alertFlag)
            else: # caso erro
                alertFlag = 2

    return render_template("register.html", alertFlag=alertFlag)


@app.route("/booksPage", methods=["GET", "POST"])
def booksPage():
    searched = 0  # to allow search books menu appear
    alertFlag = 0  # registration alert 0 = clear, 1 = success, 2 = fail
    user = session.get('user', None)

    if request.method == "POST":
        search = request.form.get("search")  # what to search
        search = str(search)  # converting to str
        books = db.execute("SELECT * FROM books ").fetchall()  # Query all books
        bookSearch = []
        kmp = KMP()
        searched = 1
        for book in books:
            if len(kmp.search(book.title.lower(), search.lower())) != 0:
                bookSearch.append(book)
            elif len(kmp.search(book.isbn.lower(), search.lower())) != 0:
                bookSearch.append(book)
            elif len(kmp.search(book.author.lower(), search.lower())) != 0:
                bookSearch.append(book)
        if len(bookSearch) <= 0: # when no search are found
                searched = 0
                alertFlag = 2 # fail to search
                return render_template("booksPage.html", user=user, searched=searched, alertFlag=alertFlag)
        return render_template("booksPage.html", user=user, searchs=bookSearch, searched=searched, alertFlag=alertFlag)

    return render_template("booksPage.html", user=user, searched=searched, alertFlag=alertFlag )


@app.route("/bookPage/<int:book_id>", methods=["GET", "POST"])
def bookPage(book_id):
    user = session.get('user', None)
    alertFlag = 0
    # make sure book exists.
    if db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).rowcount == 0:
        return render_template("error.html")
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
    reviews = db.execute("SELECT * FROM reviews WHERE bookid = :bookid", {"bookid": book_id}).fetchall()
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "WijpmnZGmEz77ghzKZgg", "isbns": book.isbn})
    averageScore = res.json()['books'][0]['average_rating']
    reviewCount = res.json()['books'][0]['reviews_count']
    if request.method == "POST":
        text = request.form.get("comments")  # what to search
        rating = request.form.get("rating")
        if db.execute(" SELECT * FROM reviews WHERE bookid = :bookid AND useremail = :useremail", {"bookid": book_id, "useremail": user.email}).rowcount == 0: #no comment
            try:
                db.execute(
                    "INSERT INTO reviews (username, text, rating, useremail, bookid) VALUES (:username, :text, :rating, :useremail, :bookid)",
                    {"username": user.fullname, "text": text, "rating": rating, "useremail": user.email,
                     "bookid": book_id})
                db.commit()
                alertFlag = 1
            except:
                return render_template("bookPage.html", user=user, book=book, reviews=reviews, alertFlag=alertFlag, averageScore=averageScore, reviewCount=reviewCount)
        else:
            alertFlag = 2

        return render_template("bookPage.html", user=user, book=book, reviews=reviews, alertFlag=alertFlag, averageScore=averageScore, reviewCount=reviewCount)

    return render_template("bookPage.html", user=user, book=book, reviews=reviews, alertFlag=alertFlag, averageScore=averageScore, reviewCount=reviewCount)

@app.route("/api/books/<string:isbn>")
def book_api(isbn):
    """Return the API information about a book."""

    # Make sure book exists.
    if db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).rowcount == 0:
        return jsonify({"error": "Invalid book_id"}), 422
    else:
        book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                           params={"key": "WijpmnZGmEz77ghzKZgg", "isbns": book.isbn})
        averageScore = res.json()['books'][0]['average_rating']
        reviewCount = res.json()['books'][0]['reviews_count']

        return jsonify({
                "title": book.title,
                "author": book.author,
                "year": book.year,
                "isbn": book.isbn,
                "review_count": reviewCount,
                "average_score": averageScore
            })


@app.route("/error")
def errorPage():
    return render_template("error.html")


