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
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

class Cart(db.Model):
	id = db.Column(db.Integer,primary_key=True,nullable=False)
	productID = db.Column(db.Integer,db.ForeignKey('product.id'))
	userID = db.Column(db.Integer,db.ForeignKey('user.id'))


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
@app.route('/user_signup')
def user_signup():
	return render_template('login.html')

@app.route('/create_user',methods=['GET','POST'])
def create_user():
	name = request.form['name']
	email = request.form['email']
	password = sha256_crypt.hash(str(request.form['password']))

	newuser = User(name=name,email=email,password=password)
	db.session.add(newuser)
	db.session.commit()
	flash('Welcome new user','success')
	return redirect(url_for('show_products'))

# Create Producer
@app.route('/producer_signup')
def producer_signup():
	return render_template('login.html')

@app.route('/create_producer',methods=['GET','POST'])
def create_producer():
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
	return redirect(url_for('show_products'))

@app.route('/add_product',methods=['GET','POST'])
def add_product():
	if request.method == 'POST':
		name = request.form['name']
		description = request.form['description']
		price = request.form['price']
		category = request.form['category']

		type_class = Category.query.filter_by(categoryname=category).first()

		newproduct = Product(name=name,description=description,price=price,type=type_class)

		db.session.add(newproduct)
		db.session.commit()

	return render_template('dummy_data.html')

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
			return redirect(url_for('show_products'))
		else:
			flash('wrong password','error')
			return render_template('login.html')
			app.logger.info('Password misMatched')
		
	return render_template('login.html')

@app.route('/product_info')
def product_info():
	return render_template('product_info.html')

# Logout
@app.route('/logout')
def logout():
	session.clear()
	flash('You are now logged out','success')

	return redirect(url_for('user_login'))

# Display Products
@app.route('/show_products',methods=['GET','POST'])
def show_products():
	all_products = Product.query.all()

	return render_template('showcase.html',all_products=all_products)

# Add to cart
@app.route('/add_toCart')
#@is_logged_in
def add_toCart():
	#productId = int(request.args.get('productId'))
	productsoncart = Product.query.all()
	'''print(productsoncart)
	#product = Product.query.filter_by(id = productId)
	userID = User.query.filter_by(email=session['email'])

	session['productsoncart'] = productsoncart

	total_price = 0
	for product in productsoncart:
		total_price += product.price

	session['total_price'] = total_price'''

	return productsoncart #redirect(url_for('Products'))

@app.route('/producer_dash')
def producer_dash():
	return render_template('sw.html')

@app.route('/cart')
def cart():
	oncart = Product.query.all()
	total_price = 0
	for product in oncart:
		total_price += product.price

	return render_template('sw2.html',oncart=oncart,total_price=total_price)

@is_logged_in
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
	email = session.get('email')
	current_user = User.query.filter_by(email=email)
	email = current_user.email

	return render_template('checkout.html', email=email, pub_key=pub_key)





#run statement
if __name__ == '__main__':
	#manager.run()
	app.run(debug=True,port=5500)