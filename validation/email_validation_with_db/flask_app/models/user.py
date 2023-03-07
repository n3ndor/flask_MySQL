from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    DB ="users_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('users_schema').query_db(query)
        users = []
        
        for everybody in results:
            users.append(cls(everybody))
        return users
    
    @classmethod
    def save(cls, data):
        query = """ 
            INSERT INTO users ( first_name, last_name, email)
            VALUES (%(first_name)s, %(last_name)s, %(email)s);
        """
        results = connectToMySQL("users_schema").query_db(query, data)
        return results

    @classmethod
    def update(cls, data):
        query = """ 
            UPDATE users
            SET first_name = %(first_name)s, last_name = %(last_name)s,
                email = %(email)s, updated_at=NOW()
            WHERE id = %(id)s;
        """
        return connectToMySQL("users_schema").query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = """DELETE FROM users 
            WHERE id = %(id)s"""
        return connectToMySQL("users_schema").query_db(query, data)


    @classmethod
    def get_one(cls, data):
        query = """SELECT * FROM users
                WHERE id = %(id)s """
        results = connectToMySQL("users_schema").query_db(query, data)
        return cls(results[0])

    @staticmethod
    def valid_user(user_info):
        is_valid = True
        

        if len(user_info["first_name"]) < 1:
            flash("First name required!")
            is_valid = False
        if len(user_info["last_name"]) < 1:
            flash("Last name required!")
            is_valid = False
        if len(user_info["email"]) < 1:
            flash("Email required!")
            is_valid = False
        if not EMAIL_REGEX.match(user_info['email']): 
            flash("Invalid email format, add like: 'example@mail.com'")
            is_valid = False
        
        if user_info['email'] == DB["email"]:
            flash("Email already in database")
            is_valid = False
        return is_valid



    # @staticmethod
    # def validate_burger(burger):
    #     is_valid = True # we assume this is true
    #     if len(burger['name']) < 3:
    #         flash("Name must be at least 3 characters.")
    #         is_valid = False
    #     if len(burger['bun']) < 3:
    #         flash("Bun must be at least 3 characters.")
    #         is_valid = False
    #     if int(burger['calories']) < 200:
    #         flash("Calories must be 200 or greater.")
    #         is_valid = False
    #     if len(burger['meat']) < 3:
    #         flash("Bun must be at least 3 characters.")
    #         is_valid = False
    #     return is_valid
