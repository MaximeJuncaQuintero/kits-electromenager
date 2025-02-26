from app import db

def init_db():
    db.create_all()
    print("Base de données initialisée !")

if __name__ == "__main__":
    init_db() 