from pymongo import MongoClient
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class UserDAO:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["generator"]
        self.users_collection = self.db["users"]

    def get_user_by_email(self, email):
        return self.users_collection.find_one({"email": email})

    def create_user(self, name, email, password):
        self.users_collection.insert_one({
            "name": name,
            "email": email,
            "password": password
        })

    def authenticate_user(self, email, password):
        user = self.get_user_by_email(email)
        if user and bcrypt.check_password_hash(user["password"], password):
            return user
        return None
