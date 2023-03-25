from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user_model



class Recipe:
    db = "recipes_many"
    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data['user_id']
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_cooked = data["date_cooked"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.liked_by = []
    
    @classmethod
    def save_recipe(cls, data):
        query = """ INSERT INTO recipes (user_id, name, description, instructions,date_cooked)
                VALUES (%(user_id)s, %(name)s, %(description)s, %(instructions)s, %(date_cooked)s);"""
        return connectToMySQL(cls.db).query_db(query, data)
        
    
    @classmethod
    def get_one_recipe(cls, data):
        query = """ SELECT * FROM recipes 
                LEFT JOIN users on users.id = recipes.user_id
                LEFT JOIN likes ON likes.recipe_id = recipes.id
                LEFT JOIN users AS user_liked ON likes.user_id = user_liked.id
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
        one_recipe.creator = user_model.User(user_data)
        #check if there are any user who liked the recipe
        if result[0]["user_liked.id"]:
            #for every user who liked the recipe create a user object and add to liked_by list
            for row in result:
                #reference the name made during the JOIN AS
                liked_user_info = {
                    "id" : row["user_liked.id"],
                    "first_name" : row['user_liked.first_name'],
                    "last_name" : row['user_liked.last_name'],
                    "email" : row['user_liked.email'],
                    "password" : "",
                    "created_at" : row['user_liked.created_at'],
                    "updated_at" : row['user_liked.updated_at']
                }
                one_recipe.liked_by.append(user_model.User(liked_user_info))
        return one_recipe


    @classmethod
    def get_all_recipes(cls, id):
        query = """ SELECT * FROM recipes
                    LEFT JOIN users ON recipes.user_id = users.id
                    LEFT JOIN likes ON recipes.id = likes.recipe_id AND likes.user_id = %(id)s
                    LEFT JOIN users AS user_liked ON likes.user_id = user_liked.id; """
        results = connectToMySQL(cls.db).query_db(query, id)
        
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

            one_recipe.creator = user_model.User(user_data)
            #check if user liked the recipe
            if p["user_liked.id"]:
                liked_user_info = {
                "id" : p["user_liked.id"],
                "first_name" : p['user_liked.first_name'],
                "last_name" : p['user_liked.last_name'],
                "email" : p['user_liked.email'],
                "password" : "",
                "created_at" : p['user_liked.created_at'],
                "updated_at" : p['user_liked.updated_at']
                }
                one_recipe.liked_by.append(user_model.User(liked_user_info))
            all_recipes.append(one_recipe)
        return all_recipes

    @classmethod
    def get_one_recipe_user_likes(cls):
        query='''
            SELECT * FROM recipes
            LEFT JOIN users
            ON recipes.user_id = users.id
            LEFT JOIN likes
            ON likes.recipe_id = recipes.id
            LEFT JOIN users AS user_liked
            ON likes.user_id = user_liked.id;

            '''
        results= connectToMySQL(cls.db).query_db(query)
        all_recipes= []
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
            one_recipe.creator= user_model.User(user_data)
            one_recipe.liked_by.append(p['likes.user_id'])
            all_recipes.append(one_recipe)
            print(one_recipe.liked_by)
        return all_recipes

    @classmethod
    def like_recipes(cls,data):
        query='''
            INSERT INTO likes(user_id, recipe_id)
            VALUES(%(user_id)s,%(recipe_id)s);
        '''
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    
    @classmethod
    def unlike_recipes(cls,data):
        query='''
        DELETE FROM likes
        WHERE likes.user_id= %(user_id)s
        AND likes.recipe_id=%(recipe_id)s;
        '''
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def update_recipe(cls, data):
        query = """ UPDATE recipes
                SET name = %(name)s, description = %(description)s, instructions = %(instructions)s , date_cooked = %(date_cooked)s
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
            flash("Name too short, at least 2 characters.")
            is_valid = False
        if len(data['description']) < 2:
            flash("Description too short, at least 2 characters.")
            is_valid = False
        if len(data["instructions"]) < 2:
            flash("Instructions too short, at least 2 characters.")
            is_valid = False
        if data['date_cooked'] == '':
            flash("Cooked date missing.")
            is_valid = False

        return is_valid