from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models import user_model



@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    if not user_model.User.validate_register(request.form):
        session["user_id"] = request.form #storing the data in session
        return redirect('/')
    new_user = user_model.User.save_user(request.form)
    session["user_id"] = new_user
    return redirect("/dashboard")

@app.route('/login',methods=['POST'])
def login():
    if not user_model.User.validate_login(request.form):
        session["user_id"] = request.form
        return redirect("/")
    email_data = {"email": request.form["login_email"]}
    old_user = user_model.User.get_by_email(email_data)
    session["user_id"] = old_user.id
    return redirect("/dashboard")

@app.route('/logout')
def logout():
    # if 'user_id' in session:
    #     session.pop('user_id')
    session.clear()
    return redirect('/')