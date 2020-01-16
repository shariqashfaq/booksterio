import os
import json
from flask import Flask, session, render_template, request, redirect 
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, substrings

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

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

#todo: implement controls for user input to prevent XSS
@app.route("/")
def index():
    
    #Welcome user if logged in
    if session:
        rows = db.execute("SELECT * FROM users WHERE id = :id", {"id":session["user_id"]}).fetchone()
        session["user"] = rows.username
    
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    """logs user in"""

    #Forget session id 
    session.clear()

    # Ensure username was submitted
    if not request.form.get("username"):
        return render_template("error.html", message="provide username")

    # Ensure password was submitted
    elif not request.form.get("password"):
        return render_template("error.html", message="provide password")

    # Query database for username
    rows = db.execute("SELECT * FROM users WHERE username = :username", {"username":request.form.get("username")}).fetchone()

    # Ensure username exists and password is correct
    if rows is None or not check_password_hash(rows.password, request.form.get("password")):
        return render_template("error.html", message="username or password is invalid")

    # Remember which user has logged in
    session["user_id"] = rows.id

    # Redirect user to home page
    return redirect("/")

@app.route("/register", methods=["POST"])
def register():
    """Register User"""

    #User submits registration form
    #Check if username and password fields are filled
    if not request.form.get("username"):
        return render_template("error.html", message="username not provided")

    elif not request.form.get("password"):
        return render_template("error.html", message="password not provided")

    #check if username is available
    rows = db.execute("SELECT * FROM users WHERE username = :username", {"username":request.form.get("username")}).fetchone()
    if not rows == None:
        return render_template("error.html", message="username unavailable")

    #Check if password matches confirmation
    if not request.form.get("password") == request.form.get("confirmPassword"):
        return render_template("error.html", message="passwords dont match")

    #Insert user into database if above conditions met
    db.execute("INSERT INTO users (username, password) VALUES (:username , :password)" , {"username":request.form.get("username"), "password":generate_password_hash(request.form.get("password"))})
    
    #store id and login user
    rows0 = db.execute("SELECT * FROM users WHERE username = :username", {"username":request.form.get("username")}).fetchone()
    session["user_id"] = rows0.id
    db.commit()
    return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/search", methods=["POST"])
@login_required
def search():
    """implements search function"""
    #Implement search rankings at some point 

    #initialize array for misspelled/incomplete search results, set a variable for the search request
    titleRows = []
    query = request.form.get("search").lower()
    

    # If user query is spelled correctly, search is case insensitive by default
    rows = db.execute("SELECT * FROM books WHERE LOWER(title) =:title OR isbn=:isbn OR LOWER(author)=:author", {"title":request.form.get("search"), "isbn":request.form.get("search"), "author":request.form.get("search")}).fetchall()

    # If user query is spelled incorrectly or is incomplete, first try and find a book field which begins with query
    # todo: no search results returned if query is "skeldton crew".
    # later try searching for substrings which are shorter than len(query)
    if not rows:
        rows1 = db.execute("SELECT * FROM books").fetchall()
        for row in rows1:
            if row["title"].lower().startswith(query) or row["author"].lower().startswith(query):
                titleRows.append(row)
    #if query does not match begining of any book field try finding a substring anywhere in the book field
        if len(titleRows) == 0 and len(query) > 5:
            for row in rows1:
                if len(substrings(query, row["title"].lower(), len(query))) > 0 or len(substrings(query, row["author"].lower(), len(query))) > 0:
                    titleRows.append(row)



    return render_template("search.html", rows=rows, query=query, titleRows=titleRows)

@app.route("/book/<title>")
@login_required
def book(title):
    """ returns a book page when user clicks link on search results page"""
    
    #convert title to json so that it can be read by javascript on book page
    return render_template("book.html", title=json.dumps(title))

@app.route("/review", methods=["POST"])
@login_required
def review():
    """Submits user review for a book taking book title as argument. Returns updated book page with new review via AJAX"""
    #todo: rank reviews by user voting


