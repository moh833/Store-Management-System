from store import db

from store.models import Main_item, BoughtItem, SoldItem, Expenses, Employee

db.create_all()

from store import bcrypt

hp = bcrypt.generate_password_hash('admin').decode('utf-8')

admin = Employee(fname='super', lname='admin', email='admin@gmail.com', phone='01615487926', password=hp, role='admin')

db.session.add(admin)

db.session.commit()
