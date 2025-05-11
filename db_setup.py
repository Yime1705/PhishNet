import sqlite3
import os

def setup_database():
    """Create the SQLite database and tables if they don't exist."""
    # Check if database directory exists, create it if not
    if not os.path.exists('data'):
        os.makedirs('data')
    
    conn = sqlite3.connect('data/phishing_db.sqlite')
    cursor = conn.cursor()
    
    # Create URLs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL,
        is_phishing BOOLEAN,
        confidence FLOAT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        features TEXT
    )
    ''')
    
    # Create a table for feedback
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url_id INTEGER,
        correct BOOLEAN,
        notes TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (url_id) REFERENCES urls (id)
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()