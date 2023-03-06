from flask_app.config.mysqlconnection import connectToMySQL

class Book:
    DB = "books_schema"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_books(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL(cls.DB).query_db(query)
        books_a = []
        for b in results:
            books_a.append(cls(b))
        return books_a

    @classmethod
    def save_book(cls, data):
        query = """ INSERT INTO books (title, num_of_pages)
            VALUES (%(title)s, %(num_of_pages)s);"""
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result

    @classmethod
    def get_book(cls, book_id):
        query = "SELECT * FROM books WHERE id=%(id)s;"
        data = {"id" : book_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        return cls(result[0])

    @classmethod
    def update_books(cls, data):
        query = """ UPDATE books
            SET (title = %(title)s, num_of_pages = %(num_of_pages)s)
            WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query, data)

