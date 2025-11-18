import pdfplumber
import docx2txt
import os

def extract_text_from_file(filepath):
    """
    Extracts clean text from .pdf, .docx, or .txt files.
    """
    _, file_extension = os.path.splitext(filepath)
    text = ""

    try:
        if file_extension == '.pdf':
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            print(f"Successfully extracted text from PDF: {filepath}")

        elif file_extension == '.docx':
            text = docx2txt.process(filepath)
            print(f"Successfully extracted text from DOCX: {filepath}")

        elif file_extension == '.txt':
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            print(f"Successfully extracted text from TXT: {filepath}")

        else:
            print(f"Warning: Unsupported file type: {file_extension}. Skipping file: {filepath}")
            return None

        return text.strip()

    except Exception as e:
        print(f"Error extracting text from {filepath}: {e}")
        return None