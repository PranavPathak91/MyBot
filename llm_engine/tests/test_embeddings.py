import sys
import os
import logging
from dotenv import load_dotenv
import numpy as np
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import default user ID from backend config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backend')))
from config import DEFAULT_USER_ID
from db.mongo_connection import init_db, get_db

from embeddings.vector_store import VectorStore
from embeddings.retriever import RAGRetriever
from embeddings.pinecone_client import PineconeEmbeddingManager

def test_vector_store():
    print("Testing Vector Store...")
    
    # Initialize embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Sample documents
    documents = [
        {"text": "Machine learning is fascinating", "source": "AI book", "user_id": DEFAULT_USER_ID},
        {"text": "Python is a great programming language", "source": "Coding manual", "user_id": DEFAULT_USER_ID},
        {"text": "Neural networks simulate brain function", "source": "Neuroscience journal", "user_id": DEFAULT_USER_ID}
    ]
    
    # Generate embeddings
    embeddings = model.encode([doc['text'] for doc in documents])
    
    # Create vector store
    vector_store = VectorStore(dimension=embeddings.shape[1])
    
    # Add documents
    vector_store.add_documents(documents, embeddings)
    
    # Test search
    query = "programming language"
    query_embedding = model.encode(query)
    
    results = vector_store.search(query_embedding, k=2)
    
    print("Search Results:")
    for result in results:
        print(f"Text: {result['text']}, Score: {result['score']}")

def test_rag_retriever():
    print("\nTesting RAG Retriever...")
    
    # Initialize embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Initialize MongoDB client using backend connection
    mongo_client = MongoClient(os.getenv('MONGO_URI'))
    
    # Initialize Pinecone client
    pinecone_client = PineconeEmbeddingManager(
        api_key=os.getenv('PINECONE_API_KEY'), 
        index_name=os.getenv('PINECONE_INDEX_NAME', 'test-index')
    )
    
    # Create RAG retriever
    retriever = RAGRetriever(
        mongodb_client=mongo_client, 
        pinecone_client=pinecone_client, 
        embedding_model=model,
        database_name=os.getenv('DATABASE_NAME'),
        collection_name='documents'
    )
    
    # Add some test logic if needed
    print("RAG Retriever initialized successfully")

def test_pinecone_embeddings():
    """
    Test Pinecone embedding functionality
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize Pinecone Embedding Manager
        pinecone_manager = PineconeEmbeddingManager(
            api_key=os.getenv('PINECONE_API_KEY'), 
            index_name=os.getenv('PINECONE_INDEX_NAME', 'test-index')
        )
        
        # Sample texts for embedding
        texts = [
            "Machine learning is fascinating",
            "Python is a great programming language",
            "Neural networks simulate brain function"
        ]
        
        # Test embedding generation
        logger.info("Testing embedding generation...")
        embeddings = pinecone_manager.generate_embeddings(texts)
        assert len(embeddings) == len(texts), "Embedding generation failed"
        logger.info(f"Successfully generated {len(embeddings)} embeddings")
        
        # Test upserting embeddings
        logger.info("Testing embedding upsert...")
        pinecone_manager.upsert_embeddings(
            texts,
            metadata=[{'source': 'test', 'user_id': DEFAULT_USER_ID} for _ in texts]
        )
        logger.info("Successfully upserted embeddings")
        
        # Test querying embeddings
        logger.info("Testing embedding query...")
        query_text = "programming language"
        query_embedding = pinecone_manager.generate_embeddings([query_text])[0]
        results = pinecone_manager.index.query(
            vector=query_embedding, 
            top_k=3, 
            include_metadata=True,
            filter={
                "user_id": {"$eq": DEFAULT_USER_ID}
            }
        )
        
        logger.info("Successfully queried embeddings")
        print("Query Results:")
        for match in results['matches']:
            print(f"Score: {match['score']}, Metadata: {match.get('metadata', {})}")
        
    except Exception as e:
        logger.error(f"Pinecone embedding test failed: {e}")
        raise

def main():
    test_vector_store()
    test_rag_retriever()
    test_pinecone_embeddings()

if __name__ == "__main__":
    main()
