# Project 1
Web Programming with Python and JavaScript

*Here i describe how i designed my project and the functions of each file*

**Index**

Describing `index.html`, route `index()` of application.py and `sign in.css
* Thi is the home page of website, where the user can sign in or click "sign up " to go to the sign up page
* It has a `signin.css reference page to ajust the html layout
* In the Flask route `index()` it renders `index.html` if receives GET method or if it's POST,
 it gets the email and password to check if the user exists and if the password is right, checking the info
 with the database, after checking if it's True a user session is created and routes to the bookspage

**Register**

Describing `register.html`, route `register()` of application.py and `register.css`
* This is the registration page of the website, where the user input important information to register a new
 account to the website.
* It has a `register.css` to ajust layout the html layout 
*In the Flask Route `register()` it renders `register.html` by the method GET or by the method POST it receives all the information
 the user inputted, and verify if there is no user already registered with the same email,if not it insert the data on the database
 always passing the cariable alertFlask variable, to control the alert notification inside the `register.html` when the user is allowed to register or not.

**Books Page**

Describing `booksPage.html`, route `booksPage()` of application.py and `booksPage.css`

* This is the Search page where the user can insert any info between, **ISBN** of the book, **Title**
of the book or the **Author** name of the book, after the possible books will appear below the search.
* In the Flask Route `booksPage()` it gets the user session variable and if method GET, renders `bookPage.html` passing the user info as a variable and if method POST it receives the string
inserted inside the search bar, select the books from the database from data base then runs an algorithm KMP (declared inside the `classes` file) that compares the string from
search bar with every string inside the book rows title, isbn and author, when it finds a pattern it inserts the bookSearch list and renders the `booksPage.html`sending variables
user,bookSearch, searched and alertFlag. The searched variable is to allow the `booksPage.html` to appear the results. after the books result the user can select one book option to 
bookpage and see more information about the book selection.

**Book Page**

Describing `bookPage.html`, route `bookPage(book_id)` of application.py 

* This is the page the user can check the title, Author, isbn, year of publication about the book selected and the user can comment and give some rating once, and check the info
from goodreads.
* In the Flask Route `bookPage(book_id)` it receives the id from the URL that is the id in the database and verify if the book id exists or routed to `error.html` page,
if exists it gets the user session info, selects the book info from books database, select the book reviews info from the reviews database 
and get the json info from goodreads with averagescore and reviewCount. If GET Method it renders the page `bookPage.html` with variables user, 
book, reviews, alertFlag, averageScore reviewCount. If POST method, receives the text and the rating the user selected, and verify if the user did not commented in that book_id
before if not then it inserts on the review database and renders the `bookPage.html` with variables user, book, reviews, alertFlag, averageScore reviewCount.

**Layout Page**

Describing the `layout.html`

* This is the standard layout page used by all other html files to have the same "template page"
* Basically it only shares the same header all other html pages need to use

**Error Page**

Describing `error.html`

* this is the Page where it is routed when a page is not found or doesn't exist.

**Postgres Database**

Describing the database used and hosted in Heroku.com

The database have 3 tables: books, reviews and users,
* **Books Table**
    * id: unique identifier
    * isbn: isbn number of the book
    * Title: Title of the book
    * Author: author of the book
    * Year: year of publication of the book
    
* **Users Table**
    * id: unique identifier
    * fullname: name of the user
    * email: email of the user
    * telephone: telephone of the user
    * password: password of the user

* **Reviews Table**
    * id: unique identifier
    * username: username of the person who commented
    * Text: Text of the comment
    * rating: rating of the comment
    * usermail: email of the user who commented
    * bookid: the id of the book
    
    


