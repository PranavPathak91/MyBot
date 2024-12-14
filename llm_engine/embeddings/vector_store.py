import numpy as np
from typing import List, Dict, Any, Optional, Union
import faiss
import uuid
import logging

class VectorStore:
    def __init__(
        self, 
        dimension: int = 1536, 
        metric: str = 'l2',
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize the vector store with specified embedding dimension
        
        :param dimension: Dimensionality of embeddings
        :param metric: Distance metric for index ('l2' or 'cosine')
        :param logger: Optional logger for tracking operations
        """
        self.dimension = dimension
        self.logger = logger or logging.getLogger(__name__)
        
        # Create FAISS index based on metric
        if metric == 'l2':
            self.index = faiss.IndexFlatL2(dimension)
        elif metric == 'cosine':
            self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine
        else:
            raise ValueError(f"Unsupported metric: {metric}")
        
        # Document storage with enhanced metadata
        self.documents: List[Dict[str, Any]] = []
        self.document_ids: List[str] = []

    def add_documents(
        self, 
        documents: List[Dict[str, Any]], 
        embeddings: np.ndarray,
        generate_ids: bool = True
    ):
        """
        Add documents and their embeddings to the store
        
        :param documents: List of document dictionaries
        :param embeddings: Numpy array of embeddings
        :param generate_ids: Automatically generate unique IDs if not present
        """
        if len(documents) != embeddings.shape[0]:
            raise ValueError("Number of documents must match number of embeddings")
        
        # Normalize and add embeddings to index
        normalized_embeddings = self._normalize_embeddings(embeddings)
        self.index.add(normalized_embeddings)
        
        # Process documents with ID management
        for doc, embedding in zip(documents, embeddings):
            # Generate or use existing ID
            doc_id = doc.get('id') if not generate_ids else str(uuid.uuid4())
            
            # Ensure user_id is present
            if 'user_id' not in doc:
                self.logger.warning("Document missing user_id")
            
            # Store document and ID
            self.documents.append(doc)
            self.document_ids.append(doc_id)

    def search(
        self, 
        query_embedding: np.ndarray, 
        k: int = 5,
        filter_fn: Optional[callable] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents using query embedding
        
        :param query_embedding: Query embedding vector
        :param k: Number of results to return
        :param filter_fn: Optional function to filter results
        :return: List of most similar documents
        """
        # Normalize query embedding
        normalized_query = self._normalize_embeddings(query_embedding.reshape(1, -1))
        
        # Perform search
        distances, indices = self.index.search(normalized_query, k)
        
        # Prepare results with scoring
        results = [
            {
                **self.documents[idx], 
                "score": float(score),
                "id": self.document_ids[idx]
            } 
            for score, idx in zip(distances[0], indices[0])
        ]
        
        # Apply optional filtering
        if filter_fn:
            results = [doc for doc in results if filter_fn(doc)]
        
        return results

    def delete_document(self, document_id: str):
        """
        Delete a specific document by its ID
        
        :param document_id: ID of the document to delete
        """
        try:
            # Find document index
            doc_index = self.document_ids.index(document_id)
            
            # Remove from documents and IDs
            del self.documents[doc_index]
            del self.document_ids[doc_index]
            
            # Rebuild FAISS index
            self._rebuild_index()
        
        except ValueError:
            self.logger.warning(f"Document {document_id} not found")

    def _rebuild_index(self):
        """
        Rebuild the FAISS index after deletions
        """
        # Recreate index
        self.index = faiss.IndexFlatL2(self.dimension)
        
        # Re-add remaining embeddings
        if self.documents:
            embeddings = np.array([
                self._get_embedding(doc) for doc in self.documents
            ])
            self.index.add(embeddings)

    def _get_embedding(self, document: Dict[str, Any]) -> np.ndarray:
        """
        Extract or generate embedding for a document
        
        :param document: Document dictionary
        :return: Embedding vector
        """
        # Implement your embedding extraction logic here
        # This is a placeholder and should be replaced with actual embedding retrieval
        return np.zeros(self.dimension)

    def _normalize_embeddings(self, embeddings: np.ndarray) -> np.ndarray:
        """
        Normalize embeddings for consistent comparison
        
        :param embeddings: Input embeddings
        :return: Normalized embeddings
        """
        # L2 normalization
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        return embeddings / norms

    def clear(self):
        """Clear the vector store completely."""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents = []
        self.document_ids = []

    def get_document_count(self) -> int:
        """
        Get the number of documents in the store
        
        :return: Total number of documents
        """
        return len(self.documents)

    def get_documents_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all documents for a specific user
        
        :param user_id: User identifier
        :return: List of user's documents
        """
        return [
            doc for doc in self.documents 
            if doc.get('user_id') == user_id
        ]
