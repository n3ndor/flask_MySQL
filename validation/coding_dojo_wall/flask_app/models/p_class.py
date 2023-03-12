from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.u_class import User

class Post:
    db = "wall"
    def __init__(self, data):
        self.id = data["id"]
        self.content = data["content"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = data["user"]
    
    @classmethod
    def save(cls, data):
        if not cls.validate_post(data):
            return False
        query = """ INSERT INTO wall.posts (user_id, content)
                    VALUES (%(user_id)s, %(content)s);"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @classmethod
    def get_all(cls):
        query = """SELECT * FROM posts
                JOIN users on posts.user_id = users.id"""
        results = connectToMySQL(cls.db).query_db(query)
        all_post = []
        for p in results:
            one_user = User({
                "id" : p["user_id"],
                "first_name" : p['first_name'],
                "last_name" : p['last_name'],
                "email" : p['email'],
                "password" : p['password'],
                "created_at" : p['created_at'],
                "updated_at" : p['updated_at']
                })
            new_post = Post({
                "id" : p["id"],
                "content" : p["content"],
                "created_at" : p['created_at'],
                "updated_at" : p['updated_at'],
                "user" : one_user
            })
            all_post.append(new_post)
        return all_post


    @classmethod
    def delete(cls, post_id):
        query = "DELETE FROM posts WHERE id = %(id)s "
        connectToMySQL(cls.db).query_db(query, {"id" : post_id})
        return post_id

    @classmethod
    def validate_post(cls, data):
        is_valid = False
        if len(data["content"]) < 1:
            flash("Empty Posts are not allowed")
            flash("Add some text first")
            is_valid = False
        return is_valid