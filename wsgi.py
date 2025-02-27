from app import app, db
from flask_migrate import upgrade
from scripts.seed_db import seed_database

def initialize_database():
    try:
        # Run migrations
        with app.app_context():
            upgrade()
            
            # Check if we need to seed the database
            # We'll check if there are any products in the database
            from app.models import Produit
            if Produit.query.count() == 0:
                print("No products found. Seeding database...")
                seed_database()
            print("Database initialization completed!")
    except Exception as e:
        print(f"Error during database initialization: {e}")

# Initialize database on startup
initialize_database()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
else:
    # For Render
    application = app