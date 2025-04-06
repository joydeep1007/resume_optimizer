from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from parser import parse_resume
from analyzer import analyze_resume
from utils import format_resume_data, validate_resume_data, save_analysis_results, format_analysis_results

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

# Create uploads and analysis_results directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'analysis_results'), exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Parse and analyze the resume
            resume_data = parse_resume(filepath)
            formatted_data = format_resume_data(resume_data)
            validate_resume_data(formatted_data)
            
            analysis_results = analyze_resume(formatted_data)
            save_analysis_results(analysis_results)
            
            # Format results for display
            display_results = format_analysis_results(analysis_results)
            
            # Clean up the uploaded file
            os.remove(filepath)
            
            return jsonify(display_results)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)