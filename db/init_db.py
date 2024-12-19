from pymongo import MongoClient
from flask_bcrypt import Bcrypt

# Initialiser la connexion MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["generator"]  # Nom de la base de données

# Initialiser bcrypt pour le hachage des mots de passe
bcrypt = Bcrypt()

def initialize_users():
    users_collection = db["users"]

    # Vérifier si la collection est vide
    if users_collection.count_documents({}) == 0:
        print("Initialisation des utilisateurs...")
        users = [
            {
                "name": "Aya Zenati",
                "email": "aya.zenati@example.com",
                "password": bcrypt.generate_password_hash("password123").decode('utf-8')
            },
            {
                "name": "Admin",
                "email": "admin@example.com",
                "password": bcrypt.generate_password_hash("adminpass").decode('utf-8')
            }
        ]
        users_collection.insert_many(users)
        print("Collection 'users' initialisée avec des données de test.")
    else:
        print("La collection 'users' est déjà initialisée.")

def initialize_templates():
    templates_collection = db["templates"]

    # Vérifier si la collection est vide
    if templates_collection.count_documents({}) == 0:
        print("Initialisation des templates...")
        templates = [
            {"title": "Template Moderne", "image": "/images/template_moderne.png", "path": "template1"},
            {"title": "Template Minimaliste", "image": "/images/template_minimaliste.png", "path": "template2"},
            {"title": "Template Coloré", "image": "/images/template_colore.png", "path": "template3"},
        ]
        templates_collection.insert_many(templates)
        print("Collection 'templates' initialisée avec des données de test.")
    else:
        print("La collection 'templates' est déjà initialisée.")

def main():
    try:
        initialize_users()
        initialize_templates()
        print("Base de données initialisée avec succès.")
    except Exception as e:
        print("Erreur lors de l'initialisation de la base de données :", e)
    finally:
        # Fermer la connexion
        client.close()

if __name__ == "__main__":
    main()
