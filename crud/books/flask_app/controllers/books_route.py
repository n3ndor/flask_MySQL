from flask import render_template, redirect, request
from flask_app.models.books_class import Book
from flask_app import app

@app.route('/books')
def books():
    all_books = Book.get_books()
    return render_template("books.html", books_all = all_books)

@app.route("/add/book", methods=["POST"])
def new_book():
    data = {"title":request.form["b_title"],
    "num_of_pages":request.form["pages"]}
    book_id = Book.save_book(data)
    return redirect("/books")

@app.route("/books/update", methods=["POST"])
def update_book():
    Book.update_books(request.form)
    return redirect("/books")

@app.route("/book/<int:id>")
def book():
    data = {"id" : id}
    return render_template("book_show.html", book=Book.get_by_id(data), unfavorited_authors=Author.unfavorited_authors(data))

@app.route("/book/<int:book_id>")
def show_book(book_id):
    data = {"id" : id}
    get_books = Book.get_books(book_id)
    return render_template("book_show.html", book = get_books, unfavorited_authors = Author.unfavorited_authors(data))

@app.route("/join/author", methods=["POST"])
def join_author():
    data = {
        "author_id" : request.form["author_id"],
        "book_id" : request.form["book_id"]
    }
    Author.add_favorite(data)
    return redirect(f"/book/{request.form['book_id']}")