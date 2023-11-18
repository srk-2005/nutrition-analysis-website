from database import db
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    # Add more fields as needed for user data

class FoodIntake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meal_type = db.Column(db.String(50), nullable=False)
    food_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    # Add more fields as needed for food intake data


class Admin(db.Model):
    # Admin model fields
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Foods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(100), nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    proteins = db.Column(db.Float, nullable=False)
    fats = db.Column(db.Float, nullable=False)

    def __init__(self, food_name, carbs, proteins, fats):
        self.food_name = food_name
        self.carbs = carbs
        self.proteins = proteins
        self.fats = fats

class UserFoodIntake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    food_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    meal = db.Column(db.String(20), nullable=False)

    def __init__(self, user_id, food_name, quantity, meal):
        self.user_id = user_id
        self.food_name = food_name
        self.quantity = quantity
        self.meal = meal

