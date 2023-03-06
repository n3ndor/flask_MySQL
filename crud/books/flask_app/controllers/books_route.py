from flask import render_template, redirect, request
from flask_app.models.books_class import Book
from flask_app import app

@app.route('/books')
def books():
    all_books = Book.get_books()
    return render_template("books.html", books_all = all_books)

@app.route("/add/book", methods=["POST"])
def new_book():
    data = {"title":request.form["btitle"],"num_of_pages":request.form["pages"]}
    book_id = Book.save_book(data)
    return redirect("/books")

@app.route("/books/update", methods=["POST"])
def update_book():
    Book.update_books(request.form)
    return redirect("/books")

@app.route("/book")
def book():
    return render_template("book_show.html")

@app.route("/book/<int:book_id>")
def show_book(book_id):
    one_book = Book.get_book(book_id)
    return render_template("book_show.html", book_one = one_book)