from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Utiliser DATABASE_URL pour Render ou l'URL locale par défaut
database_url = os.getenv('DATABASE_URL', 'postgresql://localhost/kits_db')

# Correction du préfixe postgres:// vers postgresql:// pour Render
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
db = SQLAlchemy(app)

from app import routes, models 