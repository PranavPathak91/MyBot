from typing import Dict, Any
from string import Template

class PromptTemplates:
    # Document analysis templates
    DOCUMENT_SUMMARY = Template("""
    Please provide a concise summary of the following document:
    
    ${document_text}
    
    Focus on the main points and key takeaways.
    """)

    DOCUMENT_QUESTIONS = Template("""
    Based on the following document:
    
    ${document_text}
    
    Please answer the following question:
    ${question}
    """)

    # Style learning templates
    STYLE_ANALYSIS = Template("""
    Analyze the following text for writing style characteristics:
    
    ${sample_text}
    
    Identify key elements of the writing style, including:
    1. Tone and voice
    2. Vocabulary preferences
    3. Sentence structure patterns
    4. Common phrases or expressions
    """)

    STYLE_EMULATION = Template("""
    Given the following writing style characteristics:
    ${style_characteristics}
    
    Please respond to this prompt in the same style:
    ${prompt}
    """)

    @classmethod
    def format_prompt(cls, template_name: str, **kwargs) -> str:
        """Format a prompt template with provided variables."""
        template = getattr(cls, template_name, None)
        if template is None:
            raise ValueError(f"Template {template_name} not found")
        
        return template.safe_substitute(**kwargs)

    @classmethod
    def get_all_templates(cls) -> Dict[str, Template]:
        """Get all available prompt templates."""
        return {
            name: value for name, value in vars(cls).items()
            if isinstance(value, Template)
        }
