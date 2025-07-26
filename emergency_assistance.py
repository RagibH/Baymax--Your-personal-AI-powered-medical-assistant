import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtGui import QPixmap, QFont, QCursor
from PyQt5.QtCore import Qt

# ✅ Your other pages
from first_aid_chatbot import ChatbotUI
from emergency_directory import EmergencyDirectoryPage   # <‑‑ NEW IMPORT


class EmergencyAssistanceWindow(QWidget):
    def __init__(self, username="User"):
        super().__init__()
        self.username = username
        self.setWindowTitle("Emergency Assistance - Baymax")
        self.setGeometry(100, 100, 800, 500)
        self.setStyleSheet("background-color: #ecf0f1;")

        # Hold references so windows don’t get garbage‑collected
        self.chatbot_window = None
        self.directory_window = None            # <‑‑ NEW

        self.setup_ui()

    # ------------------------------------------------------------------ #
    #  UI LAYOUT                                                         #
    # ------------------------------------------------------------------ #
    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(30)

        # ----- Header (greeting + logo) --------------------------------
        header_layout = QHBoxLayout()
        greeting = QLabel(
            f"Hi {self.username}!\nBaymax is here to assist you in emergencies.")
        greeting.setFont(QFont("Arial", 18, QFont.Bold))
        greeting.setStyleSheet("color: #2c3e50;")

        logo = QLabel()
        pixmap = QPixmap("baymax2.png")
        logo.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio,
                                     Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignRight)

        header_layout.addWidget(greeting)
        header_layout.addStretch()
        header_layout.addWidget(logo)

        # ----- Feature boxes -------------------------------------------
        box_layout = QVBoxLayout()
        box_layout.setSpacing(30)

        first_aid_box = self.create_feature_box(
            "first_aid.png", "First Aid Guide", self.open_chatbot)

        emergency_directory_box = self.create_feature_box(
            "emergency_contact.png",      # use any icon you like
            "Emergency Directory",
            self.open_directory)          # <‑‑ NEW HANDLER

        box_layout.addWidget(first_aid_box)
        box_layout.addWidget(emergency_directory_box)

        # Center boxes vertically
        center_frame = QFrame()
        center_layout = QVBoxLayout(center_frame)
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.addLayout(box_layout)

        # Assemble main layout
        main_layout.addLayout(header_layout)
        main_layout.addWidget(center_frame, alignment=Qt.AlignCenter)
        self.setLayout(main_layout)

    # ------------------------------------------------------------------ #
    #  Feature‑box factory                                               #
    # ------------------------------------------------------------------ #
    def create_feature_box(self, icon_path, title, click_handler=None):
        frame = QFrame()
        frame.setFixedSize(350, 150)
        frame.setStyleSheet("""
            QFrame {
                background-color: #537f88;
                border-radius: 15px;
            }
            QFrame:hover {
                background-color: #5b99a3;
            }
        """)

        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignCenter)

        icon_label = QLabel()
        icon = QPixmap(icon_path)
        icon_label.setPixmap(icon.scaled(
            64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_label.setAlignment(Qt.AlignCenter)

        text_label = QLabel(title)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setFont(QFont("Arial", 12, QFont.Bold))
        text_label.setStyleSheet("color: white;")

        layout.addWidget(icon_label)
        layout.addSpacing(10)
        layout.addWidget(text_label)

        if click_handler:
            frame.setCursor(QCursor(Qt.PointingHandCursor))
            frame.mousePressEvent = lambda event: click_handler()

        return frame

    # ------------------------------------------------------------------ #
    #  Open auxiliary windows                                            #
    # ------------------------------------------------------------------ #
    def open_chatbot(self):
        if self.chatbot_window is None:
            self.chatbot_window = ChatbotUI()
        self.chatbot_window.show()
        self.chatbot_window.raise_()
        self.chatbot_window.activateWindow()

    def open_directory(self):
        if self.directory_window is None:
            self.directory_window = EmergencyDirectoryPage("bangladesh_doctors.csv")
        self.directory_window.show()
        self.directory_window.raise_()
        self.directory_window.activateWindow()


# ---------------------------------------------------------------------- #
#  ENTRY                                                                 #
# ---------------------------------------------------------------------- #
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmergencyAssistanceWindow(username="Ragib")
    window.show()
    sys.exit(app.exec_())
