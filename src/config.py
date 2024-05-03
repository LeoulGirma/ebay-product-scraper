import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ebay.db'
    SECRET_KEY = 'your-secret-key'
    JWT_SECRET_KEY = 'jwt-secret-string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
