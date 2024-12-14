from typing import List, Dict, Any, Optional
import numpy as np
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from .pinecone_client import PineconeEmbeddingManager
from .vector_store import VectorStore
import logging
import threading
import time
import uuid

class RAGRetriever:
    def __init__(
        self, 
        mongodb_client: MongoClient,
        pinecone_client: PineconeEmbeddingManager,
        embedding_model: SentenceTransformer,
        database_name: str = 'user_documents',
        collection_name: str = 'documents',
        sync_interval: int = 3600  # 1 hour
    ):
        """
        Manage document retrieval across multiple vector stores
        
        :param mongodb_client: Initialized MongoDB client
        :param pinecone_client: Initialized Pinecone embedding manager
        :param embedding_model: Sentence transformer for generating embeddings
        :param database_name: MongoDB database name
        :param collection_name: MongoDB collection name
        :param sync_interval: Time between synchronization attempts
        """
        # Database connections
        self.mongo_client = mongodb_client
        self.db = self.mongo_client[database_name]
        self.documents_collection = self.db[collection_name]
        
        # Vector database clients
        self.pinecone_client = pinecone_client
        self.embedding_model = embedding_model
        
        # Local vector stores
        self.user_vector_stores: Dict[str, VectorStore] = {}
        
        # Synchronization tracking
        self.user_last_sync: Dict[str, float] = {}
        self.sync_interval = sync_interval
        
        # Logging
        self.logger = logging.getLogger(__name__)
        
        # Synchronization control
        self._stop_sync = threading.Event()
        self._sync_thread = None

    def _get_or_create_local_store(self, user_id: str) -> VectorStore:
        """
        Get or create a local vector store for a user
        
        :param user_id: Unique identifier for the user
        :return: User-specific VectorStore
        """
        if user_id not in self.user_vector_stores:
            dimension = self.embedding_model.get_sentence_embedding_dimension()
            self.user_vector_stores[user_id] = VectorStore(dimension=dimension)
        
        return self.user_vector_stores[user_id]

    def add_document(self, user_id: str, document: Dict[str, Any]) -> str:
        """
        Add a new document to MongoDB and vector stores
        
        :param user_id: Unique identifier for the user
        :param document: Document to be added
        :return: MongoDB document ID
        """
        # Validate and prepare document
        if not user_id:
            raise ValueError("User ID is required")
        
        # Ensure user_id is in the document
        document['user_id'] = user_id
        document['_id'] = str(uuid.uuid4())  # Ensure unique ID
        
        # Insert into MongoDB
        self.documents_collection.insert_one(document)
        
        # Generate embedding
        text = document.get('text', '')
        embedding = self.embedding_model.encode(text)
        
        # Update local vector store
        local_store = self._get_or_create_local_store(user_id)
        local_store.add_documents([document], embedding.reshape(1, -1))
        
        # Upsert to Pinecone
        namespace = f"user_{user_id}"
        self.pinecone_client.upsert_embeddings(
            texts=[text],
            embeddings=[embedding],
            ids=[document['_id']],
            namespace=namespace,
            metadata=[{
                'user_id': user_id,
                'title': document.get('title', ''),
                'source': document.get('source', '')
            }]
        )
        
        return document['_id']

    def retrieve_documents(
        self, 
        user_id: str, 
        query: str, 
        k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve documents for a user
        
        :param user_id: Unique identifier for the user
        :param query: Search query
        :param k: Number of documents to retrieve
        :return: List of most relevant documents
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query)
        
        # Retrieve from local vector store
        local_store = self._get_or_create_local_store(user_id)
        local_results = local_store.search(query_embedding, k=k)
        
        # Retrieve from Pinecone 
        namespace = f"user_{user_id}"
        pinecone_results = self.pinecone_client.query(
            query_embedding, 
            k=k, 
            namespace=namespace
        )
        
        # Fetch full documents from MongoDB
        document_ids = [
            result.get('id') for result in pinecone_results.get('matches', [])
        ]
        
        full_documents = list(self.documents_collection.find({
            '_id': {'$in': document_ids},
            'user_id': user_id
        }))
        
        return full_documents

    def sync_user_documents(self, user_id: str):
        """
        Synchronize documents for a specific user across all vector stores
        
        :param user_id: Unique identifier for the user
        """
        try:
            # Fetch user documents from MongoDB
            user_documents = list(self.documents_collection.find({
                'user_id': user_id
            }))
            
            if not user_documents:
                self.logger.info(f"No documents found for user {user_id}")
                return
            
            # Prepare for embedding
            texts = [doc.get('text', '') for doc in user_documents]
            
            # Generate embeddings
            embeddings = self.embedding_model.encode(texts)
            
            # Update local vector store
            local_store = self._get_or_create_local_store(user_id)
            local_store.clear()
            local_store.add_documents(user_documents, embeddings)
            
            # Prepare for Pinecone
            namespace = f"user_{user_id}"
            
            # Upsert to Pinecone
            self.pinecone_client.upsert_embeddings(
                texts=texts,
                embeddings=embeddings,
                ids=[str(doc['_id']) for doc in user_documents],
                namespace=namespace,
                metadata=[
                    {
                        'user_id': user_id,
                        'title': doc.get('title', ''),
                        'source': doc.get('source', '')
                    } for doc in user_documents
                ]
            )
            
            # Update sync tracking
            self.user_last_sync[user_id] = time.time()
            
            self.logger.info(f"Synced {len(user_documents)} documents for user {user_id}")
        
        except Exception as e:
            self.logger.error(f"Error syncing documents for user {user_id}: {e}")

    def periodic_sync_worker(self):
        """
        Background worker to periodically sync user documents
        """
        while not self._stop_sync.is_set():
            try:
                # Find users due for sync
                current_time = time.time()
                users_to_sync = [
                    user_id for user_id, last_sync in self.user_last_sync.items()
                    if current_time - last_sync >= self.sync_interval
                ]
                
                # Sync users
                for user_id in users_to_sync:
                    self.sync_user_documents(user_id)
                
                # Wait before next sync
                self._stop_sync.wait(self.sync_interval)
            
            except Exception as e:
                self.logger.error(f"Error in periodic sync worker: {e}")
                # Wait before retrying
                self._stop_sync.wait(60)

    def start_synchronization(self):
        """
        Start the background synchronization thread
        """
        if self._sync_thread is None or not self._sync_thread.is_alive():
            self._stop_sync.clear()
            self._sync_thread = threading.Thread(target=self.periodic_sync_worker)
            self._sync_thread.daemon = True
            self._sync_thread.start()
            self.logger.info("Periodic document synchronization started")

    def stop_synchronization(self):
        """
        Stop the background synchronization thread
        """
        if self._sync_thread and self._sync_thread.is_alive():
            self._stop_sync.set()
            self._sync_thread.join()
            self.logger.info("Periodic document synchronization stopped")
