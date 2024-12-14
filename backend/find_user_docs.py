import sys
sys.path.append('.')

from config import DEFAULT_USER_ID
from pymongo import MongoClient
import json
import os
from dotenv import load_dotenv
from bson import ObjectId

# Custom JSON encoder to handle ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

# Load environment variables
load_dotenv()

# Get MongoDB URI from environment
mongo_uri = os.getenv('MONGO_URI')
database_name = os.getenv('DATABASE_NAME', 'document_database')

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]

# Find documents for the default user
documents = list(db.documents.find({'user_id': DEFAULT_USER_ID}))

# Print the documents
print(f'Found {len(documents)} documents for user {DEFAULT_USER_ID}:')
print(json.dumps(documents, indent=2, cls=JSONEncoder))
