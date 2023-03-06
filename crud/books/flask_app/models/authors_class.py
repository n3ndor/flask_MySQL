from flask_app.config.mysqlconnection import connectToMySQL

class Author:
    DB = "books_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.created_at= data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def get_authors(cls):
        query = "SELECT * FROM authors;"
        results = connectToMySQL(cls.DB).query_db(query)
        authors_a = []
        for a in results:
            authors_a.append(cls(a))
        return authors_a

    @classmethod
    def save_author(cls, data):
        query = """ INSERT INTO authors (name)
            VALUES (%(name)s);"""
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result

    @classmethod
    def get_author(cls, author_id):
        query = "SELECT * FROM authors WHERE id=%(id)s;"
        data = {"id" : author_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        return cls(result[0])

    @classmethod
    def update_authors(cls, data):
        query = """ UPDATE authors
            SET name = %(name)s
            WHERE id = %(id)s"""
        return connectToMySQL(cls.DB).query_db(query, data)