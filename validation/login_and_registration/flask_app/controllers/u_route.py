from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.u_class import User


@app.route("/")
def index():
    return render_template("index.html")