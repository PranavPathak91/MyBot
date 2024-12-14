import sys
import os

# Ensure project root is in Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Load environment variables with explicit path
from dotenv import load_dotenv
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path)

# Verify environment variables
def print_env_vars():
    print("\nEnvironment Variables:")
    for key in ['PINECONE_API_KEY', 'PINECONE_INDEX_NAME', 'MONGO_URI', 'DATABASE_NAME']:
        print(f"{key}: {os.getenv(key, 'NOT SET')}")

print_env_vars()

# Imports
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

# Import from your project
from backend.config import DEFAULT_USER_ID
from llm_engine.embeddings.pinecone_client import PineconeEmbeddingManager
from llm_engine.embeddings.retriever import RAGRetriever
from llm_engine.embeddings.vector_store import VectorStore

# Pinecone configuration
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is not set in the environment variables")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = os.getenv('PINECONE_INDEX_NAME', 'test-index')
index = pc.Index(index_name)

# Initialize MongoDB
mongo_client = MongoClient(os.getenv('MONGO_URI'))
database_name = os.getenv('DATABASE_NAME', 'document_database')
db = mongo_client[database_name]

# Initialize embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize Pinecone client
pinecone_client = PineconeEmbeddingManager(
    api_key=PINECONE_API_KEY, 
    index_name=index_name
)

# Create RAG Retriever
retriever = RAGRetriever(
    mongodb_client=mongo_client,
    pinecone_client=pinecone_client,
    embedding_model=embedding_model,
    database_name=database_name
)

# Sync documents for default user
retriever.sync_user_documents(DEFAULT_USER_ID)

# Verify local vector store
local_store = retriever._get_or_create_local_store(DEFAULT_USER_ID)
print(f"\nDocuments in local vector store: {local_store.get_document_count()}")

# List documents in local vector store
documents = local_store.get_documents_by_user(DEFAULT_USER_ID)
print("\nLocal Vector Store Documents:")
for doc in documents:
    print(f"- {doc.get('name', 'Unnamed Document')}")
