from typing import List, Dict, Any, Optional
import torch
from .embeddings.vector_store import VectorStore
from .embeddings.retriever import RAGRetriever
from .models.inference import LLMInference
from .models.tokenizer import TokenizerUtils
from .utils.prompt_templates import PromptTemplates
from .utils.llm_utils import LLMUtils

class LLMEngine:
    def __init__(
        self,
        model,
        tokenizer,
        embedding_model,
        device: str = "cuda" if torch.cuda.is_available() else "cpu"
    ):
        """Initialize the LLM engine with all components."""
        self.inference = LLMInference(model, tokenizer, device)
        self.tokenizer_utils = TokenizerUtils(tokenizer)
        self.vector_store = VectorStore()
        self.retriever = RAGRetriever(self.vector_store, embedding_model)

    def process_query(
        self,
        query: str,
        max_length: int = 1000,
        temperature: float = 0.7,
        use_rag: bool = True,
        context_size: int = 5
    ) -> Dict[str, Any]:
        """Process a query and generate a response."""
        # Get relevant context if RAG is enabled
        context = None
        if use_rag:
            context = self.retriever.retrieve(query, k=context_size)
            
        # Generate response
        response = self.inference.generate(
            query,
            max_length=max_length,
            temperature=temperature,
            context=context
        )
        
        return {
            "response": response,
            "context": context,
            "metadata": {
                "tokens_used": self.tokenizer_utils.count_tokens(response),
                "context_used": bool(context)
            }
        }

    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to the vector store for RAG."""
        self.retriever.add_documents(documents)

    def analyze_style(self, text: str) -> Dict[str, Any]:
        """Analyze writing style characteristics."""
        prompt = PromptTemplates.format_prompt(
            "STYLE_ANALYSIS",
            sample_text=text
        )
        
        response = self.inference.generate(prompt)
        return {"style_analysis": response}

    def generate_with_style(
        self,
        prompt: str,
        style_characteristics: str,
        temperature: float = 0.8
    ) -> str:
        """Generate response following specific style characteristics."""
        styled_prompt = PromptTemplates.format_prompt(
            "STYLE_EMULATION",
            style_characteristics=style_characteristics,
            prompt=prompt
        )
        
        return self.inference.generate(
            styled_prompt,
            temperature=temperature
        )
