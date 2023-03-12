from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.p_class import Post

@app.route("/new_post", methods=["POST"])
def create_new_post():
    Post.save(request.form)
    return redirect("/wall")

@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    Post.delete(post_id)
    return redirect("/wall")