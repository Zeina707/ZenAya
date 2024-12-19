from flask import request, jsonify, session
from flask_bcrypt import Bcrypt
from DAO.user_dao import UserDAO
from models.users import User
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["generator"]
bcrypt = Bcrypt()

user_dao = UserDAO(db)

class AuthController:
    @staticmethod
    def login():
        data = request.json
        user_data = user_dao.find_by_email(data["email"])
        if user_data and bcrypt.check_password_hash(user_data["password"], data["password"]):
            session["user_id"] = str(user_data["_id"])
            return jsonify({"message": "Login successful"}), 200
        return jsonify({"message": "Invalid credentials"}), 401

    @staticmethod
    def register():
        data = request.json
        if user_dao.find_by_email(data["email"]):
            return jsonify({"message": "Email already exists"}), 400
        hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
        new_user = User(data["name"], data["email"], hashed_password)
        user_dao.save(new_user)
        return jsonify({"message": "User registered successfully"}), 201
