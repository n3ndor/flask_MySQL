from flask_app.config.mysqlconnection import connectToMySQL
from .ninja_class import Ninja

class Dojo:
    
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.created_at= data["created_at"]
        self.updated_at = data["updated_at"]


    @classmethod
    def get_all_dojos(cls):
        query = "SELECT * FROM dojos;"
        results = connectToMySQL("dojos_and_ninjas_schema").query_db(query)
        dojos_a = []
        for i in results:
            dojos_a.append(cls(i))
        return dojos_a

    @classmethod
    def get_one_dojo(cls, dojo_id):
        query = "SELECT * FROM dojos WHERE id=%(id)s;"
        data = {"id":dojo_id}
        result = connectToMySQL("dojos_and_ninjas_schema").query_db(query, data)
        return cls(result[0])
        

    @classmethod
    def save_dojo(cls, data):
        query=""" INSERT INTO dojos (name) 
            VALUES (%(name)s);"""
        result = connectToMySQL("dojos_and_ninjas_schema").query_db(query,data)
        return result


    @classmethod
    def update_dojo(cls, data):
        query="""UPDATE dojos 
            SET name=%(name)s 
            WHERE id=%(id)s"""
        return connectToMySQL("dojos_and_ninjas_schema").query_db(query, data)

    @classmethod
    def delete_dojo(cls, dojo_id):
        query="DELETE FROM dojos WHERE id=%(id)s"
        data = {"id":dojo_id}
        return connectToMySQL("dojos_and_ninjas_schema").query_db(query, data)
