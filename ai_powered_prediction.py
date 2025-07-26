# ai_prediction_window.py  ─── Baymax master launcher
# ----------------------------------------------------
# Imports
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QGridLayout,
    QFrame, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QFont, QCursor
from PyQt5.QtCore import Qt

# 🩺 individual prediction pages
from diabetes_pred       import DiabetesPredictionPage
from liver_pred          import LiverDiseasePredictionPage
from heart_disease_pred  import HeartDiseasePredictionPage     # ← NEW
from bmi_pred            import BMIPredictionPage              # ← NEW


class AIPredictionWindow(QWidget):
    def __init__(self, username="User"):
        super().__init__()
        self.username = username
        self.setWindowTitle("AI‑Powered Predictions - Baymax")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: #ecf0f1;")
        self.setup_ui()

    # ───────────────────────────────────────────────────────────
    # Build UI
    # ───────────────────────────────────────────────────────────
    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(30)

        # Header
        header_layout = QHBoxLayout()
        greeting = QLabel(f"Hey {self.username}!\nBaymax is ready to help you with AI…")
        greeting.setFont(QFont("Arial", 18, QFont.Bold))
        greeting.setStyleSheet("color: #2c3e50;")
        greeting.setAlignment(Qt.AlignLeft)

        logo = QLabel()
        pixmap = QPixmap("baymax2.png")
        logo.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignRight)

        header_layout.addWidget(greeting)
        header_layout.addStretch()
        header_layout.addWidget(logo)
        main_layout.addLayout(header_layout)

        # Feature grid
        grid = QGridLayout()
        grid.setSpacing(30)

        # Diabetes
        diabetes_box = self.create_feature_box("diabetes.png", "Diabetes Prediction")
        diabetes_box.mousePressEvent = self.open_diabetes_prediction
        grid.addWidget(diabetes_box, 0, 0)

        # Liver disease
        liver_box = self.create_feature_box("liver.png", "Liver Disease Prediction")
        liver_box.mousePressEvent = self.open_liver_prediction
        grid.addWidget(liver_box, 0, 1)

        # Heart disease
        heart_box = self.create_feature_box("heart.png", "Heart Disease Prediction")
        heart_box.mousePressEvent = self.open_heart_prediction
        grid.addWidget(heart_box, 1, 0)

        # BMI
        bmi_box = self.create_feature_box("health.png", "BMI Prediction")
        bmi_box.mousePressEvent = self.open_bmi_prediction
        grid.addWidget(bmi_box, 1, 1)

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    # ───────────────────────────────────────────────────────────
    # Helper for tiles
    # ───────────────────────────────────────────────────────────
    def create_feature_box(self, icon_path, title):
        frame = QFrame()
        frame.setFixedSize(350, 180)
        frame.setStyleSheet("""
            QFrame {
                background-color: #537f88;
                border-radius: 15px;
            }
            QFrame:hover {
                background-color: #3e5d65;
            }
        """)
        frame.setCursor(QCursor(Qt.PointingHandCursor))

        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignCenter)

        icon_label = QLabel()
        icon = QPixmap(icon_path)
        icon_label.setPixmap(icon.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("background-color: transparent;")

        text_label = QLabel(title)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setFont(QFont("Arial", 12, QFont.Bold))
        text_label.setStyleSheet("background-color: transparent; color: white;")

        layout.addWidget(icon_label)
        layout.addSpacing(10)
        layout.addWidget(text_label)

        return frame

    # ───────────────────────────────────────────────────────────
    # Slots for tile clicks
    # ───────────────────────────────────────────────────────────
    def open_diabetes_prediction(self, event):
        self.diabetes_window = DiabetesPredictionPage(username=self.username)
        self.diabetes_window.show()

    def open_liver_prediction(self, event):
        self.liver_window = LiverDiseasePredictionPage(username=self.username)
        self.liver_window.show()

    def open_heart_prediction(self, event):                    # ← NEW
        self.heart_window = HeartDiseasePredictionPage(username=self.username)
        self.heart_window.show()

    def open_bmi_prediction(self, event):                      # ← NEW
        self.bmi_window = BMIPredictionPage(username=self.username)
        self.bmi_window.show()


# ───────────────────────────────────────────────────────────
# Stand‑alone start
# ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AIPredictionWindow(username="Ragib")
    window.show()
    sys.exit(app.exec_())
