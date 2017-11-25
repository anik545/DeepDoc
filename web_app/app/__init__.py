from flask import Flask

# Create app and initialize flask
app = Flask(__name__)

#load configuration options from config.py
app.config.from_object('config')

from app import views