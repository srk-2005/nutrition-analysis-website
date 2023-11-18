from flask import request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

# User Registration
def register_user(username, password):
    # Check if the username is already taken
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash('Username is already taken. Please choose another.', 'danger')
        return redirect(url_for('register'))

    # Create a new user
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('login'))
    except Exception as e:
        flash('An error occurred during registration. Please try again.', 'danger')
        return redirect(url_for('register'))

# User Login
def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        flash('Login successful. Welcome!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password. Please try again.', 'danger')
        return redirect(url_for('login'))

# User Logout
def logout_user():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))
