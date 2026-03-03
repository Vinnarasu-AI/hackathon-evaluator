from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
import sys
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Add current directory to path
from github_cloner import clone_repository, get_files_to_scan
from evaluator import evaluate_project

app = Flask(__name__)
CORS(app, origins=['http://localhost:8000', 'http://127.0.0.1:8000', 'http://localhost:5000'])

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
VECTOR_DB_DIR = os.path.join(DATA_DIR, 'vector_db')
TEMP_DIR = os.path.join(DATA_DIR, 'temp')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# Ensure directories exist
os.makedirs('uploads', exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(VECTOR_DB_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Add logging to file
import logging
logging.basicConfig(
    filename=os.path.join(LOGS_DIR, 'backend.log'),
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy", 
        "message": "Server is running",
        "ollama_models": check_ollama_models()
    })

def check_ollama_models():
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            return [m['name'] for m in models]
    except:
        return []
    return []

@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    try:
        data = request.json
        github_url = data.get('github_url')
        
        if not github_url:
            return jsonify({"error": "GitHub URL is required"}), 400
        
        print(f"Received evaluation request for: {github_url}")
        
        # Step 1: Clone repository
        repo_path = clone_repository(github_url)
        print(f"Repository cloned to: {repo_path}")
        
        # Step 2-11: Run full evaluation
        results = evaluate_project(repo_path)
        
        if "error" in results:
            print(f"Evaluation error: {results['error']}")
            return jsonify(results), 500
            
        # Save results using absolute paths
        results_file = os.path.join(TEMP_DIR, 'latest_results.json')
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Evaluation complete for {github_url}. Results saved.")
        return jsonify(results)
    
    except Exception as e:
        error_msg = str(e)
        stack_trace = traceback.format_exc()
        logger.error(f"CRITICAL ERROR: {error_msg}")
        logger.error(stack_trace)
        print(f"CRITICAL ERROR: {error_msg}")
        print(stack_trace)
        return jsonify({
            "error": error_msg,
            "trace": stack_trace
        }), 500

@app.route('/api/results/latest_results.json', methods=['GET'])
def get_latest_results():
    try:
        results_path = os.path.join(TEMP_DIR, 'latest_results.json')
        if os.path.exists(results_path):
            return send_file(results_path, mimetype='application/json')
        else:
            return jsonify({"error": "No results found"}), 404
    except Exception as e:
        logger.error(f"Error fetching latest results: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Force single-threaded to see output clearly in console
    app.run(debug=True, port=5000, host='0.0.0.0', threaded=False)