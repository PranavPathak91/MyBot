import os
import yaml
from typing import Dict, Any, Optional
from dotenv import load_dotenv

class ConfigurationError(Exception):
    """Custom exception for configuration-related errors"""
    pass

class ConfigManager:
    def __init__(self, 
                 prompts_path: str = 'config/prompts.yaml', 
                 model_config_path: str = 'config/model_config.yaml'):
        """
        Initialize ConfigManager with paths to configuration files
        
        Args:
            prompts_path (str): Path to prompts configuration file
            model_config_path (str): Path to model configuration file
        """
        # Load environment variables
        load_dotenv()
        
        # Resolve absolute paths
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.prompts_path = os.path.join(base_dir, prompts_path)
        self.model_config_path = os.path.join(base_dir, model_config_path)
        
        # Initialize configuration dictionaries
        self.prompts_config: Dict[str, Any] = {}
        self.model_config: Dict[str, Any] = {}
        
        # Load configurations
        self._load_configurations()

    def _load_configurations(self):
        """
        Load configuration files and validate their contents
        """
        try:
            with open(self.prompts_path, 'r') as prompts_file:
                self.prompts_config = yaml.safe_load(prompts_file) or {}
            
            with open(self.model_config_path, 'r') as model_config_file:
                self.model_config = yaml.safe_load(model_config_file) or {}
        except FileNotFoundError as e:
            raise ConfigurationError(f"Configuration file not found: {e}")
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Error parsing configuration: {e}")

    def get_system_prompt(self, prompt_key: str = 'default') -> str:
        """
        Retrieve a system prompt by key
        
        Args:
            prompt_key (str): Key of the system prompt to retrieve
        
        Returns:
            str: System prompt text
        """
        return self.prompts_config.get('system_prompts', {}).get(prompt_key, '')

    def get_task_prompt(self, task_key: str) -> str:
        """
        Retrieve a task-specific prompt
        
        Args:
            task_key (str): Key of the task prompt
        
        Returns:
            str: Task prompt text
        """
        return self.prompts_config.get('task_prompts', {}).get(task_key, '')

    def get_context_template(self, template_key: str) -> str:
        """
        Retrieve a context template
        
        Args:
            template_key (str): Key of the context template
        
        Returns:
            str: Context template text
        """
        return self.prompts_config.get('context_templates', {}).get(template_key, '')

    def get_model_config(self, model_type: str = 'openai', config_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve model configuration
        
        Args:
            model_type (str): Type of model (e.g., 'openai', 'local')
            config_key (str, optional): Specific configuration key
        
        Returns:
            Dict[str, Any]: Model configuration or specific config value
        """
        model_configs = self.model_config.get('models', {}).get(model_type, {})
        
        if config_key:
            return model_configs.get(config_key)
        
        return model_configs

    def get_embedding_model(self, model_key: str = 'default') -> str:
        """
        Retrieve embedding model name
        
        Args:
            model_key (str): Key of the embedding model
        
        Returns:
            str: Embedding model name
        """
        embedding_models = self.model_config.get('embedding_models', {})
        
        if model_key == 'default':
            return embedding_models.get('default', '')
        
        return embedding_models.get('alternatives', [])[0] if embedding_models.get('alternatives') else ''

    def get_all_configs(self) -> Dict[str, Any]:
        """
        Retrieve all configurations
        
        Returns:
            Dict[str, Any]: Complete configuration dictionary
        """
        return {
            'prompts': self.prompts_config,
            'models': self.model_config
        }

# Create a global config manager instance
config_manager = ConfigManager()