import os
from datetime import timedelta
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(PROJECT_PATH, "uploads"), exist_ok=True)

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "specialcare@123"
    JWT_SECRET_KEY = "specialcare@123"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    UPLOAD_FOLDER = os.path.join(PROJECT_PATH, "uploads")

    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = False
    
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False
    

