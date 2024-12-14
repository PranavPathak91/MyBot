from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load MongoDB URI and database name from environment variables
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

if not MONGO_URI or not DATABASE_NAME:
    raise ValueError("MONGO_URI and DATABASE_NAME must be set in environment variables")

# Initialize MongoDB client
client = None
db = None

def init_db(app):
    """
    Initialize the MongoDB connection.
    """
    global client, db
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    return db

def get_db():
    """
    Return the MongoDB database instance.
    """
    global db
    if db is None:
        raise RuntimeError("Database not initialized. Call init_db first.")
    return db
