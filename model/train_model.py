import os
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def load_sample_data():
    """
    For demonstration, create synthetic dataset.
    In a real project, you'd load real labeled data of phishing and legitimate URLs.
    """
    # Create synthetic data
    data = {
        'url_length': np.random.normal(25, 5, 500).tolist() + np.random.normal(75, 20, 500).tolist(),
        'domain_length': np.random.normal(10, 3, 500).tolist() + np.random.normal(20, 8, 500).tolist(),
        'dots_in_domain': np.random.randint(1, 3, 500).tolist() + np.random.randint(2, 6, 500).tolist(),
        'special_chars': np.random.randint(0, 5, 500).tolist() + np.random.randint(3, 15, 500).tolist(),
        'has_ip': [0] * 450 + [1] * 50 + [0] * 100 + [1] * 400,
        'is_shortened': [0] * 480 + [1] * 20 + [0] * 300 + [1] * 200,
        'http_in_domain': [0] * 490 + [1] * 10 + [0] * 250 + [1] * 250,
        'has_at_symbol': [0] * 495 + [1] * 5 + [0] * 300 + [1] * 200,
        'double_slash_in_path': [0] * 485 + [1] * 15 + [0] * 200 + [1] * 300,
        'subdomain_count': np.random.randint(0, 2, 500).tolist() + np.random.randint(1, 5, 500).tolist(),
        'suspicious_words': np.random.randint(0, 2, 500).tolist() + np.random.randint(1, 5, 500).tolist(),
        'domain_age': np.random.randint(100, 3000, 500).tolist() + np.random.randint(0, 100, 500).tolist()
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Add labels: 0 = legitimate, 1 = phishing
    df['is_phishing'] = [0] * 500 + [1] * 500
    
    return df

def train_model():
    """Train and save the phishing detection model."""
    # Create model directory if it doesn't exist
    if not os.path.exists('model'):
        os.makedirs('model')
    
    # Load data
    df = load_sample_data()
    
    # Split features and target
    X = df.drop('is_phishing', axis=1)
    y = df['is_phishing']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    print("Model Performance:")
    print(classification_report(y_test, y_pred))
    
    # Save the model
    with open('model/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print("Model trained and saved to 'model/model.pkl'")

if __name__ == "__main__":
    train_model()