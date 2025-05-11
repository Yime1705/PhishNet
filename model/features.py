import re
import numpy as np
import tld
import urllib.parse
import whois
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import socket

def extract_features(url):
    """Extract features from a URL for phishing detection."""
    features = {}
    
    # Safely parse the URL
    try:
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc
    except:
        domain = ""
    
    # 1. URL length (phishing URLs are often longer)
    features['url_length'] = len(url)
    
    # 2. Domain length
    features['domain_length'] = len(domain)
    
    # 3. Number of dots in domain (more dots often indicate phishing)
    features['dots_in_domain'] = domain.count('.')
    
    # 4. Number of special characters
    features['special_chars'] = len(re.findall(r'[^a-zA-Z0-9.]', url))
    
    # 5. Contains IP address instead of domain
    features['has_ip'] = 1 if re.search(
        r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5]))',
        url
    ) else 0
    
    # 6. Uses URL shortening service
    shortening_services = ['bit.ly', 'goo.gl', 't.co', 'tinyurl', 'is.gd']
    features['is_shortened'] = 1 if any(service in domain for service in shortening_services) else 0
    
    # 7. Contains 'http' in domain part (suspicious)
    features['http_in_domain'] = 1 if 'http' in domain else 0
    
    # 8. URL contains '@' symbol (suspicious)
    features['has_at_symbol'] = 1 if '@' in url else 0
    
    # 9. URL contains '//' in path (might be an attempt to confuse)
    features['double_slash_in_path'] = 1 if '//' in parsed_url.path else 0
    
    # 10. Number of subdomains
    if domain:
        features['subdomain_count'] = domain.count('.') 
    else:
        features['subdomain_count'] = 0
    
    # 11. Contains suspicious words
    suspicious_words = ['secure', 'account', 'webscr', 'login', 'banking', 'confirm', 'verify', 'signin']
    features['suspicious_words'] = sum(1 for word in suspicious_words if word in url.lower())
    
    # Try to get additional features that require external requests - these may fail
    try:
        # 12. Domain age in days (if available)
        try:
            w = whois.whois(domain)
            if w.creation_date:
                if isinstance(w.creation_date, list):
                    creation_date = w.creation_date[0]
                else:
                    creation_date = w.creation_date
                
                domain_age = (datetime.now() - creation_date).days
                features['domain_age'] = domain_age
            else:
                features['domain_age'] = -1  # Unable to determine
        except:
            features['domain_age'] = -1  # Error or unavailable
    
    except:
        features['domain_age'] = -1
    
    # Return features as a dictionary for flexibility
    return features

def convert_features_to_vector(features_dict):
    """Convert features dictionary to a numerical vector for ML model."""
    # Define the order of features for consistent vectors
    feature_order = [
        'url_length', 'domain_length', 'dots_in_domain', 'special_chars', 
        'has_ip', 'is_shortened', 'http_in_domain', 'has_at_symbol',
        'double_slash_in_path', 'subdomain_count', 'suspicious_words',
        'domain_age'
    ]
    
    # Create the vector with each feature in the right position
    vector = []
    for feature in feature_order:
        if feature in features_dict:
            vector.append(features_dict[feature])
        else:
            vector.append(0)  # Default value if feature is missing
    
    return np.array(vector).reshape(1, -1)  # Reshape for scikit-learn
