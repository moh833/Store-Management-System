from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from store import db, login_manager, app, admin
from flask_login import UserMixin, current_user
from flask import session
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose

from flask import url_for, flash, redirect, Markup



@login_manager.user_loader
def load_user(emp_id):
	return Employee.query.get(int(emp_id))


def choices_from_file(name, file):
	with open('choices_files/' + file, encoding="utf-8") as f:
		data = f.readlines()
	data = [x.strip() for x in data]
	data = [(x, x) for x in data]
	return [('', name)] + data



class BoughtItem(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	time = db.Column(db.DateTime, nullable=False)
	buying_price = db.Column(db.Float, nullable=False)
	bought_quantity = db.Column(db.Integer, nullable=False)
	# current_quantity = db.Column(db.Integer, nullable=False)
	# place = db.Column(db.String(50), nullable=False)

	item_id = db.Column(db.Integer, db.ForeignKey('main_item.id'))

# editable
class Main_item(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	company = db.Column(db.String(100), nullable=False)
	country = db.Column(db.String(100), nullable=False)
	distributer = db.Column(db.String(100), nullable=False)
	family = db.Column(db.String(100), nullable=False)
	# buying_price = db.Column(db.Float, nullable=False)
	selling_price = db.Column(db.Float, nullable=False)
	# total_quantity = db.Column(db.Integer, nullable=False)
	current_quantity = db.Column(db.Integer, nullable=False)

	risk_quantity = db.Column(db.Integer, nullable=False)
	ran_out = db.Column(db.Boolean, default=False)

	place = db.Column(db.String(50), nullable=False)

	bought_items = db.relationship('BoughtItem', backref='item', lazy=True)
	sold_items = db.relationship('SoldItem', backref='item', lazy=True)

	def __repr__(self):
		return f"{self.name}"

class SoldItem(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	time = db.Column(db.DateTime, nullable=False)
	paid_price = db.Column(db.Float, nullable=False)
	sold_quantity = db.Column(db.Integer, nullable=False)
	customer = db.Column(db.String(100))
	sale = db.Column(db.Float, nullable=False, default=0.0)
	debt = db.Column(db.Float, nullable=False)

	item_id = db.Column(db.Integer, db.ForeignKey('main_item.id'))


class Expenses(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	paid_price = db.Column(db.Float, nullable=False)
	time = db.Column(db.DateTime, nullable=False)
	


class Employee(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	fname = db.Column(db.String(30), nullable=False)
	lname = db.Column(db.String(30), nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	phone = db.Column(db.String(30), unique=True, nullable=False)
	role = db.Column(db.String(30), nullable=False)

	salary = db.Column(db.Float)
	incentive = db.Column(db.Float)

	password = db.Column(db.String(60), nullable=False)


	def get_reset_token(self, expires_sec=1800):
		s = Serializer(app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'emp_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			emp_id = s.loads(token)['emp_id']
		except:
			return None
		return Employee.query.get(emp_id)


	def __repr__(self):
		return f"{self.fname} {self.lname}"






class BoughtItemView(ModelView):
	can_view_details = True
	can_edit = False
	can_delete = False
	can_create = False
	column_list = ['time', 'buying_price', 'bought_quantity', 'item']
	column_searchable_list = ['time', 'buying_price', 'bought_quantity']
	column_labels = dict(time='Time', buying_price='Unit Buying Price', bought_quantity='Quantity', item='Item')
	can_export = True


	def is_accessible(self):
		if current_user.is_authenticated and session['ROLE'] in ['admin']:
			return True

	def inaccessible_callback(self, name, **kwargs):
		flash('You don\'t have permission to access this page!', 'danger')
		return redirect(url_for('home'))

class Main_itemView(ModelView):

	def _user_formatter(view, context, model, name):
		if model.id:
			markupstring = "<a href='/%s/item_info'>%s</a>" % (model.id, model.name)
			return Markup(markupstring)
		else:
			return ""

	column_formatters = {
        'name': _user_formatter
    }


	can_view_details = True
	can_edit = False
	can_delete = False
	can_create = False
	column_list = ['id', 'name', 'company', 'country', 'distributer'
	, 'family', 'place', 'selling_price', 'current_quantity', 'ran_out']
	column_searchable_list = ['id', 'name', 'company', 'country', 'distributer'
	, 'family', 'place', 'ran_out']
	column_labels = dict(id='ID', name='Item', 
	company='Company', country='Country', distributer='Distributer', family='Family', place='Place', ran_out='Reached Risk')
	can_export = True
	form_choices = {
		'name': choices_from_file('name', 'name.txt'),
		'company': choices_from_file('company', 'company.txt'),
		'country': choices_from_file('country', 'country.txt'),
		'distributer': choices_from_file('distributer', 'distributer.txt'),
		'family': choices_from_file('family', 'family.txt'),
		'place': choices_from_file('place', 'place.txt')
	}

	def is_accessible(self):
		if current_user.is_authenticated:
			return True

	def inaccessible_callback(self, name, **kwargs):
		flash('You don\'t have permission to access this page!', 'danger')
		return redirect(url_for('home'))

class SoldItemView(ModelView):
	can_view_details = True
	can_edit = False
	can_delete = False
	can_create = False
	column_list = ['time', 'paid_price', 'sold_quantity', 'customer', 'sale', 'debt', 'item']
	column_searchable_list = ['time', 'customer', 'debt', 'item_id']
	column_labels = dict(time='Time', paid_price='Total Sold Price', sold_quantity='Quantity', customer='Customer', 
	sale='Sale', debt='Debt', item='Item')
	can_export = True

	def is_accessible(self):
		if current_user.is_authenticated and session['ROLE'] in ['admin']:
			return True

	def inaccessible_callback(self, name, **kwargs):
		flash('You don\'t have permission to access this page!', 'danger')
		return redirect(url_for('home'))


class ExpensesView(ModelView):
	can_view_details = True
	can_edit = False
	can_delete = False
	can_create = False
	column_list = ['name', 'time', 'paid_price']
	column_labels = dict(name='Type', time='Time', paid_price='Fees')
	column_searchable_list = ['name', 'time', 'paid_price']
	can_export = True

	def is_accessible(self):
		if current_user.is_authenticated and session['ROLE'] in ['admin']:
			return True

	def inaccessible_callback(self, name, **kwargs):
		flash('You don\'t have permission to access this page!', 'danger')
		return redirect(url_for('home'))


class EmployeeView(ModelView):

	can_view_details = True
	can_edit = False
	can_delete = False
	can_create = False
	column_details_exclude_list = ['password']
	page_size = 30
	# create_modal = True
	# edit_modal = True
	# form_excluded_columns = ['email']
	column_searchable_list = ['fname', 'lname', 'email', 'phone', 'role']
	can_export = True
	form_excluded_columns = ['password']
	column_labels = dict(fname='First Name', lname='Last Name', 
	email='Email', phone='Phone Number', salary='Salary', incentive='Incentive', role='Role')

	column_list = ['fname', 'lname', 'email', 'phone', 'salary', 'incentive', 'role']
	# column_editable_list = ['salary', 'incentive']

	# form_edit_rules = ('email', 'fname', 'lname')


	def is_accessible(self):
		if current_user.is_authenticated and session['ROLE'] in ['admin']:
			return True

	def inaccessible_callback(self, name, **kwargs):
		flash('You don\'t have permission to access this page!', 'danger')
		return redirect(url_for('home'))




admin.add_view(Main_itemView(Main_item, db.session, 'Items'))
admin.add_view(SoldItemView(SoldItem, db.session, 'Sold Items'))
admin.add_view(BoughtItemView(BoughtItem, db.session, 'Bought Items'))
admin.add_view(ExpensesView(Expenses, db.session, 'Expenses'))
admin.add_view(EmployeeView(Employee, db.session, 'Employees'))

