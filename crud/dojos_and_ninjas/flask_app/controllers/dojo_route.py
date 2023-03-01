from flask import render_template, redirect, request
from flask_app.models.dojo_class import Dojo
from flask_app import app

@app.route('/')
def index():
    return redirect('/dojos')

@app.route('/dojos')
def dojos():
    dojos_a = Dojo.get_all()
    return render_template("index.html", all_dojos = dojos_a)

@app.route("/create/dojos", methods=["POST"])
def create_dojo():
    Dojo.save(request.form)
    return redirect("/dojos")

@app.route("/dojo/<int:id>")
def show_dojo(id):
    data = {"id" : id}
    return render_template("dojo.html", dojo = Dojo.get_one_ninja(data))