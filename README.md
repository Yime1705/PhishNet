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


---

## 💻 Installation & Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/phishing-detection.git
   cd phishing-detection
