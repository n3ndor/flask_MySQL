from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models import user_model, recipe_model

@app.route('/dashboard')
def index_dashboard():
    if 'user_id' not in session:
        return redirect('/user/login')
    all_recipes = recipe_model.Recipe.get_all_recipes({"id" : session["user_id"]})
    user = user_model.User.get_by_id({"id" : session["user_id"]})
    return render_template('dashboard.html', all_recipes = all_recipes, user = user)

@app.route("/dashboard/new_recipe")
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {'id':session['user_id']}
    user_the = user_model.User.get_by_id(user_data)
    return render_template("recipe_create.html", the_user = user_the)

@app.route("/dashboard/create", methods=["POST"])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if not recipe_model.Recipe.validate_recipe(request.form):
        return redirect("/dashboard/new_recipe")
    new_recipe = recipe_model.Recipe.save_recipe(request.form)
    return redirect(f"/dashboard")

@app.route('/recipes/<int:id>')
def read_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    recipe_one = recipe_model.Recipe.get_one_recipe({'id': id})
    user = user_model.User.get_by_id({"id" : session["user_id"]})
    return render_template('recipe_read.html', the_recipe = recipe_one,  user = user) 

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    recipe_one = recipe_model.Recipe.get_one_recipe({'id': id})

    return render_template('recipe_edit.html', the_recipe= recipe_one)

@app.route('/recipes/update/<int:id>', methods=['POST'])
def update_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    if not recipe_model.Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{id}')

    recipe_data = {
        'id': id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_cooked': request.form['date_cooked'],
    }
    recipe_model.Recipe.update_recipe(recipe_data)
    return redirect('/dashboard')

@app.route('/recipes/remove/<int:id>')
def remove_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    recipe_model.Recipe.remove_recipe({'id':id})
    return redirect('/dashboard')


@app.route('/recipes/like/<int:id>')
def like_recipes(id):
    if 'user_id' not in session:
        return redirect('/')
    like_data={
        "user_id": session['user_id'],
        "recipe_id":  id,
    }
    recipe_model.Recipe.like_recipes(like_data)
    return redirect("/dashboard")


@app.route('/recipes/unlike/<int:id>')
def unlike_recipes(id):
    if 'user_id' not in session:
        return redirect('/')
    like_data={
        "user_id": session['user_id'],
        "recipe_id":  id,
    }
    recipe_model.Recipe.unlike_recipes(like_data)
    return redirect("/dashboard")
