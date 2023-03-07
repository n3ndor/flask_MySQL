# __init__.py

from flask import Flask
app = Flask(__name__)

app.secret_key = "don't tell me this is a secret"

