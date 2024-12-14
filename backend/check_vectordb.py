import os
import sys
import traceback
sys.path.append('.')

from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Print environment variables for debugging
print("PINECONE_API_KEY:", os.getenv('PINECONE_API_KEY'))
print("PINECONE_ENVIRONMENT:", os.getenv('PINECONE_ENVIRONMENT'))
print("PINECONE_INDEX_NAME:", os.getenv('PINECONE_INDEX_NAME'))

from pinecone import Pinecone

try:
    # Initialize Pinecone
    pc = Pinecone(
        api_key=os.getenv('PINECONE_API_KEY')
    )

    # Get the index name
    index_name = os.getenv('PINECONE_INDEX_NAME', 'test-index')

    # Connect to the index
    index = pc.Index(index_name)

    # Import default user ID
    from config import DEFAULT_USER_ID

    # Query the vector database for the default user
    query_results = index.query(
        vector=[0.1] * 384,  # Placeholder vector, replace with actual query vector if needed
        top_k=10,
        include_metadata=True,
        filter={
            "user_id": {"$eq": DEFAULT_USER_ID}
        }
    )
    
    print(f"Found {len(query_results['matches'])} vector documents for user {DEFAULT_USER_ID}:")
    for match in query_results['matches']:
        print("\nVector Document:")
        print(f"ID: {match['id']}")
        print(f"Score: {match['score']}")
        print("Metadata:")
        for key, value in match.get('metadata', {}).items():
            print(f"  {key}: {value}")
    
except Exception as e:
    print("Full error traceback:")
    traceback.print_exc()
