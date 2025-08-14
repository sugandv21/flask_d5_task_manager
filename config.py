import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "sugan21"
    MYSQL_HOST = "localhost"      
    MYSQL_DB = "task_db"

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "supersecretkey"

