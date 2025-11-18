Legal Document Insight Extractor ⚖️
This project is a full-stack web application that uses IBM Watson Natural Language Understanding (NLU) to extract key insights from legal documents.

Users can upload a .pdf, .docx, or .txt file through a custom web interface. The application analyzes the document and displays extracted information, including legal entities (people, organizations, laws), document categories (e.g., /law/crime), and overall sentiment (positive, negative, neutral).

📸 Screenshots
Here is the application in action, showing the results from analyzing a sample document.

✨ Key Features
Multi-Format Support: Extracts text from .pdf, .docx, and .txt files.

AI-Powered NLU: Leverages IBM Watson to perform deep text analysis.

Key Insight Extraction:

Entities: Identifies people, organizations, locations, laws, and legal references.

Categories: Classifies the document's topic (e.g., /business/corporate, /law/crime).

Sentiment: Analyzes the overall tone of the document.

Keywords: Pulls out the most relevant legal phrases and terms.

Full-Stack Application:

Flask Backend: A Python server handles file uploads, text extraction, and API calls.

Custom UI: A clean, responsive frontend built with HTML, CSS, and JavaScript.

Secure: API keys are kept secure using a .env file.

🛠️ Architecture & Tech Stack
This project is separated into a backend API and a frontend UI.

Backend:

Framework: Flask

AI Service: IBM Watson NLU

Text Extraction: pdfplumber (for PDFs) and docx2txt (for DOCX)

Environment: python-dotenv (for secure key management)

Frontend:

Structure: HTML5

Styling: CSS3

Interactivity: JavaScript (using fetch to call the backend API)

🚀 Setup and Installation
Follow these steps to run the project locally.

1. Prerequisites
Python 3.8+

An IBM Cloud account with Natural Language Understanding service credentials (API Key and URL).

2. Clone the Repository
(If this were on GitHub, you would clone it. For now, just ensure you have the project folder.)

Bash

git clone https://your-repo-url.git
cd legal_extractor
3. Set Up the Environment
Create and activate a Python virtual environment.

Bash

# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
4. Install Dependencies
Install all required libraries from the requirements.txt file.

Bash

pip install -r requirements.txt
5. Create the .env File
This is a critical step for security.

Create a new file in the root directory named .env

Add your IBM Watson credentials to this file:

Ini, TOML

# IBM Watson Credentials
IBM_API_KEY="YOUR_API_KEY_HERE"
IBM_SERVICE_URL="YOUR_SERVICE_URL_HERE"
▶️ How to Run the Application
Start the Flask Server: Run the app.py file from your terminal. The use_reloader=False argument is important to prevent the server from restarting on file uploads.

Bash

python app.py
(Note: If you didn't add use_reloader=False to app.py, use this command):

Bash

flask run --no-reload
Access the Web UI: Your terminal will show that the server is running. Open your web browser and go to:

http://127.0.0.1:5000

Analyze a Document: You can now upload a .pdf, .docx, or .txt file and click "Analyze Document" to see the extracted insights.