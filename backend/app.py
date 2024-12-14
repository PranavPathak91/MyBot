from flask import Flask
from flask_cors import CORS
from backend.db import init_db
from backend.api import blueprints
import os

def create_app():
    app = Flask(__name__)
    # Configure CORS to be completely permissive for development
    CORS(app, 
         supports_credentials=True,
         resources={r"/*": {
             "origins": "*",
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
             "allow_headers": "*"
         }}
    )

    # Initialize database
    init_db(app)

    # Register blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5002)
