import os

class Config:
    SECRET_KEY = "mine_secretsystem_key"
    JWT_SECRET_KEY = "mine_malik_jwt_secret_key"  
    JWT_ALGORITHM = "HS256"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:malik0112@localhost:5000/student_db"
    JWT_TOKEN_LOCATION = ["cookies"]  
    JWT_COOKIE_SECURE = False 
    JWT_COOKIE_HTTPONLY = True  
    JWT_COOKIE_CSRF_PROTECT = False  
