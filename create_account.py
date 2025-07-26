import sys
import mysql.connector
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QSizePolicy, QSpacerItem, QFrame
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


class CreateAccountWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Account - Baymax")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: #e3f2fd;")
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)

        # Left Panel (Image)
        image_label = QLabel()
        pixmap = QPixmap("baymax2.png")
        if not pixmap.isNull():
            image_label.setPixmap(pixmap.scaled(350, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout.addWidget(image_label, 1)

        # Right Panel (Form Card)
        form_container = QFrame()
        form_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
                padding: 30px;
                max-width: 400px;
            }
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setAlignment(Qt.AlignCenter)
        form_layout.setSpacing(20)

        # Title
        title = QLabel("Create Your Account")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #333;")
        title.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(title)

        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedHeight(40)
        self.username_input.setStyleSheet(self.line_edit_style())
        form_layout.addWidget(self.username_input)

        # Email input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setFixedHeight(40)
        self.email_input.setStyleSheet(self.line_edit_style())
        form_layout.addWidget(self.email_input)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet(self.line_edit_style())
        form_layout.addWidget(self.password_input)

        # Create account button
        create_button = QPushButton("Create Account")
        create_button.setFixedHeight(45)
        create_button.setStyleSheet("""
            QPushButton {
                background-color: #1e88e5;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """)
        create_button.clicked.connect(self.create_account)
        form_layout.addWidget(create_button)

        # Stretch top & bottom for vertical centering
        container_wrapper = QVBoxLayout()
        container_wrapper.addStretch()
        container_wrapper.addWidget(form_container, alignment=Qt.AlignCenter)
        container_wrapper.addStretch()

        main_layout.addLayout(container_wrapper, 1)

    def line_edit_style(self):
        return """
            QLineEdit {
                padding-left: 10px;
                font-size: 14px;
                border: 1.5px solid #90caf9;
                border-radius: 8px;
                background-color: #f9f9f9;
            }
            QLineEdit:focus {
                border: 2px solid #42a5f5;
                background-color: #ffffff;
            }
        """

    def create_account(self):
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not email or not password:
            QMessageBox.warning(self, "Incomplete", "All fields are required.")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="baymax"
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                           (username, email, password))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Account created successfully!")
            self.close()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CreateAccountWindow()
    window.show()
    sys.exit(app.exec_())
