# pdf_processor.py
import os
import json
import pymongo
import logging
from pdfminer.high_level import extract_text
from concurrent.futures import ThreadPoolExecutor
from bson import ObjectId
import nltk
from config import MONGO_URI, DB_NAME, COLLECTION_NAME, PDF_FOLDER_PATH

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# MongoDB configuration
mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
pdf_data_collection = db[COLLECTION_NAME]

# Utility function to convert ObjectId to string for JSON serialization
def convert_objectid_to_string(data):
    """Convert ObjectId to string for JSON serialization."""
    if isinstance(data, dict):
        return {k: convert_objectid_to_string(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_string(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    return data

# Function to process a single PDF file
def process_pdf(pdf_file):
    """Extract text and metadata from a PDF file and store it in MongoDB."""
    try:
        logging.info(f"Processing {pdf_file}...")  # Indicate which file is being processed
        # Extract text from the PDF
        text = extract_text(pdf_file)

        # Create metadata dictionary
        pdf_metadata = {
            "file_name": os.path.basename(pdf_file),
            "file_path": pdf_file,
            "content": text,
            "summary": "",  # Placeholder, will be updated later
            "keywords": [],  # Placeholder, will be updated later
        }

        # Insert metadata into MongoDB and get the inserted ID
        result = pdf_data_collection.insert_one(pdf_metadata)

        # Add the inserted ID to metadata
        pdf_metadata["_id"] = result.inserted_id

        logging.info(f"Successfully processed {pdf_file}.")  # Confirmation of successful processing
        return pdf_metadata
    except Exception as e:
        logging.error(f"Error processing {pdf_file}: {e}")
        return None

# Main function to process PDFs in a given folder
def process_pdfs_in_folder(folder_path):
    """Process all PDF files in the specified folder."""
    pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pdf')]
    logging.info(f"Found {len(pdf_files)} PDF files to process in {folder_path}.")

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_pdf, pdf_files))
    
    return results
