import sys
import os
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QPushButton, QRadioButton, QButtonGroup, QFormLayout, QMessageBox, QComboBox
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import joblib


class LiverDiseasePredictionPage(QWidget):
    """
    A Baymax UI page that predicts Liver Disease from 10 inputs:

        Age, Gender, BMI, Alcohol Consumption, Smoking, Genetic Risk,
        Physical Activity, Diabetes, Hypertension, Liver Function Test
    """
    def __init__(self, username="User"):
        super().__init__()
        self.username = username
        self.setWindowTitle("Liver Disease Prediction - Baymax")
        self.setGeometry(100, 100, 760, 680)
        self.setStyleSheet("background-color: #fdfefe;")
        self.setup_ui()
        self.load_model()

    # ───────────────────────────────────────────────────────────
    # UI construction
    # ───────────────────────────────────────────────────────────
    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 20, 40, 20)

        # Header – title + logo
        title = QLabel(f"Hello {self.username}!\nBaymax is here to predict Liver Disease")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #2e86c1;")
        title.setAlignment(Qt.AlignLeft)

        logo = QLabel()
        if os.path.exists("baymax.png"):
            pixmap = QPixmap("baymax.png")
            logo.setPixmap(pixmap.scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            logo.setText("🩺")
            logo.setFont(QFont("Segoe UI Emoji", 40))
        logo.setAlignment(Qt.AlignRight)

        header = QHBoxLayout()
        header.addWidget(title)
        header.addStretch()
        header.addWidget(logo)
        main_layout.addLayout(header)

        # Form – all 10 inputs
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)

        # Gender (0 = Male, 1 = Female)
        self.gender_group = QButtonGroup()
        self.gender_male = QRadioButton("Male")
        self.gender_female = QRadioButton("Female")
        self.gender_male.setChecked(True)
        self.gender_group.addButton(self.gender_male, 0)
        self.gender_group.addButton(self.gender_female, 1)
        gender_layout = QHBoxLayout()
        gender_layout.addWidget(self.gender_male)
        gender_layout.addWidget(self.gender_female)
        form_layout.addRow("Gender:", gender_layout)

        # Age
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("e.g. 45")
        form_layout.addRow("Age:", self.age_input)

        # BMI
        self.bmi_input = QLineEdit()
        self.bmi_input.setPlaceholderText("e.g. 27.5")
        form_layout.addRow("BMI:", self.bmi_input)

        # Alcohol Consumption (units/week)
        self.alcohol_input = QLineEdit()
        self.alcohol_input.setPlaceholderText("e.g. 5")
        form_layout.addRow("Alcohol (units/wk):", self.alcohol_input)

        # Smoking (0 = No, 1 = Yes)
        self.smoking_group = QButtonGroup()
        self.smoking_no = QRadioButton("No")
        self.smoking_yes = QRadioButton("Yes")
        self.smoking_no.setChecked(True)
        self.smoking_group.addButton(self.smoking_no, 0)
        self.smoking_group.addButton(self.smoking_yes, 1)
        smoking_layout = QHBoxLayout()
        smoking_layout.addWidget(self.smoking_no)
        smoking_layout.addWidget(self.smoking_yes)
        form_layout.addRow("Smoking:", smoking_layout)

        # Genetic Risk (0 = Low, 1 = Medium, 2 = High)
        self.risk_combo = QComboBox()
        self.risk_combo.addItems(["Low", "Medium", "High"])
        form_layout.addRow("Genetic Risk:", self.risk_combo)

        # Physical Activity (hrs/week)
        self.activity_input = QLineEdit()
        self.activity_input.setPlaceholderText("e.g. 3")
        form_layout.addRow("Physical Activity (hrs/wk):", self.activity_input)

        # Diabetes (0 = No, 1 = Yes)
        self.diabetes_group = QButtonGroup()
        self.diabetes_no = QRadioButton("No")
        self.diabetes_yes = QRadioButton("Yes")
        self.diabetes_no.setChecked(True)
        self.diabetes_group.addButton(self.diabetes_no, 0)
        self.diabetes_group.addButton(self.diabetes_yes, 1)
        diabetes_layout = QHBoxLayout()
        diabetes_layout.addWidget(self.diabetes_no)
        diabetes_layout.addWidget(self.diabetes_yes)
        form_layout.addRow("Diabetes:", diabetes_layout)

        # Hypertension (0 = No, 1 = Yes)
        self.hypertension_group = QButtonGroup()
        self.hypertension_no = QRadioButton("No")
        self.hypertension_yes = QRadioButton("Yes")
        self.hypertension_no.setChecked(True)
        self.hypertension_group.addButton(self.hypertension_no, 0)
        self.hypertension_group.addButton(self.hypertension_yes, 1)
        hypertension_layout = QHBoxLayout()
        hypertension_layout.addWidget(self.hypertension_no)
        hypertension_layout.addWidget(self.hypertension_yes)
        form_layout.addRow("Hypertension:", hypertension_layout)

        # Liver Function Test value
        self.lft_input = QLineEdit()
        self.lft_input.setPlaceholderText("e.g. 55")
        form_layout.addRow("Liver Function Test:", self.lft_input)

        # Predict Button
        predict_btn = QPushButton("Predict Liver Disease")
        predict_btn.setStyleSheet("""
            QPushButton {
                background-color: #1abc9c;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #16a085;
            }
        """)
        predict_btn.clicked.connect(self.predict_liver_disease)

        main_layout.addLayout(form_layout)
        main_layout.addWidget(predict_btn)
        self.setLayout(main_layout)

    # ───────────────────────────────────────────────────────────
    # Model loading
    # ───────────────────────────────────────────────────────────
    def load_model(self):
        try:
            folder = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(folder, "liver_disease_model.joblib")
            self.model = joblib.load(model_path, mmap_mode=None)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"⚠️ Failed to load model:\n{str(e)}")
            self.model = None

    # ───────────────────────────────────────────────────────────
    # Prediction
    # ───────────────────────────────────────────────────────────
    def predict_liver_disease(self):
        try:
            if self.model is None:
                raise ValueError("ML model not loaded.")

            gender = self.gender_group.checkedId()
            age = float(self.age_input.text())
            bmi = float(self.bmi_input.text())
            alcohol = float(self.alcohol_input.text())
            smoking = self.smoking_group.checkedId()
            genetic_risk = self.risk_combo.currentIndex()      # 0/1/2
            activity = float(self.activity_input.text())
            diabetes = self.diabetes_group.checkedId()
            hypertension = self.hypertension_group.checkedId()
            lft = float(self.lft_input.text())

            # Order must exactly match training feature order
            features = np.array([[
                age, gender, bmi, alcohol, smoking, genetic_risk,
                activity, diabetes, hypertension, lft
            ]])

            pred = self.model.predict(features)[0]
            msg = "⚠️ Possible Liver Disease Detected" if pred == 1 else "✅ Likely Healthy Liver"
            QMessageBox.information(self, "Prediction Result", msg)

        except ValueError as ve:
            QMessageBox.warning(self, "Input Error", f"Please enter valid numbers:\n{ve}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Something went wrong:\n{e}")


# ───────────────────────────────────────────────────────────────
# Launch for standalone testing
# ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LiverDiseasePredictionPage(username="Ragib")
    window.show()
    sys.exit(app.exec_())
