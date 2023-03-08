from flask import render_template, redirect, request

from flask_app.models.c_class import Cookie
from flask_app import app

@app.route("/")
def index():
    return redirect("/cookies")

@app.route("/cookies")
def read():
    orders_all = Cookie.get_all()
    return render_template("orders.html", all_orders = orders_all)

@app.route("/cookies/new")
def new():
    return render_template("new.html")

@app.route("/cookies/edit/<int:order_id>")
def edit(order_id):
    orders = Cookie.get_one(order_id)
    return render_template("edit.html", order = orders )

@app.route("/cookies/create", methods=["POST"])
def new_order():
    if Cookie.validate_order(request.form):
        Cookie.create(request.form)
        return redirect("/cookies")
    return redirect("/cookies/new")

@app.route("/cookies/update/<int:order_id>", methods=["Post"])
def update_order(order_id):
    if Cookie.validate_order(request.form):
        Cookie.update(request.form)
        return redirect("/cookies")
    return redirect(f"/cookies/edit/{request.form['id']}")

@app.route("/cookies/delete/<int:order_id>")
def delete(order_id):

    Cookie.delete(order_id)
    return redirect("/cookies")