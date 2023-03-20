from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import authors_class

class Book:
    DB = "books_schema"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors_who_favorited = []

    @classmethod
    def get_books(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL(cls.DB).query_db(query)
        books = []
        for b in results:
            books_a.append(cls(b))
        return books

    @classmethod
    def save_book(cls, data):
        query = """ INSERT INTO books (title, num_of_pages)
            VALUES (%(title)s, %(num_of_pages)s);"""
        return  connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_books(cls, book_id):
        query = """SELECT * FROM books
            LEFT JOIN favorites ON books.id = favorited.book_id
            LEFT JOIN authors ON authors.id = favorites.author_id
            WHERE books.id=%(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        book = cls(results[0])

        for b in results:
            if b["authors.id"] == None:
                break
            data = {
                "id" : b["authors.id"],
                "name" : ["name"],
                "created_at" : b ["authors.created_at"],
                "updated_at" : b["authors.updated_at"]
            }
            book.authors_who_favorited.append(authors_class.Author(data))
        return book

    @classmethod
    def unfavorited_books(cls,data):
        query = """SELECT * FROM books 
        WHERE books.id 
        NOT IN ( SELECT book_id FROM favorites WHERE author_id = %(id)s );"""
        
        results = connectToMySQL(cls.DB).query_db(query,data)
        books = []
        for row in results:
            books.append(cls(row))
        return books

    @classmethod
    def update_books(cls, data):
        query = """ UPDATE books
            SET (title = %(title)s, num_of_pages = %(num_of_pages)s)
            WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def add_favorite(cls, data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s); "
        return connectToMySQL(cls.DB).query_db(query, data)