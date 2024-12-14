from ..embeddings.pinecone_client import PineconeEmbeddingManager

class ContextRetriever:
    def __init__(self, top_k=5):
        self.embedding_manager = PineconeEmbeddingManager()
        self.top_k = top_k

    def retrieve_context(self, query):
        """
        Retrieve relevant context for a given query
        
        Args:
            query (str): User query
        
        Returns:
            list: Relevant context snippets
        """
        try:
            results = self.embedding_manager.index.query(
                self.embedding_manager.model.encode([query])[0].tolist(), 
                top_k=self.top_k,
                include_metadata=True
            )
            
            contexts = [
                match['metadata']['text'] 
                for match in results['matches']
            ]
            
            return contexts
        except Exception as e:
            print(f"Context retrieval error: {e}")
            return []
