from flask import render_template, redirect, request
from flask_app.models.dojo_class import Dojo
from flask_app.models.ninja_class import Ninja
from flask_app import app

@app.route("/ninja/new")
def new_ninja():
    all_dojos = Dojo.get_all_dojos()
    return render_template ("create_ninja.html",dojos_all = all_dojos)


@app.route("/create/ninja", methods=["POST"])
def create_ninja():
    Ninja.save_ninja(request.form)
    return redirect("/dojos")

@app.route('/ninja/<int:id>')
def get_ninja(id):
    one_ninja = Ninja.get_ninja(id)
    return render_template("/dojos", ninja_one = one_ninja)


@app.route("/ninjas")
def get_ninjas():
    all_ninjas = Ninja.get_all_ninjas()
    return render_template("ninja.html", ninjas_all = all_ninjas)



@app.route("/edit/ninja/<int:id>")
def edit_ninja(id):
    update_ninja = Ninja.get_one_ninja(id)
    return render_template("edit_ninja.html", ninja_update= update_ninja)


@app.route("/update/ninja/<int:ninja_id>", methods=["POST"])
def update_ninja(ninja_id):
    dojo_id = Ninja.get_one_ninja(ninja_id).dojo_id
    Ninja.update_ninja(request.form)
    return redirect(f"/dojo/{dojo_id}")

@app.route("/delete/ninja/<int:id>")
def delete_ninja(id):
    data={"id":id}
    dojo_id = Ninja.get_one_ninja(id).dojo_id
    Ninja.delete_ninja(data)
    return redirect(f"/dojo/{dojo_id}")