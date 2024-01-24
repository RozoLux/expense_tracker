from flask import Blueprint, current_app, render_template, url_for, flash, redirect, jsonify
from .models import Users
from . import db
from .forms import RegistrationForm
from werkzeug.security import generate_password_hash


main = Blueprint('main', __name__)

@main.route('/')
def home():
    try :
        users = Users.query.all()
        return render_template('index.html', users=users) # users is a list of user objects passed to the index.html template. 
    except Exception as e :
        return render_template('index.html', error=str(e))

@main.route('/users')
def get_all_users():
    try :
        users = Users.query.all()
        return jsonify([user.to_dict() for user in users])
    except Exception as e:
        return jsonify({"error": "An error occurred"}), 500
    
@main.route('/register', methods= ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Process form data
        hashed_password = generate_password_hash(form.password.data)
        new_user = Users(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('registration.html', title= 'Register', form=form )
    


