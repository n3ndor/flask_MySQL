from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import u_class



class Recipe:
    db = "recipes_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_cooked = data["date_cooked"]
        self.u_30 = data["u_30"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
    
    @classmethod
    def save_recipe(cls, data):
        query = """ INSERT INTO recipes (user_id, name, description, instructions,date_cooked, u_30)
                VALUES (%(user_id)s, %(name)s, %(description)s, %(instructions)s, %(date_cooked)s ,%(u_30)s);"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @classmethod
    def get_one_recipe(cls, data):
        query = """ SELECT * FROM recipes 
                JOIN users on users.id = user_id
                WHERE recipes.id = %(id)s;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        one_recipe = cls(result[0])
        user_data = {
                "id" : result[0]["users.id"],
                "first_name" : result[0]['first_name'],
                "last_name" : result[0]['last_name'],
                "email" : result[0]['email'],
                "password" : "",
                "created_at" : result[0]['users.created_at'],
                "updated_at" : result[0]['users.updated_at']
            }
        
        one_recipe.creator = u_class.User(user_data)
        return one_recipe


    @classmethod
    def get_all_recipes(cls):
        query = """ SELECT * FROM recipes
                    JOIN users 
                    WHERE recipes.user_id = users.id; """
        results = connectToMySQL(cls.db).query_db(query)
        
        all_recipes = []
        for p in results:
            one_recipe = cls(p)
            user_data = {
                "id" : p["users.id"],
                "first_name" : p['first_name'],
                "last_name" : p['last_name'],
                "email" : p['email'],
                "password" : "",
                "created_at" : p['users.created_at'],
                "updated_at" : p['users.updated_at']
            }

            one_recipe.creator = u_class.User(user_data)
            all_recipes.append(one_recipe)
        return all_recipes

    @classmethod
    def update_recipe(cls, data):
        query = """ UPDATE recipes
                SET name = %(name)s, description = %(description)s, instructions = %(instructions)s , date_cooked = %(date_cooked)s, u_30 = %(u_30)s
                WHERE id = %(id)s; """
        results = connectToMySQL(cls.db).query_db(query, data)
        return results


    @classmethod
    def remove_recipe(cls, data):
        query = "DELETE FROM recipes WHERE recipes.id = %(id)s "
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if len(data['name']) < 2:
            flash("Name too short.")
            is_valid = False
        if len(data['description']) < 2:
            flash("Description too short.")
            is_valid = False
        if len(data['instructions']) < 2:
            flash("Instructions too short.")
            is_valid = False
        if data['date_cooked'] == '':
            flash("Cooked date missing.")
            is_valid = False
        if 'u_30' not in data:
            flash("Does it take 30 mins or less?")
            is_valid = False
        return is_valid