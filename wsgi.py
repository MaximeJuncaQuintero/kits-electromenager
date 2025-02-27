from app import app, db
from flask_migrate import upgrade
from scripts.seed_db import seed_database
import os
from sqlalchemy import text

def initialize_database():
    try:
        # Only run this cleanup on Render (when DATABASE_URL is set)
        if os.getenv('DATABASE_URL'):
            with app.app_context():
                # Drop alembic_version table to clean migration history
                with db.engine.connect() as connection:
                    connection.execute(text('DROP TABLE IF EXISTS alembic_version'))
                    connection.commit()
                
                # Create all tables directly
                db.create_all()
                
                # Check if we need to seed the database
                from app.models import Produit
                if Produit.query.count() == 0:
                    print("No products found. Seeding database...")
                    seed_database()
                print("Database initialization completed!")
        else:
            # Local development - don't modify anything
            print("Running in local development mode")
            
    except Exception as e:
        print(f"Error during database initialization: {e}")

# Initialize database on startup
initialize_database()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
else:
    # For Render
    application = app