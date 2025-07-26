import sys
import os
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QPushButton, QRadioButton, QButtonGroup, QFormLayout, QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import joblib
import db_utils



class DiabetesPredictionPage(QWidget):
    def __init__(self, username="User", user_id=None):
        super().__init__()
        self.username = username
        self.user_id  = user_id 
        self.setWindowTitle("Diabetes Prediction - Baymax")
        self.setGeometry(100, 100, 720, 620)
        self.setStyleSheet("background-color: #fdfefe;")
        self.setup_ui()
        self.load_model()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 20, 40, 20)

        # Title & Logo
        title = QLabel(f"Hello {self.username}!\nBaymax is here to predict Diabetes")
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

        # Form
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)

        # Gender
        self.gender_group = QButtonGroup()
        self.gender_male = QRadioButton("Male")
        self.gender_female = QRadioButton("Female")
        self.gender_male.setChecked(True)
        self.gender_group.addButton(self.gender_male, 1)
        self.gender_group.addButton(self.gender_female, 0)
        gender_layout = QHBoxLayout()
        gender_layout.addWidget(self.gender_male)
        gender_layout.addWidget(self.gender_female)
        form_layout.addRow("Gender:", gender_layout)

        # Age
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Enter Age")
        form_layout.addRow("Age:", self.age_input)

        # Hypertension
        self.hypertension_group = QButtonGroup()
        self.hypertension_yes = QRadioButton("Yes")
        self.hypertension_no = QRadioButton("No")
        self.hypertension_no.setChecked(True)
        self.hypertension_group.addButton(self.hypertension_yes, 1)
        self.hypertension_group.addButton(self.hypertension_no, 0)
        hypertension_layout = QHBoxLayout()
        hypertension_layout.addWidget(self.hypertension_yes)
        hypertension_layout.addWidget(self.hypertension_no)
        form_layout.addRow("Hypertension:", hypertension_layout)

        # Heart Disease
        self.heart_group = QButtonGroup()
        self.heart_yes = QRadioButton("Yes")
        self.heart_no = QRadioButton("No")
        self.heart_no.setChecked(True)
        self.heart_group.addButton(self.heart_yes, 1)
        self.heart_group.addButton(self.heart_no, 0)
        heart_layout = QHBoxLayout()
        heart_layout.addWidget(self.heart_yes)
        heart_layout.addWidget(self.heart_no)
        form_layout.addRow("Heart Disease:", heart_layout)

        # Smoking History
        self.smoking_group = QButtonGroup()
        self.smoking_yes = QRadioButton("Yes")
        self.smoking_no = QRadioButton("No")
        self.smoking_no.setChecked(True)
        self.smoking_group.addButton(self.smoking_yes, 1)
        self.smoking_group.addButton(self.smoking_no, 0)
        smoking_layout = QHBoxLayout()
        smoking_layout.addWidget(self.smoking_yes)
        smoking_layout.addWidget(self.smoking_no)
        form_layout.addRow("Smoking History:", smoking_layout)

        # BMI
        self.bmi_input = QLineEdit()
        self.bmi_input.setPlaceholderText("Enter BMI")
        form_layout.addRow("BMI:", self.bmi_input)

        # HbA1c
        self.hba1c_input = QLineEdit()
        self.hba1c_input.setPlaceholderText("Enter HbA1c Level")
        form_layout.addRow("HbA1c Level:", self.hba1c_input)

        # Glucose
        self.glucose_input = QLineEdit()
        self.glucose_input.setPlaceholderText("Enter Blood Glucose Level")
        form_layout.addRow("Blood Glucose Level:", self.glucose_input)

        # Predict Button
        predict_btn = QPushButton("Predict Diabetes")
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
        predict_btn.clicked.connect(self.predict_diabetes)

        main_layout.addLayout(form_layout)
        main_layout.addWidget(predict_btn)
        self.setLayout(main_layout)

    def load_model(self):
        try:
            folder = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(folder, "diabetes_model.joblib")
            self.model = joblib.load(model_path, mmap_mode=None)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"⚠️ Failed to load model:\n{str(e)}")
            self.model = None

    def predict_diabetes(self):
        try:
            if self.model is None:
                raise ValueError("ML Model is not loaded.")

            gender        = self.gender_group.checkedId()
            age           = float(self.age_input.text())
            hypertension  = self.hypertension_group.checkedId()
            heart_disease = self.heart_group.checkedId()
            smoking       = self.smoking_group.checkedId()
            bmi           = float(self.bmi_input.text())
            hba1c         = float(self.hba1c_input.text())
            glucose       = float(self.glucose_input.text())

            input_data = np.array([[gender, age, hypertension, heart_disease,
                                    smoking, bmi, hba1c, glucose]])

            prediction = int(self.model.predict(input_data)[0])

            # Optional probability (comment out if model has no predict_proba)
            conf = float(self.model.predict_proba(input_data)[0, prediction]) * 100

            msg = ("✅ Diabetes Detected" if prediction == 1
                else "🟢 No Diabetes Detected")
            QMessageBox.information(self, "Prediction Result", f"{msg} ({conf:.1f}%)")

            # ── Save to DB ───────────────────────────────────────────
            if self.user_id:
                print("Saving prediction to DB for user:", self.user_id)
                db_utils.save_result("diabetes_results", {
                    "user_id": self.user_id,
                    "gender": gender,
                    "age": age,
                    "hypertension": hypertension,
                    "heart_disease": heart_disease,
                    "smoking": smoking,
                    "bmi": bmi,
                    "hba1c": hba1c,
                    "glucose": glucose,
                    "prediction": int(prediction),
                    "ts": "CURRENT_TIMESTAMP()"
                })
                print("Save function called.")


        except Exception as e:
            QMessageBox.warning(self, "Input Error",
                                f"❌ Please check your input:\n{str(e)}")

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiabetesPredictionPage(username="Ragib")
    window.show()
    sys.exit(app.exec_())
