from flask import Flask, render_template
# import the class from friend.py
from friend import Friend

app = Flask(__name__)

@app.route("/")
def index():
    # call the get all classmethod to get all friends
    all_friends = Friend.get_all()
    print(all_friends)
    return render_template("index.html", all_friends = all_friends)

@app.route("/friends/<int:friend_id>")
def show(friend_id):
    one_friend = Friend.get_one(friend_id)
    return render_template("show.html", one_friend=one_friend)

@app.route("/friends/create")
def create():
    Friend.save(request.form)
    return redirect("/")




if __name__ == "__main__":
    app.run(debug=True)

