from flask import render_template, redirect, request
from flask_app.models.authors_class import Author
from flask_app import app

@app.route('/')
def index():
    return redirect("/authors")

@app.route("/authors")
def authors():
    all_authors = Author.get_authors()
    return render_template("authors.html", authors_all = all_authors)

@app.route("/add/author", methods=["POST"])
def new_author():
    data = {"name":request.form["author"]}
    author_id = Author.save_author(data)
    return redirect("/authors")

@app.route("/authors/update", methods=["POST"])
def update_author():
    Author.update_authors(request.form)
    return redirect("/authors")

@app.route("/author")
def author():
    return render_template("author_show.html")

@app.route("/author/<int:author_id>")
def show_author(author_id):
    one_author = Author.get_author(author_id)
    return render_template("author_show.html", author_one = one_author)

