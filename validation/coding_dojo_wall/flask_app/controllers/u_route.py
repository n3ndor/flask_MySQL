from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models import u_class, p_class



@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register',methods=['POST'])
def register():

    if not u_class.User.validate_register(request.form):
        return redirect('/')
    new_user = u_class.User.save_user(request.form)
    session["user_id"] = new_user
    return redirect("/wall")

@app.route('/login',methods=['POST'])
def login():
    if not u_class.User.validate_login(request.form):
        return redirect("/")
    email_data = {"email": request.form["login_email"]}
    returning_user = u_class.User.get_by_email(email_data)
    session["user_id"] = returning_user.id
    return redirect("/wall")


@app.route('/wall')
def profile():
    if 'user_id' not in session:
        return redirect('/')
    data ={ "id" : session['user_id'] }
    user_the = u_class.User.get_by_id(data)
    post_all = p_class.Post.get_all()
    return render_template("wall.html", the_user = user_the, all_post = post_all)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')