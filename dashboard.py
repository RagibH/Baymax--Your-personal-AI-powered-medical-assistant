import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

from ai_powered_prediction import AIPredictionWindow
from emergency_assistance import EmergencyAssistanceWindow
from prescription import PrescriptionWindow  
from user_data_management import UserDataManagement

class DashboardWindow(QWidget):
    def __init__(self, username="User", user_id=None):  # Accept user_id here
        super().__init__()
        self.username = username
        self.user_id = user_id  # Store user_id if needed
        self.setWindowTitle("Baymax Dashboard")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: #ecf0f1;")
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(30)

        # Header
        header_layout = QHBoxLayout()
        greeting = QLabel(f"Hello {self.username}!\nWelcome to Baymax Dashboard")
        greeting.setFont(QFont("Arial", 18, QFont.Bold))
        greeting.setStyleSheet("color: #2c3e50;")

        logo = QLabel()
        pixmap = QPixmap("baymax.png")
        logo.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignRight)

        header_layout.addWidget(greeting)
        header_layout.addStretch()
        header_layout.addWidget(logo)

        # Grid for feature buttons
        grid = QGridLayout()
        grid.setSpacing(30)

        # Button 1: AI Predictions
        grid.addWidget(self.create_feature_button("ai_prediction.png", "AI-Powered Predictions", self.open_ai_prediction), 0, 0)

        # Button 2: Prescription Recognition
        grid.addWidget(self.create_feature_button("prescription_prediction.png", "Prescription Recognition", self.open_prescription_recognition), 0, 1)

        # Button 3: Emergency Assistance
        grid.addWidget(self.create_feature_button("emergency_icon.png", "Emergency Assistance", self.open_emergency_assistance), 1, 0)

        # Button 4: User & Data Management (click handler optional)
        grid.addWidget(
            self.create_feature_button(
                "data_icon.png",
                "User & Data Management",
                self.open_user_data_management   # ← pass the slot
            ),
            1, 1
        )

        main_layout.addLayout(header_layout)
        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    
    def open_ai_prediction(self):
        # Pass user_id if your AIPredictionWindow accepts it; else just pass username
        self.ai_window = AIPredictionWindow(username=self.username)
        self.ai_window.show()

    
    def open_emergency_assistance(self):
        self.emergency_window = EmergencyAssistanceWindow(username=self.username)
        self.emergency_window.show()

    
    def open_prescription_recognition(self):
        self.prescription_window = PrescriptionWindow()
        self.prescription_window.show()

    def open_user_data_management(self):                       # ← NEW
        self.udm_window = UserDataManagement(username=self.username)
        self.udm_window.show()

    def create_feature_button(self, icon_path, title, click_callback=None):
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
        frame.setCursor(Qt.PointingHandCursor)

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

        if click_callback:
            frame.mousePressEvent = lambda event: click_callback()

        return frame

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = DashboardWindow(username="Ragib")
    dashboard.show()
    sys.exit(app.exec_())
