#import the package Flask
from flask import Flask

#import the settings class from config.py
from config import Config

#create an app variable to store the __name__ passed from the Flask class
app = Flask(__name__)

#load the settings into the app
app.config.from_object(Config)

#import routes modules from the app package
from app import routes
