from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.magazines = []

    @classmethod
    def add_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        results = connectToMySQL('magazines_db').query_db(query, data)
        return results
    
    @classmethod
    def update_user(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW() WHERE id = %(id)s"
        results = connectToMySQL('magazines_db').query_db(query, data)
        return results
    
    @classmethod
    def get_user_magazines(cls, user_id):
        query = "SELECT * FROM magazines WHERE user_id = %(user_id)s;"
        data = {'user_id': user_id}
        results = connectToMySQL("magazines_db").query_db(query, data)
        magazine_list = []
        for result in results:
            magazine_data = {
                'id': result['id'],
                'title': result['title'],
                'description': result['description'],
            }
            magazine_list.append(magazine_data)
        return magazine_list
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("magazines_db").query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL("magazines_db").query_db(query,data)
        if result:
            return cls(result[0])
        else:
            return None
    
    @staticmethod
    def validate_register(user):
        is_valid = True 
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('magazines_db').query_db(query, user)
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.", 'registration-error')
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.", 'registration-error')
            is_valid = False
        if len(results) >= 1:
            flash("Email is unavailable, choose another email", 'registration-error')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'registration-error')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", 'registration-error')
            is_valid = False
        if user['password'] != user['val-password']:
            flash("Passwords do not match.", 'registration-error')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_update(user):
        is_valid = True 
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('magazines_db').query_db(query, user)
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.", 'registration-error')
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.", 'registration-error')
            is_valid = False
        if user['email'] != user['old_email']:
            if len(results) >= 1:
                flash("Email is unavailable, choose another email", 'registration-error')
                is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'registration-error')
            is_valid = False
        return is_valid