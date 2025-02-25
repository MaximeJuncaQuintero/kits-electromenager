from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration de la base de données
if os.environ.get('DATABASE_URL'):
    # Configuration pour Render
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    # Configuration locale
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/kits_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY', 'dev')

db = SQLAlchemy(app)

from app import routes, models 