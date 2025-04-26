# database.py
from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb://localhost:27017/")  # ou ton URI MongoDB Atlas
    db = client["generator"]  # Remplace par le nom de ta base de données
    return db
