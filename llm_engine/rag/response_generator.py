from ..models.inference import generate_response

class ResponseGenerator:
    def __init__(self, model_name='default'):
        self.model_name = model_name

    def generate(self, prompt, context=None):
        """
        Generate a response with optional context
        
        Args:
            prompt (str): User query or prompt
            context (list, optional): Retrieved context snippets
        
        Returns:
            str: Generated response
        """
        # Combine context and prompt if context is provided
        full_prompt = prompt
        if context:
            context_str = "\n".join(context)
            full_prompt = f"Context: {context_str}\n\nQuery: {prompt}"
        
        # Use the inference module to generate response
        response = generate_response(
            prompt=full_prompt, 
            model_name=self.model_name
        )
        
        return response
