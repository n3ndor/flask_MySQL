from flask import Flask, render_template, redirect, request
# import the class from friend.py
from users import User

app = Flask(__name__)

@app.route("/")
def index():
    # return "I don't know what are you searching here <br> Type /users in address bar to continue "
    return render_template("index.html")


@app.route("/users")
def show():
    all_the_users = User.get_all()
    print(all_the_users)
    return render_template("read.html", all_users=all_the_users)


@app.route("/users/new")
def new():
    return render_template("create.html")

@app.route("/users/create", methods=["POST"])
def create():
    print(request.form)
    User.save(request.form)
    return redirect("/users")



if __name__ == "__main__":
    app.run(debug=True)

