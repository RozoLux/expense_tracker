from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging


db = SQLAlchemy()
login_manager = LoginManager() # Create LoginManager instance

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:8954@localhost/expense_tracker'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'workhard'
    
        
    db.init_app(app)
    login_manager.init_app(app) # Initialize LoginManager with the app

    login_manager.login_view = 'main.login' # Ajust 'main.login' to login view's endpoint

    # User Loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from .models import Users # Import User model
        return Users.query.get(int(user_id))

    #... (rest of app factory)
    from .routes import main
    app.register_blueprint(main)    
  
    return app
