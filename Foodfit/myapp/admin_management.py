from flask import request, flash, redirect, url_for, session
from .models import Admin, Foods
from . import db

# Admin Login
def login_admin(username, password):
    admin = Admin.query.filter_by(username=username, password=password).first()
    if admin:
        session['admin_id'] = admin.id
        flash('Admin login successful. Welcome!', 'success')
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Invalid admin credentials. Please try again.', 'danger')
        return redirect(url_for('admin_login'))

# Admin Logout
def logout_admin():
    session.pop('admin_id', None)
    flash('Admin has been logged out.', 'info')
    return redirect(url_for('admin_login'))

# Admin Food Entry
def add_food(food_name, carbs, proteins, fats):
    new_food = Foods(food_name=food_name, carbs=carbs, proteins=proteins, fats=fats)
    
    try:
        db.session.add(new_food)
        db.session.commit()
        flash('Food entry added successfully.', 'success')
        return redirect(url_for('admin_food_entry'))
    except Exception as e:
        flash('An error occurred during food entry. Please try again.', 'danger')
        return redirect(url_for('admin_food_entry'))
