# text_processor.py
import pymongo
import logging
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
import string
import re
import nltk
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Load NLTK stopwords
stop_words = set(stopwords.words('english'))

# Simple text summarization function (based on word frequency)
def summarize_text(text, max_sentences=3):
    sentences = sent_tokenize(text)  # Use NLTK's sentence tokenizer
    sentence_weights = {}
    word_frequencies = Counter(word_tokenize(text.lower()))
    
    for sentence in sentences:
        sentence_words = word_tokenize(sentence.lower())
        sentence_weights[sentence] = sum(word_frequencies[word] for word in sentence_words if word not in stop_words)

    # Sort by most important sentences
    sorted_sentences = sorted(sentence_weights, key=sentence_weights.get, reverse=True)
    summary = ' '.join(sorted_sentences[:max_sentences])
    return summary

# Simple keyword extraction function (based on frequency)
def extract_keywords(text, num_keywords=5):
    words = word_tokenize(re.sub(r'[^\w\s]', '', text.lower()))  # Remove punctuation
    filtered_words = [word for word in words if word not in stop_words and len(word) > 1]
    word_frequencies = Counter(filtered_words)
    return [word for word, _ in word_frequencies.most_common(num_keywords)]

# Function to update MongoDB with summary, keywords, and length of summary
def apply_domain_adjustments(db_name=DB_NAME, collection_name=COLLECTION_NAME):
    # Connect to MongoDB
    mongo_client = pymongo.MongoClient(MONGO_URI)
    db = mongo_client[db_name]
    collection = db[collection_name]

    cursor = collection.find()
    total_documents = collection.count_documents({})
    for i, document in enumerate(cursor, start=1):
        text_content = document["content"]  # Adjust this to match your document structure

        # Apply domain-specific processing
        summary = summarize_text(text_content)
        keywords = extract_keywords(text_content)
        summary_length = len(summary.split())

        # Update MongoDB document
        try:
            collection.update_one(
                {"_id": document["_id"]},
                {"$set": {
                    "summary": summary,
                    "keywords": keywords,
                    "summary_length": summary_length
                }}
            )
            logging.info(f"Updated document {document['file_name']} with summary and keywords. ({i}/{total_documents})")
        except Exception as e:
            logging.error(f"Error updating document {document['file_name']}: {e}")
