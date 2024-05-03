from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ebay.db'
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)  # For demo purposes; in production, use hashed passwords

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    price = db.Column(db.String(80))
    shipping = db.Column(db.String(80))
    image_url = db.Column(db.String(255))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/signup', methods=['POST'])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')  # In production, ensure the password is hashed
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 409
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Bad username or password'}), 401

@app.route('/listings', methods=['POST'])
@jwt_required()
def listings():
    url = request.json.get('url')
    max_listings = request.json.get('max_listings', None)
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'message': 'Failed to retrieve data from eBay'}), 400
    soup = BeautifulSoup(response.text, 'html.parser')
    listings = soup.find_all('li', class_='s-item')
    listing_count = max_listings if max_listings is not None else len(listings)
    results = []
    for index, item in enumerate(listings[:listing_count]):
        title = item.find('h3', class_='s-item__title').text if item.find('h3', class_='s-item__title') else 'No title found'
        price = item.find('span', class_='s-item__price').text if item.find('span', class_='s-item__price') else 'No price found'
        shipping = item.find('span', class_='s-item__shipping').text if item.find('span', class_='s-item__shipping') else 'No shipping info'
        image_url = item.find('img')['src'] if item.find('img') else 'No image URL'
        product = Product(title=title, price=price, shipping=shipping, image_url=image_url)
        db.session.add(product)
        db.session.commit()
