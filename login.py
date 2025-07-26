import sys
import mysql.connector
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QFrame, QCheckBox
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from create_account import CreateAccountWindow
from dashboard import DashboardWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Baymax Login")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: #d8f5e3;")
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)

        # Left frame for Baymax image
        left_frame = QFrame()
        left_layout = QVBoxLayout(left_frame)
        left_layout.setAlignment(Qt.AlignCenter)

        image_label = QLabel()
        pixmap = QPixmap("baymax.png")  # Use a transparent background PNG
        if not pixmap.isNull():
            image_label.setPixmap(pixmap.scaled(350, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(image_label)

        # Right frame for login form
        right_frame = QFrame()
        right_layout = QVBoxLayout(right_frame)
        right_layout.setSpacing(15)
        right_layout.setAlignment(Qt.AlignCenter)

        # Baymax title
        header_title = QLabel("Baymax")
        header_title.setFont(QFont("Arial", 24, QFont.Bold))
        header_title.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(header_title)

        # Subtitle
        subtitle = QLabel("Your personal health assistant...")
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #555;")
        right_layout.addWidget(subtitle)

        # Login box
        login_box = QVBoxLayout()

        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username or Email")
        self.username_input.setFixedHeight(40)
        self.username_input.setStyleSheet(
            "padding: 10px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;"
        )

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet(
            "padding: 10px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;"
        )

        # Show password checkbox
        self.show_password_checkbox = QCheckBox("Show Password")
        self.show_password_checkbox.setFont(QFont("Arial", 10))
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        # Sign In button
        login_button = QPushButton("Sign In")
        login_button.setFixedHeight(40)
        login_button.setStyleSheet(
            "background-color: #2e7d32; color: white; font-size: 16px; border-radius: 5px;"
        )
        login_button.clicked.connect(self.check_credentials)

        # Forgot password link
        forgot_label = QLabel("<a href='#'>Forgot password?</a>")
        forgot_label.setFont(QFont("Arial", 10))
        forgot_label.setAlignment(Qt.AlignRight)
        forgot_label.setTextFormat(Qt.RichText)
        forgot_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        forgot_label.linkActivated.connect(self.open_forgot_password)


        # New user link
        new_account_label = QLabel("New? <a href='#'>Create an account</a>")
        new_account_label.setFont(QFont("Arial", 10))
        new_account_label.setAlignment(Qt.AlignCenter)
        new_account_label.setTextFormat(Qt.RichText)
        new_account_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        new_account_label.setOpenExternalLinks(False)  # Important: handle clicks internally
        new_account_label.linkActivated.connect(self.open_create_account)  # Connect signal


        # Add widgets to login box
        login_box.addWidget(self.username_input)
        login_box.addWidget(self.password_input)
        login_box.addWidget(self.show_password_checkbox)
        login_box.addWidget(forgot_label)
        login_box.addWidget(login_button)
        login_box.addWidget(new_account_label)

        right_layout.addSpacing(10)
        right_layout.addLayout(login_box)

        # Add frames to main layout
        main_layout.addWidget(left_frame, 1)
        main_layout.addWidget(right_frame, 1)

    def toggle_password_visibility(self, state):
        if state == Qt.Checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
    def open_create_account(self):
        self.create_account_window = CreateAccountWindow()
        self.create_account_window.show()
    def open_forgot_password(self):
        from forget_pass import ForgotPasswordWindow
        self.forgot_window = ForgotPasswordWindow()
        self.forgot_window.show()
    


    def check_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Incomplete", "Please enter both username and password.")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="baymax"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()
            conn.close()

            if result:
                QMessageBox.information(self, "Success", "Login successful!")
                self.dashboard = DashboardWindow(username=username)
                self.dashboard.show()
                self.close()  # Close the login window
            else:
                QMessageBox.warning(self, "Failed", "Invalid username or password.")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
