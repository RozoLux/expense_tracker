from flask import Blueprint, current_app, render_template, url_for, flash, redirect, jsonify, abort
from .models import Users, Expenses, Categories # Import Users model
from . import db
from .forms import RegistrationForm, LoginForm, ExpenseForm 
from werkzeug.security import generate_password_hash
from flask_login import login_user, current_user, login_required, logout_user
from sqlalchemy import func



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
    return render_template('register.html', title= 'Register', form=form )

@main.route('/login', methods=['GET', 'POST'])
def login(): 
    form = LoginForm()

    if form.validate_on_submit():
        #Form is valid, proceed with authentication
        user = Users.query.filter_by(name=form.username.data).first()
        print(f"User found: {user}")

        if user and user.check_password(form.password.data):
            # User is authenticated, log them in
            login_user(user)
            flash('Login succesful !', 'succes')
            return redirect(url_for('main.home'))
        else:
            print("Password check failed")
            flash('Login Unsuccessful.Please check username and password', 'danger')

    return render_template('login.html', title='Login', form=form)

@main.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expenses(userid=current_user.userid, 
                           amount=form.amount.data,
                           description=form.description.data,
                           date=form.date.data,
                           categoryid=form.categoryid.data)
        db.session.add(expense)
        db.session.commit()
        flash('Your expense has been added !', 'succes')
        return redirect(url_for('main.view_expenses'))
    return render_template('add_expense.html', form=form)

@main.route('/expenses')
@login_required
def view_expenses():
    expenses = Expenses.query.filter_by(userid=current_user.userid).order_by(Expenses.date.desc()).all()
    return render_template('expenses.html', expenses=expenses)

@main.route('/delete_expense/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expenses.query.get_or_404(expense_id)
    if expense.userid != current_user.userid:
        abort(403) # Prevent deleting someone else's expense
    db.session.delete(expense)
    db.session.commit()
    flash('Your expense has been deleted!', 'success')
    return redirect(url_for('main.view_expenses'))

@main.route('/edit_expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id) :
    expense = Expenses.query.get_or_404(expense_id)
    if expense.userid != current_user.userid:
        abort(403) # Prevent editing someone else's expense
    form = ExpenseForm(obj=expense) # Pre-fill form
    if form.validate_on_submit():
        expense.amount = form.amount.data
        expense.categoryid = form.categoryid.data
        expense.description = form.description.data
        expense.data = form.date.data
        db.session.commit()
        flash('Expense updated successfully.', 'success')
        return redirect (url_for('main.view_expenses'))
    return render_template('edit_expense.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    # #aggregate expenses by category 
    # expenses_by_category = db.session.query(Expenses.categoryid, func.sum(Expenses.amount).label('total_amount')).group_by(Expenses.categoryid).filter(Expenses.userid==current_user.userid).all()

     #aggregate expenses by category 
    expenses_by_category = db.session.query(Categories.categoryname, func.sum(Expenses.amount).label('total_amount')).group_by(Categories.categoryname).filter(Expenses.userid==current_user.userid).all()

    # Total expenses
    total_expenses=db.session.query(func.sum(Expenses.amount)).filter(Expenses.userid==current_user.userid)

    # Aggregate expense by category for the current user
    expenses_data = db.session.query(Expenses.categoryid, func.sum(Expenses.amount).label('total_amount')).group_by(Expenses.categoryid).filter(Expenses.userid == current_user.userid).all()

    # Calculate the total expenses for the current user 
    total_expenses = db.session.query(func.sum(Expenses.amount)).filter(Expenses.userid == current_user.userid).scalar()

    #Prepare data for Chart.js
    categories = [data.categoryid for data in expenses_data]
    totals = [float(data.total_amount) for data in expenses_data]

    return render_template('dashboard.html', expenses_by_category= expenses_by_category, total_expenses=total_expenses, categories=categories, totals=totals)