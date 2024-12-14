from typing import List, Dict, Any
from transformers import PreTrainedTokenizer

class TokenizerUtils:
    def __init__(self, tokenizer: PreTrainedTokenizer):
        """Initialize tokenizer utilities."""
        self.tokenizer = tokenizer

    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text."""
        return len(self.tokenizer.encode(text))

    def truncate_text(self, text: str, max_tokens: int) -> str:
        """Truncate text to fit within max_tokens limit."""
        tokens = self.tokenizer.encode(text)
        if len(tokens) <= max_tokens:
            return text
        
        truncated_tokens = tokens[:max_tokens]
        return self.tokenizer.decode(truncated_tokens)

    def batch_encode(self, texts: List[str], **kwargs) -> Dict[str, Any]:
        """Encode a batch of texts."""
        return self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            return_tensors="pt",
            **kwargs
        )

    def batch_decode(self, token_ids: List[List[int]], **kwargs) -> List[str]:
        """Decode a batch of token IDs."""
        return self.tokenizer.batch_decode(token_ids, **kwargs)
