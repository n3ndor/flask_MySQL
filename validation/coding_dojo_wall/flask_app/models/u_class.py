from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASS_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$')

class User:
    db = "wall"
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_user(cls,data):
        pw_hash = bcrypt.generate_password_hash(data['password'])
        user_data= {
            'first_name': data['first_name'], 
            'last_name': data['last_name'],
            'email': data['email'],
            'password': pw_hash
        }
        query = """
            INSERT INTO users (first_name, last_name, email, password) 
            VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"""
        results = connectToMySQL(cls.db).query_db(query,user_data)
        return results

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
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])



    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validate_register(data):
        is_valid = True
        email_data = {"email" : data["email"]}
        valid_user = User.get_by_email(email_data)

        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters","register")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters","register")
            is_valid = False
        if data['confirm'] != data['password']:
            flash("Passwords don't match","register")
            is_valid = False
        if valid_user:
            flash("Email already taken.","register")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email format.","register")
            is_valid = False
        if not PASS_REGEX.match(data["password"]):
            flash("Password must contain at least:","register") 
            flash("- a digit number","register")
            flash("- one uppercase letter","register")
            flash("- one lowercase letter","register")
            flash("- one digit","register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid= True
        
        email_data= { "email": data["login_email"]}
        valid_user = User.get_by_email(email_data)
        if not valid_user:
            flash('Invalid Credentials', "login")
            is_valid=False
        if valid_user:
            if not bcrypt.check_password_hash(valid_user.password, data['login_password']):
                flash('Invalid Credentials','login')
                is_valid=False
        return is_valid