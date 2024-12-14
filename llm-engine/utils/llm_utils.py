from typing import List, Dict, Any, Optional
import torch
import numpy as np

class LLMUtils:
    @staticmethod
    def chunk_text(text: str, chunk_size: int, overlap: int = 100) -> List[str]:
        """Split text into overlapping chunks."""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            
            # Adjust chunk end to not split words
            if end < len(text):
                end = text.rfind(' ', start, end)
                if end == -1:
                    end = start + chunk_size
            
            chunks.append(text[start:end])
            start = end - overlap
            
        return chunks

    @staticmethod
    def combine_embeddings(embeddings: List[torch.Tensor], 
                         weights: Optional[List[float]] = None) -> torch.Tensor:
        """Combine multiple embeddings with optional weights."""
        if weights is None:
            weights = [1.0] * len(embeddings)
        
        if len(embeddings) != len(weights):
            raise ValueError("Number of embeddings must match number of weights")
        
        weighted_sum = sum(emb * w for emb, w in zip(embeddings, weights))
        return weighted_sum / sum(weights)

    @staticmethod
    def cosine_similarity(a: torch.Tensor, b: torch.Tensor) -> float:
        """Calculate cosine similarity between two vectors."""
        return float(torch.nn.functional.cosine_similarity(a, b, dim=0))

    @staticmethod
    def format_context(documents: List[Dict[str, Any]], 
                      max_length: int = 2000) -> str:
        """Format retrieved documents into context string."""
        context = []
        current_length = 0
        
        for doc in documents:
            doc_text = doc["text"]
            doc_length = len(doc_text)
            
            if current_length + doc_length > max_length:
                remaining = max_length - current_length
                if remaining > 100:  # Only add if remaining space is significant
                    context.append(doc_text[:remaining])
                break
            
            context.append(doc_text)
            current_length += doc_length
        
        return "\n\n".join(context)
