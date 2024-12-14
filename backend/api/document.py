from flask import Blueprint, request, jsonify, send_file
from gridfs import GridFS
from bson.objectid import ObjectId
from io import BytesIO
from backend.db.mongo_connection import get_db
from datetime import datetime
import traceback
from backend.config import DEFAULT_USER_ID

document_bp = Blueprint('document', __name__)

@document_bp.route('/documents', methods=['POST'])
def upload_document():
    """
    Endpoint to upload a document and store it in MongoDB GridFS.
    """
    try:
        # Check if file is in the request
        if 'file' not in request.files:
            print("No file in request")
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']  # Retrieve the file
        folder = request.form.get('folder', 'My Drive')  # Folder name
        summary = request.form.get('summary', 'No summary provided')  # Optional summary
        hashtags = request.form.getlist('hashtags')  # Hashtags as a list

        print(f"Received file: {file.filename} for folder: {folder}")

        # Save file to GridFS
        db = get_db()
        fs = GridFS(db)
        file_id = fs.put(file, filename=file.filename)  # Save file to GridFS and get file_id
        print(f"File saved to GridFS with ID: {file_id}")

        # Save metadata to MongoDB
        document_metadata = {
            "user_id": DEFAULT_USER_ID,
            "folder": folder,
            "name": file.filename,
            "summary": summary,
            "hashtags": hashtags,
            "file_id": file_id,  # Reference to the file in GridFS
            "uploaded_at": datetime.now().isoformat()
        }
        result = db.documents.insert_one(document_metadata)
        print(f"Metadata saved with ID: {result.inserted_id}")

        return jsonify({
            'message': 'File uploaded successfully',
            'doc_id': str(result.inserted_id)
        }), 200
    except Exception as e:
        print(f"Error in upload_document: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


@document_bp.route('/documents', methods=['GET'])
def list_documents():
    """
    Endpoint to list all documents for the current user.
    """
    try:
        db = get_db()
        fs = GridFS(db)
        
        # Get all files for the current user
        documents = list(db.documents.find({"user_id": DEFAULT_USER_ID}))
        
        # Group files by folder
        folders = {}
        for doc in documents:
            folder = doc.get('folder', 'My Drive')
            if folder not in folders:
                folders[folder] = []
            
            folders[folder].append({
                'id': str(doc['_id']),
                'name': doc['name'],
                'summary': doc.get('summary', 'No summary'),
                'hashtags': doc.get('hashtags', []),
                'uploaded_at': doc.get('uploaded_at')
            })
        
        return jsonify(folders), 200
    except Exception as e:
        print(f"Error listing documents: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@document_bp.route('/documents/<document_id>', methods=['GET'])
def get_document(document_id):
    """
    Endpoint to retrieve a document's file and metadata.
    """
    try:
        db = get_db()
        fs = GridFS(db)
        
        try:
            doc_id = ObjectId(document_id)
        except:
            return jsonify({'error': 'Invalid document ID'}), 400
        
        # Find the document metadata for the current user
        doc_metadata = db.documents.find_one({
            '_id': doc_id, 
            'user_id': DEFAULT_USER_ID
        })
        
        if not doc_metadata:
            return jsonify({'error': 'Document not found'}), 404
        
        # Retrieve the file from GridFS
        file_id = doc_metadata.get('file_id')
        if not file_id or not fs.exists(file_id):
            return jsonify({'error': 'File not found'}), 404
        
        # Send the file
        grid_out = fs.get(file_id)
        return send_file(
            BytesIO(grid_out.read()),
            mimetype='application/octet-stream',
            download_name=doc_metadata.get('name', 'downloaded_file')
        )
    except Exception as e:
        print(f"Error in get_document: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@document_bp.route('/documents/<document_id>', methods=['DELETE'])
def delete_document(document_id):
    try:
        db = get_db()
        fs = GridFS(db)
        
        try:
            # Convert string ID to ObjectId
            doc_id = ObjectId(document_id)
        except:
            return jsonify({'error': 'Invalid document ID'}), 400
        
        # Find the document metadata
        doc_metadata = db.documents.find_one({
            '_id': doc_id, 
            'user_id': DEFAULT_USER_ID  # Ensure document belongs to current user
        })
        if not doc_metadata:
            return jsonify({'error': 'Document not found'}), 404
        
        # Get the file_id from metadata
        file_id = doc_metadata.get('file_id')
        
        # Check if file exists in GridFS
        if file_id and fs.exists(file_id):
            fs.delete(file_id)
        
        # Remove document metadata
        result = db.documents.delete_one({
            '_id': doc_id, 
            'user_id': DEFAULT_USER_ID
        })
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Failed to delete document metadata'}), 500
        
        return jsonify({'message': 'Document deleted successfully'}), 200
    except Exception as e:
        print(f"Error deleting document: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500