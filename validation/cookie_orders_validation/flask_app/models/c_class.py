from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Cookie:
    DB = "cookie_schema"
    def __init__(self,data):
        self.id = data["id"]
        self.customer = data["customer"]
        self.type = data["type"]
        self.quantity = data["quantity"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):
        query = "SELECT * from cookies;"
        results = connectToMySQL(cls.DB).query_db(query)

        order_list = []
        for o in results:
            order_list.append(cls(o))
        return order_list

    @classmethod
    def create(cls, data):

        query = """
                INSERT into cookies (customer, type, quantity)
                VALUES (%(customer)s, %(type)s, %(quantity)s);"""

        result = connectToMySQL(cls.DB).query_db(query, data)
        return result

    @classmethod
    def get_one(cls, order_id):
        query = "SELECT * FROM cookies WHERE id = %(id)s;"
        data = {"id": order_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def update(cls, data):

        query = """
                UPDATE cookies
                SET customer = %(customer)s, type = %(type)s, quantity = %(quantity)s, updated_at=NOW()
                WHERE id = %(id)s;"""

        result = connectToMySQL(cls.DB).query_db(query, data)
        return result