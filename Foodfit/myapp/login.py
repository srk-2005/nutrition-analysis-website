from flask import Flask, render_template, flash, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from myapp.models import Admin, User, Food, UserFoodIntake  # Import your models
from config import Config

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@localhost/nutrition_analysis_db'  # Replace with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(Config)
db = SQLAlchemy(app)

# Define your login-related routes here

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Accessing the login route")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user is an admin
        admin = Admin.query.filter_by(username=username, password=password).first()
        if admin:
            session['admin_id'] = admin.id
            flash('Admin login successful. Welcome!', 'success')
            return redirect(url_for('admin_dashboard'))

        # Check if the user is a regular user
        user = User.query.filter_by(username=username, password=password).first()
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
        # Add logic to display the user dashboard here
        return "User Dashboard"
    else:
        flash('You must log in first.', 'danger')
        return redirect(url_for('login'))

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_id' in session:
        # Fetch admin-specific data and render the admin dashboard template
        return render_template('admin_dashboard.html')
    else:
        flash('You must log in as an admin first.', 'danger')
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Password and confirm password do not match.', 'danger')
        else:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')
