from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import logging

app = Flask(__name__)

# Configuration des logs
logging.basicConfig(level=logging.DEBUG)

# Configuration de la base de données
database_url = os.getenv('DATABASE_URL')
if database_url:
    # Assurez-vous que l'URL commence par postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # URL par défaut pour le développement local
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/kits_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key')

# Debug mode
app.debug = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models