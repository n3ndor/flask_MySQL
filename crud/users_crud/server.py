from flask import Flask, render_template, redirect, request
from users import User

app = Flask(__name__)

@app.route("/")
def index():
    # return "I don't know what are you searching here <br> Type /users in address bar to continue "
    return render_template("index.html")


@app.route("/users")
def read():
    all_the_users = User.get_all()
    return render_template("read.html", all_users=all_the_users)


@app.route("/users/new")
def new():
    return render_template("create.html")

@app.route("/users/create", methods=["POST"])
def create():
    User.save(request.form)
    return redirect("/users")

@app.route("/users/update", methods=["POST"])
def update():
    User.update(request.form)
    return redirect("/users")

@app.route("/users/delete/<int:id>")
def delete(id):
    data={"id":id}
    User.delete(data)
    return redirect("/users")

@app.route("/users/edit/<int:id>")
def edit(id):
    data ={"id":id}
    return render_template("edit.html",user=User.get_one(data))

@app.route("/users/show/<int:id>")
def show(id):
    data={"id":id}
    return render_template("show.html", user=User.get_one(data))

if __name__ == "__main__":
    app.run(debug=True)

