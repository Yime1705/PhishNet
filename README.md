# 🔐 Phishing URL Detection Web App

A full-stack phishing URL detection system using machine learning. This app analyzes URLs to determine if they are likely phishing attempts, then stores and displays past predictions for user reference.

---

## 🚀 Features

- ✅ URL safety check using trained ML model  
- 📊 Confidence score for predictions  
- 🗂️ History of scanned URLs stored in SQLite  
- 💡 Real-time result display  
- 🌐 Built with Flask, HTML, CSS, and JavaScript  

---

## 🧠 Machine Learning

- Model trained using `train_model.py`
- Feature extraction handled in `features.py`
- Serialized model stored as `model.pkl`

---

## 🗂️ Project Structure

```bash
PHISHING-DETECTION/
│
├── app.py                 # Flask app main file
├── db_setup.py           # DB initialization script
├── hello.py              # Test or auxiliary route
├── requirements.txt      # Python dependencies
│
├── data/
│   └── phishing_db.sqlite    # SQLite DB storing scan history
│
├── model/
│   ├── model.pkl             # Trained ML model
│   ├── features.py           # URL feature extraction
│   └── train_model.py        # Model training script
│
├── static/               # Static assets (CSS, JS)
│
├── templates/
│   ├── index.html        # Main input form
│   └── results.html      # Results display
│
└── .venv/                # Python virtual environment

yaml
Copy
Edit

---

## 💻 Installation & Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/phishing-detection.git
   cd phishing-detection
Create a virtual environment:

bash
Copy
Edit
python -m venv .venv
Activate the environment:

On Windows:

bash
Copy
Edit
.venv\Scripts\activate
On macOS/Linux:

bash
Copy
Edit
source .venv/bin/activate
Install the dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Set up the database:

bash
Copy
Edit
python db_setup.py
Run the app:

bash
Copy
Edit
python app.py
Open in your browser:
Visit http://localhost:5000

🧪 Example Usage
Enter a URL like http://example.com/login.php

Hit "Check"

The app will display:

✅ Prediction (Safe / Potential Phishing)

📊 Confidence level

🗂️ Scan history in a table

🛠 Tech Stack
Backend: Python, Flask

Frontend: HTML, CSS, JavaScript

Machine Learning: Scikit-learn

Database: SQLite

📌 To Do
 Add user authentication

 Export scan history as CSV

 Improve ML model accuracy

 Add REST API endpoint

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

