from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models import r_class, u_class

@app.route('/wall')
def index_wall():
    if 'user_id' not in session:
        return redirect('/user/login')
    user_data = {"id":session['user_id']}
    user_the = u_class.User.get_by_id(user_data)
    recipe_the = r_class.Recipe.get_all_recipes()
    return render_template('wall.html', the_user = user_the, the_recipes = recipe_the)



@app.route("/wall/new_recipe")
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {'id':session['user_id']}
    user_the = u_class.User.get_by_id(user_data)
    return render_template("recipe_create.html", the_user = user_the)

@app.route("/wall/create", methods=["POST"])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if not r_class.Recipe.validate_recipe(request.form):
        return redirect("/wall/new_recipe")
    
    # data = {
    #     'user_id': session['user_id'],
    #     'name': request.form['name'],
    #     'description': request.form['description'],
    #     'instructions': request.form['instructions'],
    #     'date_cooked': request.form['date_cooked'],
    #     'u_30': request.form['u_30'],
    # }
    new_recipe = r_class.Recipe.save_recipe(request.form) #data

    return redirect(f"/wall")

@app.route('/recipes/<int:id>')
def read_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    recipe_one = r_class.Recipe.get_one_recipe({'id': id})
    print(recipe_one.creator)
    return render_template('recipe_read.html', the_recipe = recipe_one)

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    recipe_one = r_class.Recipe.get_one_recipe({'id': id})
    return render_template('recipe_edit.html', the_recipe= recipe_one)

@app.route('/recipes/update/<int:id>', methods=['POST'])
def update_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    if not r_class.Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{id}')

    recipe_data = {
        'id': id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_cooked': request.form['date_cooked'],
        'u_30': request.form['u_30'],
    }
    r_class.Recipe.update_recipe(recipe_data)
    return redirect('/wall')

@app.route('/recipes/remove/<int:id>')
def remove_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    r_class.Recipe.remove_recipe({'id':id})
    return redirect('/wall')

