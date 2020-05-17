from store.models import Main_item, BoughtItem, SoldItem, Employee
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import DateField
import re
 

from store import app

# def choices_from_file(name, file):
# 	with open('choices_files/' + file, encoding="utf-8") as f:
# 		data = f.readlines()
# 	data = [x.strip() for x in data]
# 	data = [(x, x) for x in data]
# 	return [('', name)] + [('other', 'Other')] + data

choices = {'role': [('', 'Role'), ('admin', 'Admin'), ('regular', 'Regular')], 
			'search_by': [('', 'Search By'), ('name', 'Name')
			, ('type_', 'Type'), ('car', 'Car')]}

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)], render_kw={'autofocus': 'true'})
	password = PasswordField('Password', validators=[DataRequired(), Length(max=50)])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

# class SearchItemForm(FlaskForm):
# 	search = IntegerField('ID', validators=[DataRequired()], render_kw={'autofocus': 'true'})
# 	# search_by = SelectField('Serach By', validators=[DataRequired()], choices = choices.get('search_by'))
# 	submit = SubmitField('Search')

class SoldItemForm(FlaskForm):
	# time = DateField('Time', format='%Y-%m-%d', validators=[DataRequired()])
	quantity = IntegerField('Quantity', validators=[DataRequired()])
	paid_price = FloatField('Paid Price', validators=[DataRequired()])
	sale = FloatField('Sale')
	customer = StringField('Customer', validators=[Length(max=100)])

	submit = SubmitField('Sell')
# ['name', 'company', 'country', 'distributer', 'car_family', 'car_name', 'place']
class BoughtItemForm(FlaskForm):
	name = SelectField('Item\'s Name', validators=[DataRequired()], render_kw={'autofocus': 'true'})
	company = SelectField('Company', validators=[DataRequired()])
	country = SelectField('Country', validators=[DataRequired()])
	distributer = SelectField('Distributer', validators=[DataRequired()])
	family = SelectField('Family', validators=[DataRequired()])
	place = SelectField('Place', validators=[DataRequired()])

	other_name = StringField('Items\'s Name', validators=[Length(max=100)])
	other_company = StringField('Company', validators=[Length(max=100)])
	other_country = StringField('Country', validators=[Length(max=100)])
	other_distributer = StringField('Distributer', validators=[Length(max=100)])
	other_family = StringField('Family', validators=[Length(max=100)])
	other_place = StringField('Place', validators=[Length(max=100)])

	quantity = IntegerField('Quantity', validators=[DataRequired()])
	buying_price = FloatField('Buying Price', validators=[DataRequired()])
	selling_price = FloatField('Selling Price', validators=[DataRequired()])


	risk_quantity = IntegerField('Risk Quantity', validators=[DataRequired()])
	submit = SubmitField('Buy')



class DebtForm(FlaskForm):
	sale = FloatField('Sale')
	paid_money = FloatField('Paid Money', validators=[DataRequired()])

	submit = SubmitField('Edit')


class AddExpensesForm(FlaskForm):

	name = StringField('Type', validators=[Length(max=100)])
	paid_money = FloatField('Paid Money', validators=[DataRequired()])
	time = DateField('Time', format='%Y-%m-%d', validators=[DataRequired()])

	submit = SubmitField('Add')


class EmployeeAccountForm(FlaskForm):
	fname = StringField('First Name', validators=[DataRequired(), Length(max=50)], render_kw={'autofocus': 'true'})
	lname = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
	email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
	phone = StringField('Phone', validators=[DataRequired()])

	salary = FloatField('Salary', render_kw={'disabled': 'true'})
	incentive = FloatField('Incentive', render_kw={'disabled': 'true'})

	submit = SubmitField('Update')


	def validate_phone(self, phone):
		if phone.data != current_user.phone:
			employee = Employee.query.filter_by(phone=phone.data).first()
			if employee:
				raise ValidationError('That Phone is already registered.')
			if re.search('[a-zA-Z]', phone):
				raise ValidationError('Please enter a valid phone Number.')



	def validate_email(self, email):
		if email.data.lower() != current_user.email:
			employee = Employee.query.filter_by(email=email.data.lower()).first()
			if employee:
				raise ValidationError('That email is taken. Please choose a different one.')


class AddEmpForm(FlaskForm):
	fname = StringField('First Name', validators=[DataRequired(), Length(max=50)], render_kw={'autofocus': 'true'})
	lname = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
	email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
	phone = StringField('Phone', validators=[DataRequired(), Length(max=15)])
	role = SelectField('Role', validators=[DataRequired()], choices = choices.get('role'))

	salary = FloatField('Salary')
	incentive = FloatField('Incentive')

	password = PasswordField('Password', validators=[DataRequired(), Length(max=50)])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(max=50), EqualTo('password', message='Password doesn\'t match.')])
	submit = SubmitField('Add')


	def validate_email(self, email):
		employee = Employee.query.filter_by(email=email.data.lower()).first()
		if employee:
			raise ValidationError('That email is taken. Please choose a different one.')

	def validate_phone(self, phone):
		employee = Employee.query.filter_by(phone=phone.data).first()
		if employee:
			raise ValidationError('That Phone is already registered.')
		if re.search('[a-zA-Z]', phone.data):
			raise ValidationError('Please enter a valid phone Number.')
		# if len(phone.data) != 11 or phone.data[:2] != '01':
			# raise ValidationError('Please enter a valid phone Number.')


# class AddItemForm(FlaskForm):
# 	fname = StringField('First Name', validators=[DataRequired(), Length(max=50)], render_kw={'autofocus': 'true'})
# 	lname = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
# 	email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
# 	phone = StringField('Phone', validators=[DataRequired(), Length(max=15)])
# 	role = SelectField('Role', validators=[DataRequired()], choices = choices.get('role'))

# 	password = PasswordField('Password', validators=[DataRequired(), Length(max=50)])
# 	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(max=50), EqualTo('password', message='Password doesn\'t match.')])
# 	submit = SubmitField('Add')




#--------------------------------------------------

class RequestResetForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)], render_kw={'autofocus': 'true'})
	submit = SubmitField('Request Password Reset')

	def validate_email(self, email):
		employee = Employee.query.filter_by(email=email.data.lower()).first()
		if employee is None:
			raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired(), Length(max=50)])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(max=50), EqualTo('password')])
	submit = SubmitField('Reset Password')
