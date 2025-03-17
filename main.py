from flask import Flask, request, render_template, jsonify
from docai_processor import process_document
from gemini_processor import get_summary
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
            
        print("Starting Doc AI processing...")
        # Process with Doc AI
        try:
            doc_ai_results = process_document(file)
            print("Doc AI Results:", doc_ai_results)
        except Exception as e:
            print("Doc AI Error:", str(e))
            return jsonify({'error': f'Doc AI processing failed: {str(e)}'}), 500

        print("Starting Gemini processing...")
        # Need to seek to start of file as it was read in Doc AI
        file.seek(0)
        
        # Get Gemini summary
        try:
            summary = get_summary(file)
            print("Gemini Summary received")
        except Exception as e:
            print("Gemini Error:", str(e))
            return jsonify({'error': f'Gemini processing failed: {str(e)}'}), 500

        return render_template('result.html', 
                             extracted_data=doc_ai_results,
                             summary=summary)
                             
    except Exception as e:
        print("General Error:", str(e))
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
