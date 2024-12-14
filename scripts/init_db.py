from backend.app import create_app
from backend.db.models import db

def init_database():
    """Initialize the database and create all tables"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()
