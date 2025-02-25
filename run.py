from app import app, db
from scripts.seed_db import seed_database

if __name__ == "__main__":
    with app.app_context():
        seed_database()
        print("Base de données peuplée avec succès!") 