from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from myapp.models import Admin,db, Foods, UserFoodIntake, User  # Import the Admin model (adjust the import path as needed)
from config import Config
import mysql.connector
# from . import db  # Import the SQLAlchemy database instance (adjust the import path as needed)
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@localhost/nutrition_analysis_db'  # Replace with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(Config)
db = SQLAlchemy(app)

conn = mysql.connector.connect(user = 'root',password='12345',host = '127.0.0.1',database='nutrition_analysis_db')
cursor = conn.cursor()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Define your routes and views here
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Password and confirm password do not match.', 'danger')
        else:
            users = Users(username=username, password=password)
            db.session.add(users)
            db.session.commit()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Users.query.filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.id
            flash('Login successful. Welcome!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        # Add logic to display user dashboard here
        return render_template('dashboard.html')
    else:
        flash('You must log in first.', 'danger')
        return redirect(url_for('login'))

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Define the SQL query to check admin credentials
        query = "SELECT id FROM admins WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))

        admin_id = cursor.fetchone()  # Fetch the admin ID

        if admin_id:
            session['admin_id'] = admin_id[0]  # Store admin ID in the session
            flash('Admin login successful. Welcome!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials. Please try again.', 'danger')

        cursor.close()  # Close the cursor
        conn.close()  # Close the database connection

    return render_template('admin_login.html')


# Define the route for the admin dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_id' in session:
        # Fetch admin-specific data and render the admin dashboard template
        return render_template('admin_dashboard.html')
    else:
        flash('You must log in as an admin first.', 'danger')
        return redirect(url_for('admin_login'))

@app.route('/admin_food_entry', methods=['GET', 'POST'])
def admin_food_entry():
    if request.method == 'POST':
        food_name = request.form['food_name']
        carbs = float(request.form['carbs'])
        proteins = float(request.form['proteins'])
        fats = float(request.form['fats'])

        food = Foods(food_name=food_name, carbs=carbs, proteins=proteins, fats=fats)
        db.session.add(food)
        db.session.commit()
        flash('Food added successfully!', 'success')

    return render_template('admin_food_entry.html')

from datetime import datetime  # Import the datetime module

@app.route('/food_intake', methods=['GET', 'POST'])
def food_intake():
    if request.method == 'POST':
        food_name = request.form['food_name']
        quantity = float(request.form['quantity'])
        meal = request.form['meal']
        #date = request.form['date']  # Retrieve the date from the form
        
        # Get user ID from session
        user_id = session.get('user_id')
        
        if user_id:
            # Convert the date string to a datetime object
            #formatted_date = datetime.strptime(date, '%Y-%m-%d')
            
            # Assuming you have a MySQL table named 'user_food_intake' for storing food intake data
            insert_query = "INSERT INTO user_food_intake (user_id, food_name, quantity, meal) VALUES (%s, %s, %s, %s)"
            values = (user_id, food_name, quantity, meal)
            
            try:
                cursor.execute(insert_query, values)
                conn.commit()
                flash('Food intake logged successfully!', 'success')
            except mysql.connector.Error as err:
                # Handle any MySQL errors that occur during insertion
                flash(f"Error: {err}", 'danger')
        else:
            flash('User ID not found in session. Please log in.', 'danger')
            return redirect(url_for('login'))  # Redirect to login page if user ID is missing

    return render_template('food_intake.html')

#food search module
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        food_name = request.form.get('food_name')
        quantity = float(request.form.get('quantity'))  # Convert quantity to float

        # Fetch food data from the database based on the food name
        cursor.execute("SELECT proteins, carbs, fats FROM foods WHERE food_name = %s", (food_name,))
        food_data = cursor.fetchone()
        
        if food_data:
            # Calculate nutrition values based on quantity
            result = {
                "food_name": food_name,
                "quantity": quantity,
                "proteins": round(food_data[1] * quantity, 2),
                "carbs": round(food_data[0] * quantity, 2),
                "fats": round(food_data[2] * quantity, 2),
            }
        else:
            result = None  # Food not found

        return render_template('search.html', result=result)
    
    return render_template('search.html', result=None)

if __name__ == '__main__':
#    db.create_all()
    app.run(debug=True)
