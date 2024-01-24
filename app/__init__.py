from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:8954@localhost/expense_tracker'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'workhard'
   

   
        
    db.init_app(app)

    #... (rest of app factory)
    from .routes import main
    app.register_blueprint(main)    
  
    return app
