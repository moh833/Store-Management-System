import secrets
import os
from functools import wraps
from flask import render_template, url_for, flash, redirect, request, abort, session
from store import app, db, bcrypt, mail
from store.models import Main_item, BoughtItem, SoldItem, Expenses, Employee
from store.forms import (LoginForm, SoldItemForm, BoughtItemForm, DebtForm, 
 						EmployeeAccountForm, RequestResetForm, ResetPasswordForm,
						 AddEmpForm, AddExpensesForm)
from flask_login import login_user, current_user, logout_user, login_required

from flask_mail import Message

import datetime

print(os.getcwd())

def required_roles(*roles):
	def wrapper(func):
		@wraps(func)
		def wrapped(*args, **kwargs):
			if session['ROLE'] in roles:
				return func(*args, **kwargs)
			flash('You don\'t have permission to access this page!', 'danger')
			return redirect(url_for('home'))
		return wrapped
	return wrapper


def choices_from_file(name, file):
	with open('choices_files/' + file, encoding="utf-8") as f:
		data = f.readlines()
	data = [x.strip() for x in data]
	data = [(x, x) for x in data]
	return [('', name)] + data + [('other', 'Other')]

def add_choice_to_file(choice, file):
	with open('choices_files/' + file, 'a', encoding="utf-8") as f:
		f.write(f'{choice}\n')


@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/about/')
def about():
	return render_template('about.html', title='About')



@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		employee = Employee.query.filter_by(email=form.email.data.lower()).first()
		if employee and bcrypt.check_password_hash(employee.password, form.password.data):
			login_user(employee, remember=form.remember.data)
			session['ROLE'] = current_user.role
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Invalid credentials. Try Again.', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	session.pop('ROLE', None)
	return redirect(url_for('home'))


# @app.route('/search_for_item', methods=['GET', 'POST'])
# @login_required
# def search_for_item():
# 	form = SearchItemForm()
# 	item = None
# 	if form.validate_on_submit():
# 		# if form.search_by.data == 'name':
# 		# 	item = Main_item.query.filter_by(name=form.search.data).first()
# 		# elif form.search_by.data == 'type_':
# 		# 	item = Main_item.query.filter_by(type_=form.search.data).first()
# 		# elif form.search_by.data == 'car':
# 		# 	item = Main_item.query.filter_by(car=form.search.data).first()
# 		item = Main_item.query.filter_by(id=int(form.search.data)).first()
# 		if item:
# 			flash(f'{item}', 'success')
# 			return redirect(url_for('item_info', id=item.id))
# 		else:
# 			flash('That item doesn\'t exist', 'danger')
# 	return render_template('search_for_item.html', title='Search for Item', form=form)


@app.route('/<id>/item_info', methods=['GET', 'POST'])
@login_required
def item_info(id):
	item = Main_item.query.filter_by(id=int(id)).first()
	if not item:
		flash('This Item Doesn\'t exist', 'danger')
		return redirect(url_for('home'))
	form = SoldItemForm()
	if form.validate_on_submit():
		item.current_quantity -= form.quantity.data
		sold_item = SoldItem(item_id=item.id)
		sold_item.sold_quantity = form.quantity.data
		sold_item.paid_price = form.paid_price.data
		sold_item.sale = form.sale.data
		sold_item.customer = form.customer.data
		sold_item.time = datetime.datetime.now().replace(microsecond=0)
		sold_item.debt = (item.selling_price * int(form.quantity.data)) - (float(form.paid_price.data) + float(form.sale.data))
		# flash(f'{item.selling_price}, {form.quantity.data}, \
		# {form.paid_price.data}, {form.sale.data}', 'success')

		if item.current_quantity <= item.risk_quantity:
			item.ran_out = True
		db.session.add(sold_item)
		db.session.commit()
		flash(f'{sold_item.sold_quantity} of {item.name} has been\
		 sold', 'success')
		return redirect(url_for('home'))
	elif request.method == 'GET':
		form.quantity.data = 1
		form.paid_price.data = item.selling_price
		form.sale.data = 0
	return render_template('item_info.html', title='Item\'s info', form=form, item=item)


@app.route('/buy_item', methods=['GET', 'POST'])
@login_required
@required_roles('admin')
def buy_item():
	form = BoughtItemForm()
	form.name.choices = choices_from_file('Item\'s Name', 'name.txt')
	form.company.choices = choices_from_file('Company', 'company.txt')
	form.country.choices = choices_from_file('Country', 'country.txt')
	form.distributer.choices = choices_from_file('Distributer', 'distributer.txt')
	form.family.choices = choices_from_file('Family', 'family.txt')
	form.place.choices = choices_from_file('Place', 'place.txt')
	if form.validate_on_submit():
		bought_item = BoughtItem()
		main_item = Main_item.query.filter_by(name=form.name.data, 
			company=form.company.data, country=form.country.data, 
			distributer=form.distributer.data, family=form.family.data).first()
		if not main_item:
			main_item = Main_item()
			main_item.current_quantity = form.quantity.data
			db.session.add(main_item)
		else:
			main_item.current_quantity += form.quantity.data

		if form.name.data == 'other':
			main_item.name = form.other_name.data
			add_choice_to_file(form.other_name.data, 'name.txt')
		else:
			main_item.name = form.name.data
		
		if form.company.data == 'other':
			main_item.company = form.other_company.data
			add_choice_to_file(form.other_company.data, 'company.txt')
		else:
			main_item.company = form.company.data

		if form.country.data == 'other':
			main_item.country = form.other_country.data
			add_choice_to_file(form.other_country.data, 'country.txt')
		else:
			main_item.country = form.country.data

		if form.distributer.data == 'other':
			main_item.distributer = form.other_distributer.data
			add_choice_to_file(form.other_distributer.data, 'distributer.txt')
		else:
			main_item.distributer = form.distributer.data

		if form.family.data == 'other':
			main_item.family = form.other_family.data
			add_choice_to_file(form.other_family.data, 'family.txt')
		else:
			main_item.family = form.family.data

		if form.place.data == 'other':
			main_item.place = form.other_place.data
			add_choice_to_file(form.other_place.data, 'place.txt')
		else:
			main_item.place = form.place.data

		main_item.selling_price = form.selling_price.data
		
		main_item.risk_quantity = form.risk_quantity.data
		if main_item.current_quantity <= form.risk_quantity.data:
			main_item.ran_out = True
		# db.session.add(main_item)
		db.session.commit()

		bought_item.item_id = main_item.id
		bought_item.time = datetime.datetime.now().replace(microsecond=0)
		bought_item.buying_price = form.buying_price.data
		bought_item.bought_quantity = form.quantity.data
		db.session.add(bought_item)
		db.session.commit()


		flash(f"{bought_item.bought_quantity} of {main_item.name} has been added\
			for {bought_item.buying_price} each, You have now\
				{main_item.current_quantity} of {main_item.name}'s", 'success')
		return redirect(url_for('home'))
	elif request.method == 'GET':
		pass
		# form.name.choices = choices_from_file('name', 'name.txt')
		# form.company.choices = choices_from_file('company', 'company.txt')
		# form.country.choices = choices_from_file('country', 'country.txt')
		# form.distributer.choices = choices_from_file('distributer', 'distributer.txt')
		# form.family.choices = choices_from_file('family', 'family.txt')
		# form.place.choices = choices_from_file('place', 'place.txt')
	return render_template('buy_item.html', title='Buy Item', form=form)



@app.route('/debts')
@login_required
def display_debts():
	debts = SoldItem.query.filter(SoldItem.debt!=0.0).all()
	return render_template('display_debts.html', title='Debts', sold_items=debts)


@app.route('/debts/<id>', methods=['GET', 'POST'])
@login_required
def debt(id):
	sold_item = SoldItem.query.filter_by(id=int(id)).first()
	if not sold_item:
		flash('Not Found', 'danger')
		return redirect(url_for('display_debts'))
	form = DebtForm()
	if form.validate_on_submit():
		if form.sale.data:
			sold_item.sale += float(form.sale.data)
		sold_item.paid_price += float(form.paid_money.data)
		sold_item.debt -=  (float(form.sale.data) + float(form.paid_money.data))
		db.session.commit()
		return redirect(url_for('display_debts'))
	elif request.method == 'GET':
		form.sale.data = 0.0
		form.paid_money.data = sold_item.debt
	return render_template('debt.html', title='Debts', form=form, sold_item=sold_item)


@app.route('/add_expenses', methods=['GET', 'POST'])
@login_required
def add_expenses():
	form = AddExpensesForm()
	if form.validate_on_submit():
		expense = Expenses()
		expense.name = form.name.data
		expense.paid_price = form.paid_money.data
		expense.time = form.time.data
		db.session.add(expense)
		db.session.commit()
		flash('Expense added successfully', 'success')
		return redirect(url_for('add_expenses'))
	return render_template('add_expense.html', title='Add Expense', form=form)



@app.route('/employee_account', methods=['GET', 'POST'])
@login_required
def employee_account():
	form = EmployeeAccountForm()
	if form.validate_on_submit():
		current_user.fname = form.fname.data
		current_user.lname = form.lname.data
		current_user.email = form.email.data.lower()
		current_user.phone = form.phone.data
		db.session.commit()
		flash('Your account has been updated!', 'success')
		return redirect(url_for('employee_account'))
	elif request.method == 'GET':
		form.fname.data = current_user.fname
		form.lname.data = current_user.lname
		form.email.data = current_user.email
		form.phone.data = current_user.phone
		if current_user.salary:
			form.salary.data = current_user.salary
		if current_user.incentive:
			form.incentive.data = current_user.incentive

	return render_template('employee_account.html', title='Account', form=form)




@app.route('/add_employee', methods=['GET', 'POST'])
@login_required
@required_roles('admin')
def add_emp():
	form = AddEmpForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		emp = Employee(fname=form.fname.data, lname=form.lname.data, email=form.email.data.lower(),
					 phone=form.phone.data, role=form.role.data
					 , password=hashed_password)
		if form.salary.data:
			emp.salary = form.salary.data
		if form.incentive.data:
			emp.incentive = form.incentive.data
		db.session.add(emp)
		db.session.commit()
		flash('A new Employee has been added successfully', 'success')
		return redirect(url_for('add_emp'))
	return render_template('add_employee.html', title='Add Employee', form=form)





#-------------------------------------------------
# 'noreply@demo.com'
def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request',
				sender=app.config['MAIL_USERNAME'],
				recipients=[user.email])
	msg.body = f'''To reset your password, visit the following link or copy it to your browser:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
	mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		emp = Employee.query.filter_by(email=form.email.data.lower()).first()
		if emp:
			send_reset_email(emp)
		flash('An email has been sent with instructions to reset your password.', 'info')
		return redirect(url_for('login'))
	return render_template('reset_request.html', title='Reset Password', form=form)
	


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	emp = Employee.verify_reset_token(token)	
	if emp is None:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		if emp:
			emp.password = hashed_password
		db.session.commit()
		flash('Your password has been updated! You are now able to login', 'success')
		return redirect(url_for('login'))
	return render_template('reset_token.html', title='Reset Password', form=form)


# --------------------------errors--------------------------------------


@app.errorhandler(404)
def error_404(error):
	return render_template('errors/404.html'), 404


@app.errorhandler(403)
def error_403(error):
	return render_template('errors/403.html'), 403


@app.errorhandler(500)
def error_500(error):
	return render_template('errors/500.html'), 500
