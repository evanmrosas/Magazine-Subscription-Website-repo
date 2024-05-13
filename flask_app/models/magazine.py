from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Magazine:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_all_magazines(cls):
        query = "SELECT magazines.id, magazines.title, users.first_name, users.last_name FROM magazines INNER JOIN users ON magazines.user_id = users.id;"
        results = connectToMySQL('magazines_db').query_db(query)
        print("Results:", results)
        magazine_list = []
        for result in results:
            magazine_data = {
                'id': result['id'],
                'title': result['title'],
                'first_name': result['first_name'],
                'last_name': result['last_name']
                }
            magazine_list.append(magazine_data)
        return magazine_list
    
    @classmethod
    def add_magazine(cls, data):
            query = "INSERT INTO magazines (title, description, user_id, created_at, updated_at) VALUES (%(title)s, %(description)s, %(user_id)s, NOW(), NOW());"
            results = connectToMySQL('magazines_db').query_db(query, data)
            return results
    
    @classmethod
    def delete_magazine(cls, data):
        query = "DELETE FROM magazines WHERE id = %(id)s;"
        results = connectToMySQL('magazines_db').query_db(query, data)
        return results
    
    @classmethod
    def view_magazine(cls, data):
        query = "SELECT magazines.id, magazines.title, magazines.description, users.first_name, users.last_name FROM magazines INNER JOIN users ON magazines.user_id = users.id WHERE magazines.id = %(id)s"
        results = connectToMySQL('magazines_db').query_db(query, data)
        if results:
            result = results[0]
            magazine_data = {
                'id': result['id'],
                'title': result['title'],
                'description': result['description'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
            }
            return magazine_data
        else:
            return None
        
    @staticmethod
    def validate_magazine(magazine):
        is_valid = True 
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL('magazines_db').query_db(query, magazine)
        if len(magazine['title']) < 2:
            flash("Name must be at least 2 characters.")
            is_valid = False
        query = "SELECT * FROM magazines WHERE title = %(title)s"
        results = connectToMySQL('magazines_db').query_db(query, magazine)
        if isinstance(results, list) and len(results) >= 1:
            flash("Title is unavailable, choose another title")
            is_valid = False
        if len(magazine['description']) < 10:
            flash("Description must be at least 10 characters.")
            is_valid = False
        return is_valid