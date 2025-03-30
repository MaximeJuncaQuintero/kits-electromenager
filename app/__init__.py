from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import logging

app = Flask(__name__)

# Configuration de la base de données
database_url = os.getenv('DATABASE_URL', 'postgresql://mjunca@localhost/kits_db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key')

# Debug mode
app.debug = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models