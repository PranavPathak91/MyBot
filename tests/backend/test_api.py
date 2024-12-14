import pytest
from backend.app import create_app
from backend.db.models import db, User, Chat, Message, Document

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    return app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def init_database(app):
    """Initialize database for testing"""
    with app.app_context():
        db.create_all()
        
        # Create test user
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
        
        yield db
        
        db.drop_all()

def test_create_chat(client, init_database):
    """Test chat creation endpoint"""
    response = client.post('/api/chat', json={'user_id': 1})
    assert response.status_code == 201
    assert 'chat_id' in response.json

def test_send_message(client, init_database):
    """Test message sending endpoint"""
    # First create a chat
    chat_response = client.post('/api/chat', json={'user_id': 1})
    chat_id = chat_response.json['chat_id']
    
    # Send a message
    response = client.post(f'/api/chat/{chat_id}/messages', 
                         json={'content': 'Hello, bot!'})
    assert response.status_code == 200
    assert len(response.json['messages']) == 2  # User message and bot response

def test_upload_document(client, init_database):
    """Test document upload endpoint"""
    data = {
        'file': (open('test_document.txt', 'w+b'), 'test.txt'),
        'user_id': 1
    }
    response = client.post('/api/documents', data=data)
    assert response.status_code == 201
    assert 'filename' in response.json
