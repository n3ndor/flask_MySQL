# __init__.py

from flask import Flask

app = Flask(__name__)

app.secret_key = "All the recipes have a unique secret, such as this init file"

