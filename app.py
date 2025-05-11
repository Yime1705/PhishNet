from flask import Flask, render_template, request, jsonify
import pickle
import json
import sqlite3
from datetime import datetime
import os

# Import our modules
from model.features import extract_features, convert_features_to_vector
from db_setup import setup_database

app = Flask(__name__)

# Ensure the model directory exists
if not os.path.exists('model'):
    os.makedirs('model')

# Check if model exists, if not train it
if not os.path.exists('model/model.pkl'):
    from model.train_model import train_model
    train_model()

# Load the model
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_url():
    """Analyze a URL for phishing indicators."""
    data = request.get_json()
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Extract features
    features = extract_features(url)
    
    # Convert to format for ML model
    feature_vector = convert_features_to_vector(features)
    
    # Make prediction
    prediction = model.predict(feature_vector)[0]
    confidence = model.predict_proba(feature_vector)[0][prediction]
    
    # Store in database
    conn = sqlite3.connect('data/phishing_db.sqlite')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO urls (url, is_phishing, confidence, features) VALUES (?, ?, ?, ?)",
        (url, bool(prediction), float(confidence), json.dumps(features))
    )
    url_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    # Return result
    result = {
        'url': url,
        'is_phishing': bool(prediction),
        'confidence': float(confidence),
        'features': features,
        'url_id': url_id
    }
    
    return jsonify(result)

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    """Allow users to submit feedback on predictions."""
    data = request.get_json()
    url_id = data.get('url_id')
    correct = data.get('correct')
    notes = data.get('notes', '')
    
    if url_id is None or correct is None:
        return jsonify({'error': 'URL ID and correctness feedback are required'}), 400
    
    # Store feedback
    conn = sqlite3.connect('data/phishing_db.sqlite')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO feedback (url_id, correct, notes) VALUES (?, ?, ?)",
        (url_id, bool(correct), notes)
    )
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/history', methods=['GET'])
def get_history():
    """Get history of analyzed URLs."""
    conn = sqlite3.connect('data/phishing_db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, url, is_phishing, confidence, timestamp FROM urls ORDER BY timestamp DESC LIMIT 100"
    )
    rows = cursor.fetchall()
    history = [dict(row) for row in rows]
    conn.close()
    
    return jsonify(history)

@app.route('/results/<int:url_id>')
def view_results(url_id):
    """Show detailed results for a specific URL."""
    conn = sqlite3.connect('data/phishing_db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get URL info
    cursor.execute("SELECT * FROM urls WHERE id = ?", (url_id,))
    url_info = dict(cursor.fetchone())
    
    # Get feedback if any
    cursor.execute("SELECT * FROM feedback WHERE url_id = ?", (url_id,))
    feedback = cursor.fetchone()
    if feedback:
        feedback = dict(feedback)
    
    conn.close()
    
    # Parse the features
    url_info['features'] = json.loads(url_info['features'])
    
    return render_template('results.html', url_info=url_info, feedback=feedback)

if __name__ == '__main__':
    # Make sure database is set up
    setup_database()
    
    # Start the Flask app
    app.run(debug=True)