"""
API Blueprint initialization
"""
from .document import document_bp
from .user import user_bp

blueprints = [document_bp, user_bp]
