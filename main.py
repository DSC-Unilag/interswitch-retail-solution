# Inbuilt libs
import os

#External Libraries
from flask import Flask,request,url_for,render_template,session,logging,flash,redirect
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
	address = db.Column(db.String(225),unique=True)
	item = db.relationship('Product',backref='manufacturer')
	category_id = db.Column(db.Integer,db.ForeignKey('category.id'))

## Endpoints #
@app.route('/create_user',methods=['GET','POST'])
def create_user():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		password = sha256_crypt.hash(str(request.form['password']))

		newuser = User(name=name,email=email,password=password)
		db.session.add(newuser)
		db.session.commit()
		flash('Welcome new user','success')
		return redirect(url_for('user_profile'))
	else:
		app.logger.info('PLs sign up')

	return render_template('userSignUp.html')



@app.route('/create_producer',methods=['GET','POST'])
def create_producer():
	if request.method == "POST":
		name = request.form['companyname']
		email = request.form['email']
		phone = request.form['phone']
		address = request.form['address']
		category = request.form['category']

		newproducer = Producer(name=name, email=email, phone=phone, category=category)
		db.session.add(newproducer)
		db.session.commit()

		# create session
		'''session['logged_in'] = True
		session['name'] = name

		flash(f'Welcome to your dashboard {session.name}','success')

		return redirect(url_for('producer_profile'))'''
	return render_template('ProducerSignup.html')

@app.route('/user_login',methods=['GET','POST'])
def user_login():
	if request.method == 'POST':
		email = request.form['email']
		user_password = str(request.form['password'])

		result = User.query.filter_by(email=email).first()
		password = result.password

		#compare passwords
		if sha256_crypt.verify(user_password,password):

			# create user session 
			session['logged_in'] = True
			session['name'] = result.name

			flash('You are now logged in','success')
			return redirect(url_for('dashboard'))
		else:
			flash('wrong password','error')
			return render_template('userSignUp.html')
			#app.logger.info('Password misMatched')

		
	return render_template('userSignUp.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
	

#run statement
if __name__ == '__main__':
	#manager.run()
	app.run(debug=True,port=5500)