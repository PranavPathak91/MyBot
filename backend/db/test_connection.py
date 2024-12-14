from backend.db.mongo_connection import get_db, init_db
import datetime
import pytest
from flask import Flask

def test_connection():
    try:
        # Create a test app to initialize database
        test_app = Flask(__name__)
        test_app.config['TESTING'] = True
        
        # Initialize database
        db = init_db(test_app)
        
        collections = db.list_collection_names()
        print(f"Connected to MongoDB! Collections: {collections}")
    except Exception as e:
        pytest.fail(f"Failed to connect to MongoDB: {e}")

def test_mongodb_connection():
    try:
        # Create a test app to initialize database
        test_app = Flask(__name__)
        test_app.config['TESTING'] = True
        
        # Initialize database
        db = init_db(test_app)
        
        # Create a test document
        test_doc = {
            "test_id": "connection_test",
            "timestamp": datetime.datetime.utcnow(),
            "status": "success"
        }
        
        # Insert the test document
        result = db.test_collection.insert_one(test_doc)
        assert result.inserted_id is not None, "Failed to insert test document"
        
        # Retrieve the document
        retrieved_doc = db.test_collection.find_one({"test_id": "connection_test"})
        assert retrieved_doc is not None, "Failed to retrieve test document"
        
        # Clean up - delete the test document
        delete_result = db.test_collection.delete_one({"test_id": "connection_test"})
        assert delete_result.deleted_count == 1, "Failed to delete test document"
        
    except Exception as e:
        pytest.fail(f"Error testing MongoDB connection: {str(e)}")

if __name__ == "__main__":
    test_connection()
    test_mongodb_connection()
    print("MongoDB connection test completed successfully!")
