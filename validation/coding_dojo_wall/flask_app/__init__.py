# __init__.py

from flask import Flask
app = Flask(__name__)

app.secret_key = "change the password, don't be annoying"

