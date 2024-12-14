import os
import logging
from typing import Optional, Union, Dict, Any

import PyPDF2
import pdfplumber

class FileProcessor:
    """
    A utility class for processing various file types, with a focus on PDF extraction.
    
    Supports multiple methods of PDF text extraction to ensure robust text retrieval.
    """
    
    @staticmethod
    def extract_pdf_text(file_path: str) -> Optional[str]:
        """
        Extract text from a PDF file using multiple methods for robustness.
        
        Args:
            file_path (str): Path to the PDF file
        
        Returns:
            Optional[str]: Extracted text from the PDF, or None if extraction fails
        """
        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            return None
        
        try:
            # Method 1: Using pdfplumber (more robust for complex PDFs)
            with pdfplumber.open(file_path) as pdf:
                text = "\n".join([page.extract_text() or "" for page in pdf.pages])
                if text and text.strip():
                    return text
        except Exception as pdfplumber_error:
            logging.warning(f"pdfplumber extraction failed: {pdfplumber_error}")
        
        try:
            # Method 2: Using PyPDF2 (fallback method)
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                
                if text and text.strip():
                    return text
        except Exception as pypdf_error:
            logging.error(f"PyPDF2 extraction failed: {pypdf_error}")
        
        logging.error(f"Could not extract text from PDF: {file_path}")
        return None
    
    @staticmethod
    def process_file(file_path: str) -> Union[str, None]:
        """
        Process a file and extract its text content.
        
        Args:
            file_path (str): Path to the file to be processed
        
        Returns:
            Union[str, None]: Extracted text from the file, or None if extraction fails
        """
        # Validate file existence
        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            return None
        
        # Determine file extension
        file_extension = os.path.splitext(file_path)[1].lower()
        
        # Process based on file type
        try:
            if file_extension == '.pdf':
                text = FileProcessor.extract_pdf_text(file_path)
                if text:
                    return text
                else:
                    logging.error(f"Could not extract text from PDF: {file_path}")
                    return None
            else:
                logging.error(f"Unsupported file type: {file_extension}")
                return None
        except Exception as e:
            logging.error(f"File processing error: {e}")
            return None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
