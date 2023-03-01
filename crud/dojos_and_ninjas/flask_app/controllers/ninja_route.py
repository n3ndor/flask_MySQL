from flask import render_template, redirect, request

from flask_app.models import dojo_class, ninja_class
from flask_app import app


@app.route("/ninjas")
def ninjas():
    return render_template("ninja.html", dojos=dojo_class.Dojo.get_all())

@app.route("/create/ninja", methods=["POST"])
def create_ninja():
    ninja_class.Ninja.save(request.form)
    return redirect("/dojos")

