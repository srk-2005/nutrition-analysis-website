from flask import request, flash, redirect, url_for, session
from .models import UserFoodIntake, Food
from . import db

# Log Food Intake
def log_food_intake(user_id, meal_type, food_name, quantity):
    # Retrieve the nutritional data for the selected food from the database
    food = Food.query.filter_by(food_name=food_name).first()
    
    if food:
        # Calculate the nutrient intake based on the quantity
        carbs = food.carbs * quantity
        proteins = food.proteins * quantity
        fats = food.fats * quantity
        
        # Create a new food intake entry
        food_intake = UserFoodIntake(
            user_id=user_id,
            meal_type=meal_type,
            food_name=food_name,
            quantity=quantity,
            carbs=carbs,
            proteins=proteins,
            fats=fats
        )
        
        try:
            db.session.add(food_intake)
            db.session.commit()
            flash('Food intake logged successfully.', 'success')
        except Exception as e:
            flash('An error occurred while logging food intake. Please try again.', 'danger')
    else:
        flash('Food not found in the database. Please check the name and try again.', 'danger')
    
    return redirect(url_for('food_intake'))

# Get User's Food Intake
def get_user_food_intake(user_id):
    user_food_intake = UserFoodIntake.query.filter_by(user_id=user_id).all()
    return user_food_intake
