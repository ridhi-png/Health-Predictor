# 🏥 HealthTracker

![HealthTracker](https://img.shields.io/badge/HealthTracker-Interactive%20Dashboard-blue?style=for-the-badge)  
**Created with ❤️ by [Ridhi](https://github.com/ridhi-png)**

A smart and interactive health tracking web application to monitor patient symptoms, predict diseases, and visualize health trends.

---

## 🚀 Key Features

- **🧑‍⚕️ Patient Management**: Store patient info and medical history securely  
- **🤒 Symptom Tracking**: Catalog symptoms with severity levels  
- **🩺 Disease Predictions**: Identify health conditions with descriptions and remedies  
- **📊 Interactive Reports**: Generate detailed health reports with predictions  
- **📈 Dashboard Analytics**: Visualize health metrics and trends using interactive charts  

---

## 💻 Technologies Used

| Layer | Technology |
|-------|------------|
| Backend | Django, Python |
| Frontend | HTML, CSS, JavaScript, Bootstrap |
| Data Visualization | Chart.js |
| Database | SQLite (development), PostgreSQL (production) |

---

## 🎨 Dashboard Preview

![Dashboard Preview](https://img.shields.io/badge/Dashboard-Interactive-green?style=for-the-badge)  

- Live charts & graphs for patient health trends  
- Easy navigation through symptoms and reports  
- Quick insights with color-coded metrics  

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.x  
- Django 4.x  
- Node.js & npm (optional for frontend dependencies)  

### Installation

```bash
# Clone the repository
git clone https://github.com/ridhi-png/HealthTracker.git
cd HealthTracker

# Create virtual environment
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Start the server
python manage.py runserver
