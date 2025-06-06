from pymongo import MongoClient

class MongoDB:
    def __init__(self, db_name, uri="mongodb://localhost:27017/"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

# Initialisation de l'objet MongoDB
db = MongoDB("generator")
