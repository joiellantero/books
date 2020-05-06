import os, json, requests

from flask import Flask, session, render_template, flash, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from helpers import login_required

app = Flask(__name__)

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


# 404 error handler
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


# landing page
@app.route("/")
def index():
    return render_template("index.html")


# registration page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # take the inputs from the text boxes
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        # access users table
        usernameData = db.execute("SELECT username FROM users WHERE username=:username", {"username":username}).fetchone()

        # check if username is already taken
        if usernameData is not None:
            flash("Username already exists!", "danger")
            return render_template("register.html")

        else:
            if password == confirm:
                # save the user to the database
                db.execute("INSERT INTO users(username, password) VALUES(:username, :password)", {"username":username, "password":password})
                db.commit()
                flash("Registration Successful!", "success")
                return redirect( url_for('login') )

            else:
                flash("Password doesn't match!", "danger")
                return render_template("register.html")

    return render_template("register.html")


# login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # take the input from the text boxes
        username = request.form.get("username")
        password = request.form.get("password")

        # access the users table
        usernameData = db.execute("SELECT id, username FROM users WHERE username=:username", {"username":username}).fetchone()
        passwordData = db.execute("SELECT password FROM users WHERE username=:username", {"username":username}).fetchone()
        
        # user checker
        if usernameData is None:
            flash("User not registered!", "danger")
            return render_template("login.html")
        else:
            # password checker
            if password == passwordData.password:
                # session started
                session["log"] = True

                # remember session
                session["user_id"] = usernameData.id
                session["user_name"] = usernameData.username
                return redirect(url_for('library') )

            else:
                # password didnt match passwordData.password
                flash("Incorrect password!", "danger")
                return render_template("login.html")

    return render_template("login.html")


# logout
@app.route("/logout")
def logout():
    # forget all the sessions
    session.clear()

    flash("Log out successful", "success")
    return redirect(url_for('login'))


# library page
@app.route("/library", methods=["GET", "POST"])
@login_required
def library():
    currentUser = session["user_name"]

    if request.method == "POST":
        # book id checker
        if not request.form.get("book"):
            flash("Library can't search for nothing. Enter an ISBN, title, or author of book.", "danger")
            return render_template("error.html", username=currentUser)
        
        # guess the other parts of the input
        query = "%" + request.form.get("book") + "%"

        # capitalize each words of the search input
        query = query.title()

        rows = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn LIKE :query OR title LIKE :query OR author LIKE :query LIMIT 20", {"query": query})

        if rows.rowcount == 0:
            flash("The book you are searching is not in our library.", "danger")
            return render_template("error.html", username=currentUser)

        books = rows.fetchall()

        return render_template("library.html", books=books, username=currentUser)

    return render_template("library.html", username=currentUser)


# books page
@app.route("/book/<isbn>", methods=['GET','POST'])
@login_required
def book(isbn):
    currentUser = session["user_name"]

    if request.method == "POST":
        # remember user
        currentUserId = session["user_id"]

        # take form inputs
        rating = request.form.get("rating")
        comment = request.form.get("comment")

        book_id = db.execute("SELECT id FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()[0]

        review_row = db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_id = :book_id", {"user_id": currentUserId, "book_id": book_id})

        if review_row.rowcount == 1:
            flash("Only one book review per user is allowed!", "danger")
            return redirect("/book/" + isbn)

        rating = int(rating)

        db.execute("INSERT INTO reviews (user_id, book_id, comment, rating) VALUES (:user_id, :book_id, :comment, :rating)", {"user_id": currentUserId, "book_id": book_id, "comment": comment, "rating": rating})
        db.commit()

        flash("Review succesfully submitted!", "success")
        return redirect("/book/" + isbn)

    else:
        book_info = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchall()

        # take review from goodreads
        key = os.getenv("GOODREADS_KEY")
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": isbn})
        response = res.json()
        response = response['books'][0]
        book_info.append(response)

        book_id = db.execute("SELECT id FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()[0]

        # take book reviews 
        reviews = db.execute("SELECT users.username, comment, rating FROM users INNER JOIN reviews ON users.id = reviews.user_id WHERE book_id = :book", {"book": book_id}).fetchall()

        review_row = db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": book_id})

        if review_row.rowcount == 0:
            return render_template("book.html", book_info=book_info, reviews=reviews, username=currentUser, message='No user reviews submitted')

        return render_template("book.html", book_info=book_info, reviews=reviews, username=currentUser)


@app.route("/api/<isbn>", methods=["GET"])
@login_required
def api_call(isbn):
    row = db.execute("SELECT isbn, title, author, year, COUNT(reviews.id) as review_count, AVG(reviews.rating) as average_score FROM books FULL OUTER JOIN reviews ON books.id = reviews.book_id WHERE isbn = :isbn GROUP BY title, author, year, isbn", {"isbn": isbn})

    if row.rowcount == 0:
        return jsonify({"ERROR": "API call failed"}), 422
  
    tmp = row.fetchone()

    result = dict(tmp.items())

    if result['average_score'] is None:
         return jsonify(result)
    
    else:
        result['average_score'] = float('%.2f'%(result['average_score']))
        return jsonify(result)
