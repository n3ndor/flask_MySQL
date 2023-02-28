from flask import render_template, redirect, request

from flask_app.models import dojo, ninja
from flask_app import app


@app.route("/ninjas")
def ninjas():

    return render_template("ninja.html")