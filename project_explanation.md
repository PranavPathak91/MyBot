# MyBot Project Architecture Overview

## 🏗️ Project Structure and Design Philosophy

### High-Level Architecture
The MyBot project is a sophisticated document management and AI-powered analysis platform, designed with a modular, scalable microservices-like architecture. The system is divided into three primary components:

1. **Backend Services** (Python/Flask)
2. **Frontend Interface** (React)
3. **LLM Engine** (Machine Learning Core)

### 📂 Detailed Directory Structure

```
MyBot/
│
├── backend/                  # Server-side application logic
│   ├── api/                  # API endpoint definitions
│   │   ├── __init__.py       # Blueprint registration
│   │   ├── document.py       # Document-related REST endpoints
│   │   └── user.py           # User management endpoints
│   │
│   ├── db/                   # Database interaction layer
│   │   ├── __init__.py       # Database initialization
│   │   ├── mongo_connection.py  # MongoDB connection management
│   │   └── models.py         # Data models and schemas
│   │
│   ├── utils/                # Utility modules
│   │   ├── error_handler.py  # Centralized error handling
│   │   └── auth.py           # Authentication utilities
│   │
│   ├── config.py             # Application configuration
│   └── app.py                # Flask application factory
│
├── frontend/                 # React-based user interface
│   └── src/
│       ├── components/       # Reusable UI components
│       └── pages/
│           └── DocumentUploadPage.jsx  # Main document management view
│
├── llm-engine/               # Machine Learning Core
│   ├── embeddings/           # Vector representation logic
│   │   ├── pinecone_client.py  # Vector database integration
│   │   ├── retriever.py      # Retrieval augmentation
│   │   └── vector_store.py   # Vector storage management
│   │
│   ├── models/               # Machine Learning Models
│   │   ├── inference.py      # Model inference pipeline
│   │   ├── tokenizer.py      # Text tokenization
│   │   └── finetune.py       # Model fine-tuning utilities
│   │
│   └── utils/                # ML Utility Functions
│       ├── prompt_templates.py  # Prompt engineering
│       └── llm_utils.py      # LLM helper functions
│
├── .env                      # Environment configuration
└── requirements.txt          # Python dependency management
```

## 🗃️ Database Design

### MongoDB Schema

#### 1. Documents Collection
```json
{
  "_id": "ObjectId",
  "user_id": "default_user_123",
  "folder": "My Drive",
  "name": "document.pdf",
  "summary": "Automatically generated document summary",
  "hashtags": ["#research", "#important"],
  "file_id": "GridFS_ObjectId",
  "uploaded_at": "ISO_8601_Timestamp",
  "metadata": {
    "file_type": "pdf",
    "size_bytes": 1024,
    "last_processed": "Timestamp"
  }
}
```

#### 2. GridFS File Storage
- Stores actual document binary content
- Referenced by `file_id` in documents collection
- Supports large file storage beyond BSON document size limits

## 🔧 Technology Stack

### Backend
- **Web Framework**: Flask
- **Database**: MongoDB (PyMongo)
- **File Storage**: GridFS
- **Authentication**: JWT (planned)

### Frontend
- **Framework**: React
- **State Management**: React Hooks
- **HTTP Client**: Fetch API

### Machine Learning
- **Vector Database**: Pinecone
- **ML Framework**: PyTorch
- **NLP**: Hugging Face Transformers
- **Embedding**: Sentence Transformers

## 🚀 Current System Capabilities

1. **Document Management**
   - Upload documents to specific folders
   - Generate automatic summaries
   - Add hashtag-based categorization
   - Retrieve documents with metadata

2. **API Endpoints**
   - `/documents` (GET): List all documents
   - `/documents` (POST): Upload new document
   - Future: Document search, advanced filtering

## 🧠 LLM Engine Design Considerations

### Embedding Generation
- Convert documents to high-dimensional vector representations
- Use state-of-the-art transformer models
- Support multiple document types (PDF, DOCX, TXT)

### Retrieval Augmented Generation (RAG)
- Semantic search across document corpus
- Dynamic context retrieval
- Prompt engineering for contextual responses

### Vector Storage Strategy
- Pinecone for scalable, fast vector similarity search
- Efficient indexing and retrieval
- Support for incremental updates

## 🔍 Recommended Next Steps for LLM Integration

1. Implement document embedding generation
2. Create vector store initialization
3. Develop RAG retrieval mechanism
4. Design prompt templates for different use cases
5. Build inference pipeline with context-aware responses

## 🛠️ Configuration Management
- Environment-based configuration
- Secure credential management
- Flexible deployment across environments

## 📊 Performance Considerations
- Asynchronous processing
- Efficient vector storage
- Minimal latency in document retrieval
- Scalable architecture
