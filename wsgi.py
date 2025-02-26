from app import app, db
from scripts.seed_db import seed_database

# Initialisation de la base de données au démarrage
with app.app_context():
    db.create_all()
    seed_database()
    print("Base de données initialisée !")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
else:
    # Pour Render
    application = app