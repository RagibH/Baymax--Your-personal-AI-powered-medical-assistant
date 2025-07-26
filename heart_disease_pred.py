# heart_disease_ui.py
# -----------------------------------------------
# Baymax UI page for Heart‑Disease prediction
# Author: Your‑Name‑Here
# Requires: PyQt5, pandas, joblib

import sys, os, joblib
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QPushButton, QRadioButton, QButtonGroup, QFormLayout, QMessageBox, QComboBox
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt


class HeartDiseasePredictionPage(QWidget):
    """
    Baymax page to predict Heart Disease using the classic
    UCI 14‑feature dataset (0 = no disease, 1 = disease).
    """
    def __init__(self, username="User"):
        super().__init__()
        self.username = username
        self.setWindowTitle("Heart Disease Prediction - Baymax")
        self.setGeometry(100, 100, 780, 720)
        self.setStyleSheet("background-color: #fdfefe;")
        self.setup_ui()
        self.load_model()

    # ───────────────────────────────────────────────────────────
    # UI
    # ───────────────────────────────────────────────────────────
    def setup_ui(self):
        main = QVBoxLayout()
        main.setContentsMargins(40, 20, 40, 20)

        # Header
        title = QLabel(f"Hello {self.username}!\nBaymax is here to predict Heart Disease")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #2e86c1;")
        title.setAlignment(Qt.AlignLeft)

        logo = QLabel()
        if os.path.exists("baymax.png"):
            logo.setPixmap(QPixmap("baymax.png").scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            logo.setText("❤️")
            logo.setFont(QFont("Segoe UI Emoji", 40))
        logo.setAlignment(Qt.AlignRight)

        header = QHBoxLayout()
        header.addWidget(title)
        header.addStretch()
        header.addWidget(logo)
        main.addLayout(header)

        # Form
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignLeft)

        # ─── Numeric helpers ────────────────────────────────
        def make_edit(phtext):
            e = QLineEdit(); e.setPlaceholderText(phtext); return e

        # age
        self.age_input = make_edit("e.g. 54")

        # sex (0 = Female, 1 = Male)
        self.sex_grp = QButtonGroup()
        self.sex_male   = QRadioButton("Male")
        self.sex_female = QRadioButton("Female")
        self.sex_male.setChecked(True)
        self.sex_grp.addButton(self.sex_female, 0)
        self.sex_grp.addButton(self.sex_male,   1)
        sex_box = QHBoxLayout(); sex_box.addWidget(self.sex_male); sex_box.addWidget(self.sex_female)

        # chest pain type (0–3)
        self.cp_combo = QComboBox()
        self.cp_combo.addItems([
            "0 – Typical angina",
            "1 – Atypical angina",
            "2 – Non‑anginal pain",
            "3 – Asymptomatic"
        ])

        # resting blood pressure
        self.trestbps_input = make_edit("e.g. 130")

        # cholesterol
        self.chol_input = make_edit("e.g. 246")

        # fasting blood sugar > 120 mg/dL (0/1)
        self.fbs_grp = QButtonGroup()
        self.fbs_no  = QRadioButton("≤ 120")
        self.fbs_yes = QRadioButton("> 120")
        self.fbs_no.setChecked(True)
        self.fbs_grp.addButton(self.fbs_no,  0)
        self.fbs_grp.addButton(self.fbs_yes, 1)
        fbs_box = QHBoxLayout(); fbs_box.addWidget(self.fbs_no); fbs_box.addWidget(self.fbs_yes)

        # resting ECG (0,1,2)
        self.restecg_combo = QComboBox()
        self.restecg_combo.addItems([
            "0 – Normal",
            "1 – ST‑T abnormality",
            "2 – Probable/Definite LVH"
        ])

        # max heart rate
        self.thalach_input = make_edit("e.g. 150")

        # exercise‑induced angina (0/1)
        self.exang_grp = QButtonGroup()
        self.exang_no  = QRadioButton("No")
        self.exang_yes = QRadioButton("Yes")
        self.exang_no.setChecked(True)
        self.exang_grp.addButton(self.exang_no,  0)
        self.exang_grp.addButton(self.exang_yes, 1)
        exang_box = QHBoxLayout(); exang_box.addWidget(self.exang_no); exang_box.addWidget(self.exang_yes)

        # oldpeak
        self.oldpeak_input = make_edit("e.g. 1.4")

        # slope (0‑2)
        self.slope_combo = QComboBox()
        self.slope_combo.addItems([
            "0 – Upsloping",
            "1 – Flat",
            "2 – Downsloping"
        ])

        # number of major vessels (0‑3)
        self.ca_combo = QComboBox()
        self.ca_combo.addItems([str(i) for i in range(4)])

        # thal (0 normal, 1 fixed, 2 reversible)
        self.thal_combo = QComboBox()
        self.thal_combo.addItems([
            "0 – Normal",
            "1 – Fixed defect",
            "2 – Reversible defect"
        ])

        # add to form
        form.addRow("Age:", self.age_input)
        form.addRow("Sex:", sex_box)
        form.addRow("Chest Pain Type:", self.cp_combo)
        form.addRow("Resting BP (trestbps):", self.trestbps_input)
        form.addRow("Cholesterol (chol):", self.chol_input)
        form.addRow("Fasting Blood Sugar:", fbs_box)
        form.addRow("Resting ECG:", self.restecg_combo)
        form.addRow("Max Heart Rate (thalach):", self.thalach_input)
        form.addRow("Exercise‑induced Angina:", exang_box)
        form.addRow("Oldpeak:", self.oldpeak_input)
        form.addRow("Slope:", self.slope_combo)
        form.addRow("Major Vessels (ca):", self.ca_combo)
        form.addRow("Thal:", self.thal_combo)

        # Predict button
        predict_btn = QPushButton("Predict Heart Disease")
        predict_btn.setStyleSheet("""
            QPushButton {
                background-color: #1abc9c;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 10px;
            }
            QPushButton:hover { background-color: #16a085; }
        """)
        predict_btn.clicked.connect(self.predict)

        main.addLayout(form)
        main.addWidget(predict_btn)
        self.setLayout(main)

    # ───────────────────────────────────────────────────────────
    # Model
    # ───────────────────────────────────────────────────────────
    def load_model(self):
        try:
            folder = os.path.dirname(os.path.abspath(__file__))
            bundle = joblib.load(os.path.join(folder, "heart_disease_model.joblib"))
            self.model     = bundle["model"]
            self.columns   = bundle["features"]        # original column order
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load model:\n{e}")
            self.model = None

    # ───────────────────────────────────────────────────────────
    # Prediction
    # ───────────────────────────────────────────────────────────
    def predict(self):
        try:
            if self.model is None:
                raise RuntimeError("Model not loaded.")

            # Collect inputs
            row = {
                "age":        float(self.age_input.text()),
                "sex":        self.sex_grp.checkedId(),
                "cp":         self.cp_combo.currentIndex(),
                "trestbps":   float(self.trestbps_input.text()),
                "chol":       float(self.chol_input.text()),
                "fbs":        self.fbs_grp.checkedId(),
                "restecg":    self.restecg_combo.currentIndex(),
                "thalach":    float(self.thalach_input.text()),
                "exang":      self.exang_grp.checkedId(),
                "oldpeak":    float(self.oldpeak_input.text()),
                "slope":      self.slope_combo.currentIndex(),
                "ca":         int(self.ca_combo.currentText()),
                "thal":       self.thal_combo.currentIndex()
            }

            # Build DataFrame in original training column order
            X = pd.DataFrame([[row[c] for c in self.columns]], columns=self.columns)

            pred = int(self.model.predict(X)[0])
            prob = self.model.predict_proba(X)[0, 1]

            if pred == 1:
                msg = f"⚠️ High risk of Heart Disease (probability {prob:.2%})"
            else:
                msg = f"✅ Low risk of Heart Disease (probability {prob:.2%})"

            QMessageBox.information(self, "Prediction Result", msg)

        except ValueError as ve:
            QMessageBox.warning(self, "Input Error", f"Check your inputs:\n{ve}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Something went wrong:\n{e}")


# ─────────────────────────────────────────────────────────────
# Stand‑alone launch
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = HeartDiseasePredictionPage(username="Ragib")
    wnd.show()
    sys.exit(app.exec_())
