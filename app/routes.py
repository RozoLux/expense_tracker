from flask import Blueprint, current_app
from flask import jsonify
from .models import Users
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return ' Hello World !'

@main.route('/users')
def get_all_users():
    try :
        users = Users.query.all()
        return jsonify([user.to_dict() for user in users])
    except Exception as e:
        return jsonify({"error": "An error occurred"}), 500
    

