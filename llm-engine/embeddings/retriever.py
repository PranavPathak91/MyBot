from typing import List, Dict, Any
import numpy as np
from .vector_store import VectorStore

class RAGRetriever:
    def __init__(self, vector_store: VectorStore, embedding_model: Any):
        """Initialize the RAG retriever with a vector store and embedding model."""
        self.vector_store = vector_store
        self.embedding_model = embedding_model

    def retrieve(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant documents for a query using RAG."""
        # Get query embedding
        query_embedding = self.embedding_model.encode(query)
        
        # Search vector store
        results = self.vector_store.search(query_embedding, k=k)
        
        # Sort by relevance score
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results

    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add new documents to the retriever."""
        # Generate embeddings for documents
        texts = [doc["text"] for doc in documents]
        embeddings = self.embedding_model.encode(texts)
        
        # Add to vector store
        self.vector_store.add_documents(documents, embeddings)
