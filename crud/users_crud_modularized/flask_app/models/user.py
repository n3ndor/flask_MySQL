from flask_app.config.mysqlconnection import connectToMySQL

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


