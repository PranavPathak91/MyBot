import os
import sys
import logging

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from backend.utils import FileProcessor

def test_file_processor():
    """
    Test the FileProcessor with a sample PDF
    """
    # Determine the path to a test PDF
    test_pdf_path = os.path.join(os.path.dirname(__file__), 'test_document.pdf')
    
    # Create a sample PDF if it doesn't exist (for demonstration)
    if not os.path.exists(test_pdf_path):
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(test_pdf_path)
        c.drawString(100, 750, "This is a test PDF for FileProcessor")
        c.drawString(100, 700, "It contains multiple lines of text")
        c.save()
    
    # Process the PDF
    result = FileProcessor.process_file(test_pdf_path)
    
    # Print the processing result
    print("Extracted Text:")
    print(result)

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    
    test_file_processor()
