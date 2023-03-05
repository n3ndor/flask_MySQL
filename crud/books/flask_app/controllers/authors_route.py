from flask import render_template, redirect, request
from flask_app import app

@app.route('/')
def index():
    return redirect("/authors")

@app.route("/authors")
def authors():
    return render_template("authors.html")

@app.route("/author")
def author():
    return render_template("author_show.html")