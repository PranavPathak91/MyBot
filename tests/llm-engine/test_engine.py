import pytest
from backend.llm_engine.engine import LLMEngine
import torch

@pytest.fixture
def llm_engine():
    """Create LLM engine instance for testing"""
    # Initialize with test models
    return LLMEngine(
        model=None,  # Mock model for testing
        tokenizer=None,  # Mock tokenizer for testing
        embedding_model=None,  # Mock embedding model for testing
        device="cpu"
    )

def test_process_query(llm_engine):
    """Test query processing"""
    response = llm_engine.process_query(
        query="What is machine learning?",
        max_length=100,
        temperature=0.7
    )
    assert 'response' in response
    assert 'metadata' in response

def test_add_documents(llm_engine):
    """Test document addition to vector store"""
    documents = [
        {
            'content': 'Test document content',
            'metadata': {'title': 'Test Doc'}
        }
    ]
    llm_engine.add_documents(documents)
    # Verify documents were added (implementation dependent)

def test_analyze_style(llm_engine):
    """Test style analysis"""
    text = "This is a test document for style analysis."
    analysis = llm_engine.analyze_style(text)
    assert 'style_analysis' in analysis

def test_generate_with_style(llm_engine):
    """Test style-based generation"""
    prompt = "Generate a response"
    style = "formal and technical"
    response = llm_engine.generate_with_style(
        prompt=prompt,
        style_characteristics=style
    )
    assert isinstance(response, str)
    assert len(response) > 0
