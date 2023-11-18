import os

class Config:
    # Set the secret key for your application (used for session management, etc.)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'

    # Configure the database URL for SQLAlchemy (adjust as needed)
    SQLALCHEMY_DATABASE_URI = 'mysql://root:12345@localhost/nutrition_analysis_db'

    # Disable modification tracking for SQLAlchemy (optional)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

