# Inbuilt libs
import os

#External Libraries
from flask import Flask,request,url_for,render_template,session,logging,flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from passlib.hash import sha256_crypt
# Local Modules
from config import uri

#Instantiate App
app = Flask(__name__)

#db config
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#instantiate dbObject
db = SQLAlchemy(app)

#instantiate ma
ma = Marshmallow(app)

migrate = Migrate(app,db)
manager = Manager(app)

manager.add_command('db',MigrateCommand)

#Models
class User(db.Model):
	id = db.Column(db.Integer,primary_key=True,nullable=False)
	name = db.Column(db.String(100))
	email = db.Column(db.String(100))
	password = db.Column(db.String(100))
	cartItems = db.Column(db.Integer)

class Category(db.Model):
	"""docstring for ClassName"""
	id = db.Column(db.Integer,primary_key=True,nullable=False)
	categoryname = db.Column(db.String(255))
	item = db.relationship('Product',backref='type')
	maker = db.relationship('Producer',backref='produce_class')

class Product(db.Model):
	"""docstring for ClassName"""
	id = db.Column(db.Integer,primary_key=True,nullable=False)
	name = db.Column(db.String(200))
	description = db.Column(db.Text)
	type_id = db.Column(db.Integer,db.ForeignKey('category.id'))
	producer_id = db.Column(db.Integer,db.ForeignKey('producer.id'))

class Producer(db.Model):
	id = db.Column(db.Integer,primary_key=True,nullable=False)
	companyname = db.Column(db.String(200),unique=True)
	email = db.Column(db.String(100))
	phone = db.Column(db.String(100))
	#address = db.Column(db.Text,unique=True)
	item = db.relationship('Product',backref='manufacturer')
	category_id = db.Column(db.Integer,db.ForeignKey('category.id'))

## Endpoints #

@app.route('/create_user',methods=['GET','POST'])
def create_user():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		#cartItems = request.form['cartItems']
		password = sha256_crypt.hash(str(request.form['password']))

		newuser = User(name=name,email=email,password=password)
		db.session.add(newuser)
		db.session.commit()
		app.logger.info('SUCCESSFUL')
	else:
		app.logger.info('PLs sign up')
	return render_template('index.html')

	name = request.json['name']
	email = request.json['email']
	cartItems = request.json['cartItems']

	newuser = User(name=name, email=email, cartItems=cartItems)
	db.session.add(newuser)
	db.session.commit()
	return redirect(url_for('profile'))

@app.route('/user_profile') 
def showProfile():
	return render_template('profile.html')

@app.route('/create_producer',methods=['GET','POST'])
def create_producer():
	if request.method == "POST":
		name = request.json['name']
		email = request.json['email']
		phone = request.json['telephone']
		address = request.json['address']
		category = request.json['category']

		newproducer = Producer(name=name, email=email, phone=phone, item=item, category_id=category_id)
		db.session.add(newproducer)
		db.session.commit()
		return redirect(url_for('producer_profile'))

@app.route('/user_login',methods=['GET','POST'])
def user_login():
	if request.method == 'POST':
		email = request.form['email']
		user_password = str(request.form['password'])

		result = User.query.filter_by(email=email).first()
		password = result.password

		#compare passwords
		if sha256_crypt.verify(user_password,password):
			app.logger.info('Password Matched')
		else:
			app.logger.info('Password misMatched')

		
	return render_template('index.html')

@app.route('/user_profile')
def showProfile():
	return render_template('profile.html')

@app.route('/add_producer')
def add_producer():
	name = request.json['name']
	email = request.json['email']
	phone = request.json['telephone']
	address = request.json['address']
	category = request.json['category']

	return 'all good'

#run statement
if __name__ == '__main__':
	#manager.run()
	app.run(debug=True,port=5500)