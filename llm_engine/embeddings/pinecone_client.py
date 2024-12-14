import os
import logging
import pinecone
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
import numpy as np

class PineconeEmbeddingManager:
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        index_name: Optional[str] = 'test-index',
        model_name: Optional[str] = 'all-MiniLM-L6-v2'
    ):
        """
        Initialize Pinecone Embedding Manager
        
        :param api_key: Pinecone API key (optional, uses environment variable)
        :param index_name: Name of the Pinecone index
        :param model_name: Name of the sentence transformer model
        """
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Use API key from environment or parameter
        self.api_key = api_key or os.getenv('PINECONE_API_KEY')
        if not self.api_key:
            raise ValueError("Pinecone API key is required")
        
        # Initialize embedding model
        self.model_name = model_name
        self.model = SentenceTransformer(self.model_name)
        
        # Get embedding dimension
        self.embedding_dimension = self.model.get_sentence_embedding_dimension()
        
        try:
            # Initialize Pinecone client
            self.pc = pinecone.Pinecone(api_key=self.api_key)
            
            # Set index name
            self.index_name = index_name
            
            # Create or update index if needed
            self._setup_index()
            
            # Get index reference
            self.index = self.pc.Index(self.index_name)
            
        except Exception as e:
            self.logger.error(f"Pinecone initialization failed: {e}")
            raise
    
    def _setup_index(self):
        """
        Create or update Pinecone index
        """
        try:
            # Check if index exists
            existing_indexes = [idx.name for idx in self.pc.list_indexes()]
            
            # If index exists, check its configuration
            if self.index_name in existing_indexes:
                # Get index details
                index_details = next(
                    (idx for idx in self.pc.list_indexes() if idx.name == self.index_name), 
                    None
                )
                
                # If dimension is different, delete and recreate
                if index_details and index_details.dimension != self.embedding_dimension:
                    self.logger.warning(f"Deleting existing index with mismatched dimension: {self.index_name}")
                    self.pc.delete_index(self.index_name)
                    existing_indexes.remove(self.index_name)
            
            # Create index if not exists
            if self.index_name not in existing_indexes:
                self.logger.info(f"Creating index: {self.index_name}")
                
                # Create serverless index with dynamic dimension
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.embedding_dimension,
                    metric='cosine',
                    spec={
                        'serverless': {
                            'cloud': 'aws',
                            'region': 'us-east-1'
                        }
                    }
                )
                self.logger.info(f"Index {self.index_name} created successfully with dimension {self.embedding_dimension}")
            
        except Exception as e:
            self.logger.error(f"Index setup failed: {e}")
            raise
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for given texts
        
        :param texts: List of text strings
        :return: List of embeddings
        """
        try:
            embeddings = self.model.encode(texts).tolist()
            return embeddings
        except Exception as e:
            self.logger.error(f"Embedding generation failed: {e}")
            raise
    
    def upsert_embeddings(
        self, 
        texts: List[str], 
        embeddings: Optional[List[List[float]]] = None,
        ids: Optional[List[str]] = None,
        namespace: str = 'default', 
        metadata: Optional[List[Dict[str, Any]]] = None
    ):
        """
        Upsert embeddings into Pinecone index with enhanced flexibility
        
        :param texts: List of text strings
        :param embeddings: Optional pre-computed embeddings
        :param ids: Optional custom vector IDs
        :param namespace: Namespace to upsert vectors into
        :param metadata: Optional list of metadata dictionaries
        """
        try:
            # Generate embeddings if not provided
            if embeddings is None:
                embeddings = self.generate_embeddings(texts)
            
            # Generate IDs if not provided
            if ids is None:
                ids = [str(i) for i in range(len(texts))]
            
            # Prepare vectors for upsert
            vectors = [
                {
                    'id': str(vector_id), 
                    'values': emb, 
                    'metadata': meta or {}
                }
                for vector_id, emb, meta in zip(
                    ids, 
                    embeddings, 
                    metadata or [{}]*len(texts)
                )
            ]
            
            # Upsert vectors into specified namespace
            self.index.upsert(
                vectors=vectors, 
                namespace=namespace
            )
            self.logger.info(f"Upserted {len(vectors)} vectors in namespace '{namespace}'")
        
        except Exception as e:
            self.logger.error(f"Embedding upsert failed: {e}")
            raise

    def query(
        self, 
        query_embedding: np.ndarray, 
        k: int = 5, 
        namespace: str = 'default',
        filter: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Enhanced query method with more flexible parameters
        
        :param query_embedding: Numpy array of query embedding
        :param k: Number of top results to return
        :param namespace: Namespace to query
        :param filter: Optional metadata filter
        :return: Query results dictionary
        """
        try:
            # Perform query with optional filtering
            query_results = self.index.query(
                vector=query_embedding.tolist(),
                top_k=k,
                namespace=namespace,
                filter=filter or {}
            )
            
            return query_results
        
        except Exception as e:
            self.logger.error(f"Embedding query failed: {e}")
            raise

    def delete_embeddings(
        self, 
        ids: List[str], 
        namespace: str = 'default'
    ):
        """
        Delete specific vectors from a namespace
        
        :param ids: List of vector IDs to delete
        :param namespace: Namespace to delete from
        """
        try:
            self.index.delete(
                ids=ids,
                namespace=namespace
            )
            self.logger.info(f"Deleted {len(ids)} vectors from namespace '{namespace}'")
        
        except Exception as e:
            self.logger.error(f"Vector deletion failed: {e}")
            raise

    def fetch_vector_by_id(
        self, 
        vector_id: str, 
        namespace: str = 'default'
    ) -> Optional[np.ndarray]:
        """
        Fetch a specific vector by its ID
        
        :param vector_id: ID of the vector to fetch
        :param namespace: Namespace to fetch from
        :return: Numpy array of vector embedding
        """
        try:
            # Fetch vector details
            fetch_result = self.index.fetch([vector_id], namespace=namespace)
            
            # Extract vector values
            vectors = fetch_result.get('vectors', {})
            if vector_id in vectors:
                return np.array(vectors[vector_id]['values'])
            
            return None
        
        except Exception as e:
            self.logger.error(f"Vector fetch failed: {e}")
            return None

    def get_index_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the Pinecone index
        
        :return: Index statistics dictionary
        """
        try:
            stats = self.index.describe_index_stats()
            return stats
        except Exception as e:
            self.logger.error(f"Failed to retrieve index stats: {e}")
            raise
