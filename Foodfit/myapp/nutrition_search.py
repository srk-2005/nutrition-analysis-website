from .models import Food
from app import db

# Function to search for nutritional information of a food
def search_nutritional_info(food_name, quantity):
    try:
        # Retrieve the nutritional data for the selected food from the database
        food = Food.query.filter_by(food_name=food_name).first()
        
        if food:
            # Calculate the nutrient intake based on the quantity
            carbs = food.carbs * quantity
            proteins = food.proteins * quantity
            fats = food.fats * quantity
            
            # Return the calculated nutritional information
            nutritional_info = {
                'food_name': food_name,
                'quantity': quantity,
                'carbs': carbs,
                'proteins': proteins,
                'fats': fats
            }
            
            return nutritional_info
        else:
            return None  # Food not found in the database
    except Exception as e:
        # Handle any errors that occur during the search
        return None

# Function to retrieve a list of all available foods for searching
def get_all_foods():
    foods = Food.query.all()
    return foods
