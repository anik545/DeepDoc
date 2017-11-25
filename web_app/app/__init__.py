from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


from flask_mail import Mail

# Create app and initialize flask
app = Flask(__name__)

#load configuration options from config.py
app.config.from_object('config')

from app import views