from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import books_class

class Author:
    DB = "books_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.favorite_books = []
        self.created_at= data["created_at"]
        self.updated_at = data["updated_at"]
        self.favorite_books = []
    
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
        return connectToMySQL(cls.DB).query_db(query, data)

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

    @classmethod
    def add_favorite(cls,data):
        query = "INSERT INTO favorites (author_id,book_id) VALUES (%(author_id)s,%(book_id)s);"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def unfavorited_authors(cls, data):
        query = """ SELECT * FROM authors
            WHERE authors.id 
            NOT IN (SELECT author_id FROM favorites WHERE book_id = %(id)s);
            """
        result = connectToMySQL(cls.DB).query_db(query, data)
        authors = []
        for a in results:
            authors.append(cls(a))
        return authors

    @classmethod
    def get_by_id(cls,data):
        query = """SELECT * FROM authors 
            LEFT JOIN favorites ON authors.id = favorites.author_id 
            LEFT JOIN books ON books.id = favorites.book_id 
            WHERE authors.id = %(id)s;"""
        results = connectToMySQL('books').query_db(query,data)
        author = cls(results[0])
        
        for row in results:
            if row['books.id'] == None:
                break
            data = {
                "id": row['books.id'],
                "title": row['title'],
                "num_of_pages": row['num_of_pages'],
                "created_at": row['books.created_at'],
                "updated_at": row['books.updated_at']
            }
            author.favorite_books.append(book.Book(data))
        return author