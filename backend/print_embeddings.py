import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from llm_engine.embeddings.pinecone_client import PineconeEmbeddingManager
from llm_engine.embeddings.retriever import RAGRetriever

# Initialize MongoDB
mongo_client = MongoClient('mongodb+srv://pranavgenaiexperiments:jrvAYPrzVyOjfMlM@cluster0.tibcj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = mongo_client['document_database']
documents_collection = db['documents']

# Initialize Pinecone
pinecone_client = PineconeEmbeddingManager(
    api_key='pcsk_YZany_6dVP28ckbLDTJCsxfCouwaLcd4esofdWdK3jAe9fydzitR49X31BnLynHU6AT1z'
)

# Initialize embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize RAG Retriever
rag_retriever = RAGRetriever(
    mongodb_client=mongo_client,
    pinecone_client=pinecone_client,
    embedding_model=embedding_model
)

# Sync documents for the user
user_id = 'default_user_123'

# Fetch documents directly from MongoDB
documents = list(documents_collection.find({'user_id': user_id}))

print(f"Total Documents for user {user_id}: {len(documents)}")
for i, doc in enumerate(documents, 1):
    print(f"\nDocument {i}:")
    print("Document ID:", doc.get('_id', 'Unknown'))
    print("Name:", doc.get('name', 'No Name'))
    print("Folder:", doc.get('folder', 'No Folder'))
    print("Summary:", doc.get('summary', 'No Summary'))
    print("Hashtags:", doc.get('hashtags', []))
    print("Uploaded At:", doc.get('uploaded_at', 'Unknown Date'))

# Optional: Sync and retrieve using RAG retriever
print("\n--- RAG Retriever Sync Debug ---")
try:
    # Modify documents to include summary as text
    modified_documents = []
    for doc in documents:
        modified_doc = doc.copy()
        modified_doc['text'] = doc.get('summary', doc.get('name', ''))
        modified_documents.append(modified_doc)
    
    # Manually set documents in the retriever's local store
    local_store = rag_retriever._get_or_create_local_store(user_id)
    
    # Generate embeddings for the documents
    texts = [doc.get('text', '') for doc in modified_documents]
    embeddings = embedding_model.encode(texts)
    
    # Add documents to local store
    local_store.clear()
    local_store.add_documents(modified_documents, embeddings)
    
    # Upsert to Pinecone
    namespace = f"user_{user_id}"
    pinecone_client.upsert_embeddings(
        texts=texts,
        embeddings=embeddings,
        ids=[str(doc['_id']) for doc in modified_documents],
        namespace=namespace,
        metadata=[
            {
                'user_id': user_id,
                'name': doc.get('name', ''),
                'folder': doc.get('folder', ''),
                'hashtags': doc.get('hashtags', [])
            } for doc in modified_documents
        ]
    )
    
    print("Successfully synced documents to local and Pinecone stores.")
    
except Exception as e:
    print(f"Sync failed: {e}")
    import traceback
    traceback.print_exc()
