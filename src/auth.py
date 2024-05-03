from flask import request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from models import User, db

def configure_jwt(app):
    jwt = JWTManager(app)

    @app.route('/signup', methods=['POST'])
    def signup():
        # Signup
        pass

    @app.route('/login', methods=['POST'])
    def login():
        # Login 
        pass
