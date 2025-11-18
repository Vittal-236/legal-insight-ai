import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import time

# Import our existing modules
from text_extractor import extract_text_from_file
from nlu_service import analyze_legal_text
from parser import parse_nlu_response

# --- CONFIGURATION ---
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- ROUTES ---

@app.route('/')
def index():
    """
    Serves the main HTML page (our frontend UI).
    """
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_document():
    """
    This is the API endpoint that the frontend will call.
    It handles the file upload, processing, and returns the JSON result.
    """
    # 1. Check if a file was sent
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        # Save the file temporarily
        temp_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(temp_filepath)
        
        print(f"Processing file: {temp_filepath}")

        try:
            # 2. Extract Text (using our existing module)
            text = extract_text_from_file(temp_filepath)
            if not text:
                return jsonify({"error": "Could not extract text from file."}), 400

            # 3. Analyze Text (using our existing module)
            nlu_response = analyze_legal_text(text)
            if not nlu_response:
                return jsonify({"error": "NLU analysis failed."}), 500

            # 4. Parse Results (using our existing module)
            structured_data = parse_nlu_response(nlu_response, filename)

            # 5. Clean up the temporary file
            os.remove(temp_filepath)

            # 6. Send the JSON result back to the frontend
            return jsonify(structured_data)

        except Exception as e:
            # Clean up even if there's an error
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)
            print(f"Error during analysis: {e}")
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False) # Runs the server on http://127.0.0.1:5000