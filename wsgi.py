from app import app, db

# Initialisation de la base de données au démarrage
with app.app_context():
    db.create_all()
    print("Base de données initialisée !")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
else:
    # Pour Render
    application = app