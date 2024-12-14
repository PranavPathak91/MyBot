from typing import List, Dict, Any, Optional
import torch
from transformers import PreTrainedModel, PreTrainedTokenizer

class LLMInference:
    def __init__(
        self,
        model: PreTrainedModel,
        tokenizer: PreTrainedTokenizer,
        device: str = "cuda" if torch.cuda.is_available() else "cpu"
    ):
        """Initialize the LLM inference wrapper."""
        self.model = model.to(device)
        self.tokenizer = tokenizer
        self.device = device

    def generate(
        self,
        prompt: str,
        max_length: int = 1000,
        temperature: float = 0.7,
        top_p: float = 0.9,
        context: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Generate text response from the model."""
        # Prepare input with context if provided
        if context:
            context_text = "\n".join([doc["text"] for doc in context])
            full_prompt = f"{context_text}\n\n{prompt}"
        else:
            full_prompt = prompt

        # Tokenize input
        inputs = self.tokenizer(
            full_prompt,
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(self.device)

        # Generate response
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )

        # Decode and return response
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response[len(full_prompt):].strip()

    def get_embedding(self, text: str) -> torch.Tensor:
        """Get embeddings for input text."""
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            # Use the last hidden state as embedding
            embeddings = outputs.last_hidden_state.mean(dim=1)

        return embeddings
