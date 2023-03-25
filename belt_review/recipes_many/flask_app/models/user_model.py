from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import recipe_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASS_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$')

class User:
    db = "recipes_many"
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.all_recipes = []

    @classmethod
    def save_user(cls, form_data): #save a user to database
        pw_hash = bcrypt.generate_password_hash(form_data['password'])
        user_data= {
            'first_name': form_data['first_name'], 
            'last_name': form_data['last_name'],
            'email': form_data['email'],
            'password': pw_hash
        }
        query = """
            INSERT INTO users (first_name, last_name, email, password) 
            VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        result = connectToMySQL(cls.db).query_db(query, user_data)
        return result #returning the id that was created

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        if results:
            user_objects=[]
            for row in results:
                one_user = cls(record)
                user_objects.append( one_user)
            return user_objects
        else:
            return None

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        # if len(result) < 1:
        if results:
            one_user = cls(results[0])
            return one_user
        return False

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            one_user = cls(result[0])
            return one_user
        return False

    @classmethod
    def get_user_with_recipes(cls, data):
        query = """ SELECT * FROM users
                    LEFT JOIN recipes ON users.id = recipes.user_id
                    WHERE users.id = %(users_id)s """
        results = connectToMySQL(cls.db).query_db(query, data)
        #creating a User instance from the database info of the user
        one_user = cls(results[0])
        for row in results:
            recipe_data = { #parsing out the database data for the recipe
                "id" : row["id"],
                "user_id" : row["user_id"],
                "name" : row["name"],
                "description" : row["description"],
                "instructions" : row["instructions"],
                "date_cooked" : row["date_cooked"],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at']
            }
            one_user.all_recipes.append(recipe_model.Recipe(recipe_data))
        return one_user #this will be used in the template


    @staticmethod
    def validate_register(form_data):
        is_valid = True
    #check if the user exists
        data = {"email" : form_data["email"]}
        valid_user = User.get_by_email(data)
    # registration validations
        if len(form_data['first_name']) < 2:
            flash("First name must be at least 2 characters.","register")
            is_valid = False
        if len(form_data['last_name']) < 2:
            flash("Last name must be at least 2 characters.","register")
            is_valid = False
        if form_data['confirm'] != form_data['password']:
            flash("Passwords don't match.","register")
            is_valid = False
        # if len(form_data["email"]) < 1:
        #     flash("Email must be added", "register")
        elif not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid Email format.","register")
            is_valid = False
        # elif User.get_by_email(form_data):
        if valid_user:
            flash("Email already registered.","register")
            is_valid = False


            """ activate to specify the password difficulty"""
        # if not PASS_REGEX.match(form_data["password"]):
        #     flash("Password must contain at least:","register") 
        #     flash("- a digit number","register")
        #     flash("- one uppercase letter","register")
        #     flash("- one lowercase letter","register")
        #     flash("- one digit","register")
        #     is_valid = False
        return is_valid

    @staticmethod
    def validate_login(form_data):
        is_valid= True
        
        email_data= { "email": form_data["login_email"]}
        valid_user = User.get_by_email(email_data)
        if not valid_user:
            flash('Something is wrong, check again.', "login")
            is_valid = False
        if valid_user:
            if not bcrypt.check_password_hash(valid_user.password, form_data['login_password']):
                flash('Invalid Credentials','login')
                is_valid = False
        return is_valid