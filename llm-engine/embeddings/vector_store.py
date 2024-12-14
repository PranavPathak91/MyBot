import numpy as np
from typing import List, Dict, Any
import faiss

class VectorStore:
    def __init__(self, dimension: int = 1536):
        """Initialize the vector store with specified embedding dimension."""
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents: List[Dict[str, Any]] = []

    def add_documents(self, documents: List[Dict[str, Any]], embeddings: np.ndarray):
        """Add documents and their embeddings to the store."""
        if len(documents) != embeddings.shape[0]:
            raise ValueError("Number of documents must match number of embeddings")
        
        self.index.add(embeddings)
        self.documents.extend(documents)

    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents using query embedding."""
        distances, indices = self.index.search(query_embedding.reshape(1, -1), k)
        return [
            {**self.documents[idx], "score": float(score)} 
            for score, idx in zip(distances[0], indices[0])
        ]

    def clear(self):
        """Clear the vector store."""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents = []
