from flask import render_template, redirect, request
from flask_app.models.dojo import Dojo
from flask_app import app

@app.route('/')
def index():
    return redirect('/dojos')

@app.route('/dojos')
def dojos():
    
    return render_template("index.html")