from flask_app.config.mysqlconnection import connectToMySQL

class Ninja:

    def __init__(self, data):
        self.id = data['id']
        self.dojo_id = data['dojo_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_ninjas(cls):
        query = "SELECT * FROM ninjas"
        results = connectToMySQL("dojos_and_ninjas_schema").query_db(query)
        all_rows = []
        for row in results:
            all_rows.append( cls(row) )
        return all_rows

    @classmethod 
    def get_one_ninja(cls, ninja_id):
        query = "SELECT * FROM ninjas WHERE id=%(id)s;"
        data = {"id":ninja_id}
        result = connectToMySQL("dojos_and_ninjas_schema").query_db(query, data)
        print(result)
        return cls(result[0])

    @classmethod
    def get_ninjas_dojo(cls, dojo_id):
        query = "SELECT * FROM ninjas WHERE dojo_id=%(id)s;"
        data={"id":dojo_id}
        results = connectToMySQL("dojos_and_ninjas_schema").query_db(query, data)
        all_rows = []
        for row in results:
            all_rows.append( cls(row) )
        return all_rows

    @classmethod
    def save_ninja(cls, data):
        query = """
            INSERT INTO ninjas (first_name, last_name, age, dojo_id)
            VALUES (%(first_name)s, %(last_name)s, %(age)s, %(dojo_id)s);
        """
        results = connectToMySQL("dojos_and_ninjas_schema").query_db(query, data)
        return results

    @classmethod
    def update_ninja(cls, data):
        query="""UPDATE ninjas 
            SET first_name=%(first_name)s, last_name=%(last_name)s, age=%(age)s, dojo_id=%(dojo_id)s 
            WHERE id = %(id)s;"""
        return connectToMySQL("dojos_and_ninjas_schema").query_db(query, data)

    @classmethod
    def delete_ninja(cls,data):
        query="DELETE FROM ninjas WHERE id=%(id)s"
        results = connectToMySQL("dojos_and_ninjas_schema").query_db(query, data)
        return results
