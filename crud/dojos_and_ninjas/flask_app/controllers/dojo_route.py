from flask import render_template, redirect, request
from flask_app.models.dojo_class import Dojo
from flask_app.models.ninja_class import Ninja
from flask_app import app

@app.route('/')
def index():
    return redirect('/dojos')

@app.route('/dojo/<int:dojo_id>')
def get_one_dojo(dojo_id):
    one_dojo = Dojo.get_one_dojo(dojo_id)
    all_ninjas = Ninja.get_ninjas_dojo(dojo_id)
    return render_template("one_dojo.html", dojo_one = one_dojo, ninjas_all=all_ninjas)

@app.route("/dojos")
def get_dojos():
    all_dojos = Dojo.get_all_dojos()
    return render_template("index.html", dojos_all = all_dojos)

@app.route("/create/dojo", methods=["POST"])
def create_dojo():
    Dojo.save_dojo(request.form)
    return redirect("/dojos")


@app.route("/edit/dojo/<int:dojo_id>")
def edit_dojo(dojo_id):
    edit_dojo = Dojo.get_one_dojo(dojo_id)
    return render_template("edit_dojo.html", dojo_edit = edit_dojo)

@app.route("/update/<int:dojo_id>", methods=["POST"])
def update_dojo(dojo_id):
    Dojo.update_dojo(request.form)
    return redirect("/dojos")

@app.route("/delete/dojo/<int:dojo_id>")
def delete(dojo_id):
    Dojo.delete_dojo(dojo_id)
    return redirect("/dojos")