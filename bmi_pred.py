# bmi_ui.py
# ------------------------------------------------------------
# Baymax BMI‑category prediction page
# Requires: PyQt5, pandas, numpy, joblib

import sys, os, joblib
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QPushButton, QRadioButton, QButtonGroup, QFormLayout, QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt


class BMIPredictionPage(QWidget):
    """
    Predicts BMI class:
        0 Extremely Weak · 1 Weak · 2 Normal · 3 Overweight · 4 Obesity · 5 Extreme Obesity
    Features: Gender (0 Female/1 Male), Height (cm), Weight (kg)
    """
    CLASS_LABELS = [
        "Extremely Weak",
        "Weak",
        "Normal",
        "Overweight",
        "Obesity",
        "Extreme Obesity"
    ]

    def __init__(self, username="User"):
        super().__init__()
        self.username = username
        self.setWindowTitle("BMI Prediction - Baymax")
        self.setGeometry(120, 120, 640, 520)
        self.setStyleSheet("background-color: #fdfefe;")
        self._build_ui()
        self._load_model()

    # ───────────────────────────────────────────────────────────
    # UI
    # ───────────────────────────────────────────────────────────
    def _build_ui(self):
        main = QVBoxLayout(); main.setContentsMargins(40, 20, 40, 20)

        # Header
        title = QLabel(f"Hello {self.username}!\nBaymax is here to estimate your BMI class")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #2e86c1;")
        title.setAlignment(Qt.AlignLeft)

        logo = QLabel()
        if os.path.exists("baymax.png"):
            logo.setPixmap(QPixmap("baymax.png").scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            logo.setText("⚖️")
            logo.setFont(QFont("Segoe UI Emoji", 40))
        logo.setAlignment(Qt.AlignRight)

        header = QHBoxLayout()
        header.addWidget(title); header.addStretch(); header.addWidget(logo)
        main.addLayout(header)

        # Form
        form = QFormLayout(); form.setLabelAlignment(Qt.AlignLeft)

        # Gender radio buttons (Female 0 / Male 1)
        self.gender_grp = QButtonGroup()
        self.gender_male   = QRadioButton("Male");   self.gender_grp.addButton(self.gender_male, 1)
        self.gender_female = QRadioButton("Female"); self.gender_grp.addButton(self.gender_female, 0)
        self.gender_male.setChecked(True)
        gbox = QHBoxLayout(); gbox.addWidget(self.gender_male); gbox.addWidget(self.gender_female)
        form.addRow("Gender:", gbox)

        # Height & Weight inputs
        self.height_edit = QLineEdit(); self.height_edit.setPlaceholderText("cm e.g. 170")
        self.weight_edit = QLineEdit(); self.weight_edit.setPlaceholderText("kg e.g. 65")
        form.addRow("Height (cm):", self.height_edit)
        form.addRow("Weight (kg):", self.weight_edit)

        # Predict button
        predict_btn = QPushButton("Predict BMI Category")
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
        predict_btn.clicked.connect(self._predict)

        main.addLayout(form)
        main.addWidget(predict_btn)
        self.setLayout(main)

    # ───────────────────────────────────────────────────────────
    # Load Model
    # ───────────────────────────────────────────────────────────
    def _load_model(self):
        try:
            bundle = joblib.load(os.path.join(os.path.dirname(__file__), "bmi_model_prediction.joblib"))
            self.model    = bundle["model"]
            self.features = bundle["features"]      # ["Gender","Height","Weight"]
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load model:\n{e}")
            self.model = None

    # ───────────────────────────────────────────────────────────
    # Predict
    # ───────────────────────────────────────────────────────────
    def _predict(self):
        try:
            if self.model is None:
                raise RuntimeError("Model not loaded.")

            gender  = self.gender_grp.checkedId()
            height  = float(self.height_edit.text())
            weight  = float(self.weight_edit.text())

            X = pd.DataFrame([[gender, height, weight]], columns=self.features)

            pred = int(self.model.predict(X)[0])
            proba = self.model.predict_proba(X)[0, pred]

            label = self.CLASS_LABELS[pred]
            QMessageBox.information(
                self, "BMI Prediction",
                f"Predicted category: <b>{label}</b><br/>Probability: {proba:.2%}"
            )

        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numerical values for height and weight.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Something went wrong:\n{e}")


# ─────────────────────────────────────────────────────────────
# Stand‑alone launcher
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = BMIPredictionPage(username="Ragib")
    wnd.show()
    sys.exit(app.exec_())
