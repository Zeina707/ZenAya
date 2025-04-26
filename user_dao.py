from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['generator']
users_collection = db['users']

class UserDAO:
    @staticmethod
    def get_user_by_email(email):
        user = users_collection.find_one({"email": email})  # Requête MongoDB
        return user  # Retourne l'utilisateur ou None

    @staticmethod
    def create_user(name, email, password):
        user = {
            "name": name,
            "email": email,
            "password": password
        }
        users_collection.insert_one(user)  # Insérer un nouvel utilisateur dans MongoDB
