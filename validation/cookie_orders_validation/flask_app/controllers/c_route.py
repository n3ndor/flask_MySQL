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
    data = {"id":order_id}
    return render_template("edit.html", order = Cookie.get_one(order_id))

