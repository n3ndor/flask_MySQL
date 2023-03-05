from flask import render_template, redirect, request
from flask_app import app

@app.route('/books')
def books():
    return render_template("books.html")

@app.route('/book')
def book():
    return render_template("book_show.html")