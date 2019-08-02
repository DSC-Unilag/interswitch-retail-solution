# Inbuilt libs
import os

#External Libraries
from flask import Flask,request,url_for,render_template,session,logging,flash,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from passlib.hash import sha256_crypt
from functools import wraps
# Local Modules
from config import uri

#Instantiate App
app = Flask(__name__)

app.secret_key = os.urandom(24)

#Paystack keys
pub_key = "pk_test_82788a109685a5da5134bf4997f61ce4df7be4e6"
secret_key = "sk_test_a04a9d39d4578cf392c9df3162d3108d6301bf22"

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
	plan = db.Column(db.String(100))
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
	price = db.Column(db.Integer)
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


# Json Schema
class productSchema(ma.ModelSchema):
	class Meta():
		model = Product

class categorySchema(ma.ModelSchema):
	class Meta():
		model = Category

class userSchema(ma.ModelSchema):
	class Meta():
		model = User

class producerSchema(ma.ModelSchema):
	class Meta():
		model = Producer

# Init Schema Object
product_schema = productSchema(strict=True)
products_schema = productSchema(many=True,strict=True)

category_schema = productSchema(strict=True)
categories_schema = productSchema(many=True,strict=True)

user_schema = productSchema(strict=True)
users_schema = productSchema(many=True,strict=True)

producer_schema = productSchema(strict=True)
producers_schema = productSchema(many=True,strict=True)



## Endpoints #

# Check if user_logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorized please login','danger')
			return redirect(url_for('user_login'))

	return wrap

# Index
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/profile')
@is_logged_in
def profile():
	return render_template('profile.html')

# Create New User
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

# Create Producer
@app.route('/create_producer',methods=['GET','POST'])
def create_producer():
	if request.method == "POST":
		companyname = request.form['companyname']
		email = request.form['email']
		phone = request.form['phone']
		address = request.form['address']
		category = request.form['category']

		producer_class = Category.query.filter_by(categoryname=category).first()
		#app.logger.info(producer_class.categoryname)

		newproducer = Producer(companyname=companyname, email=email, phone=phone, address=address, produce_class=producer_class)
		db.session.add(newproducer)
		db.session.commit()

		# create session
		'''session['logged_in'] = True
		session['name'] = name

		flash(f'Welcome to your dashboard {session.name}','success')

		return redirect(url_for('producer_profile'))'''
	return render_template('ProducerSignup.html')

# User Login
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
			session['email'] = result.email

			flash('You are now logged in','success')
			return redirect(url_for('index'))
		else:
			flash('wrong password','error')
			return render_template('userSignUp.html')
			#app.logger.info('Password misMatched')
		
	return render_template('userSignUp.html')

# Logout
@app.route('/logout')
def logout():
	session.clear()
	flash('You are now logged out','success')

	return redirect(url_for('user_login'))

# Display Products
@app.route('/api/show_products',methods=['GET','POST'])
def show_products():
	products = Product.query.all()
	product_class = Category.query.all()

	presult = users_schema.dump(products)
	cresult = categories_schema.dump(product_class)

	return jsonify(presult.data)

# Checkout
@app.route('/checkout')
@is_logged_in
def checkout():
	curent_user = 'emma'
	email = 'emma@gmail.com'
    return render_template('checkout.html', email=email, pub-key=)

#run statement
if __name__ == '__main__':
	manager.run()
	#app.run(debug=True,port=5500)