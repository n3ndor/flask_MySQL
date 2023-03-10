from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models import u_class


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register',methods=['POST'])
def register():

    if not u_class.User.validate_register(request.form):
        return redirect('/')
    new_user = u_class.User.save_user(request.form)
    print(new_user)
    session["user_id"] = new_user
    return redirect(f"/{new_user}")

@app.route('/login',methods=['POST'])
def login():
    if not u_class.User.validate_login(request.form):
        return redirect("/")
    email_data = {"email": request.form["login_email"]}
    returning_user = u_class.User.get_by_email(email_data)
    session["user_id"] = returning_user.id
    return redirect(f"/{returning_user.id}")


@app.route('/<int:id>')
def profile(id):
    if 'user_id' not in session:
        return redirect('/')
    data ={ id : session['user_id'] }
    a = u_class.User.get_by_email(data)
    return render_template("logged_in.html", the_user = a)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')