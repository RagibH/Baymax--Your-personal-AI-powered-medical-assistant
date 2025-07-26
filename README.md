# BayMax - Your Personal AI-Powered Medical Assistant 🤖💊

**BayMax** is an AI-powered healthcare companion that provides medical predictions, emergency assistance, and health monitoring—all in one desktop application.

---

## 📦 Prerequisites

- Python 3.8+
- pip package manager
- MySQL (via XAMPP/phpMyAdmin or any other setup)

---

## 🔗 Download Required Model Files

Due to GitHub file size limitations, please download the following essential model files manually:

👉 [Diabetes and Prescription Models (Google Drive)](https://drive.google.com/drive/folders/1eDj2H9Xo3ahAcJeAbbO-78dEhEX9fGp_?usp=drive_link)

Place the downloaded models in the correct directories as specified in the project.

---

## 🛠 Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/baymax-medical-assistant.git
   cd baymax-medical-assistant
2. Create a virtual environment and activate it:
   ```bash
    python -m venv venv
    source venv/bin/activate     # For Linux/macOS
    venv\Scripts\activate        # For Windows
3. Install dependencies:
   ```bash
   pip install -r requirements.txt

❗ Excluded from Repository
The following files and folders are excluded and should be generated or configured locally:

__pycache__/ - Python cache files (auto-generated)

venv/ - Your virtual environment

.env - Environment variables (create your own for DB connection)

🏥 Available Features
  ✅ BMI Prediction
  
  ✅ Diabetes Risk Assessment
  
  ✅ Heart Disease Prediction
  
  ✅ Liver Disease Analysis
  
  ✅ Emergency Assistance
  
  ✅ Handwritten Medicine Detection from Prescriptions
  
  ✅ First Aid Chatbot
  
  ✅ Emergency Directory (Doctor Contacts)

 Notes:
Ensure your MySQL server is running before launching the application.

Models must be downloaded and placed in their respective folders to avoid loading issues.

All user-related data will be stored in the connected MySQL database.



📧 Contact
For queries, suggestions, or support, feel free to reach out or raise an issue in the repository. or mail: ragibhasansec@gmail.com
