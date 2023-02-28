from flask_app.config.mysqlconnection import connectToMySQL
from .ninja import Ninja

class Dojo:
    ninjas = []
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.created.at= data["created.at"]
        self.updated.at = data["updated.at"]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos;"
        results = connectToMySQL("dojos_and_ninjas_schema")