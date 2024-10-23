# priyanshi-tomar/wasserstoff/AiInternTask
 welcome
# Document Intelligence Pipeline

This project is a Document Intelligence Pipeline designed to process PDF files, extract text, summarize content, and extract keywords using MongoDB for storage. The pipeline leverages concurrent processing for efficient handling of multiple PDF files.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)


## Features

- Extracts text and metadata from PDF files.
- Stores extracted content in MongoDB.
- Summarizes content and extracts keywords using Natural Language Processing (NLP).
- Supports concurrent processing of multiple PDF files for efficiency.
- Configurable parameters for file paths and database settings.

## Technologies Used

- Python 3.x
- PDFMiner for PDF processing
- NLTK for Natural Language Processing
- MongoDB for data storage
- ThreadPoolExecutor for concurrent processing

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/priyanshi-tomar-wasserstoff-AiInternTask.git
   cd priyanshi-tomar-wasserstoff-AiInternTask

### Install the required packages:

in bash- 

pip install pdfminer.six pymongo nltk
Download the necessary NLTK resources (these are handled in the code):

Copy code in python-
Copy code
import nltk
nltk.download('punkt')
nltk.download('stopwords')
Make sure you have MongoDB installed and running on your local machine.

### Usage
Place your PDF files in the specified folder (default: C:\Users\Priyanshi Tomar\Desktop\pdfs).

### Run the main script to start processing:

Copy code in bash- 

python main.py
The processed data will be stored in the document_intelligence database under the pdf_data collection in MongoDB.

### Directory Structure
graphql
Copy code
project/
│
├── main.py               # Entry point for the application
├── pdf_processor.py      # Contains PDF processing logic
├── text_processor.py     # Contains text processing logic
└── config.py             # Contains configuration settings
Contributing
Contributions are welcome! If you have suggestions for improvements or find any bugs, please create an issue or submit a pull request.