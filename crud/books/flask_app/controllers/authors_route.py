from flask import render_template, redirect, request
from flask_app import app

@app.route('/')
def index():
    return render_template("authors.html")