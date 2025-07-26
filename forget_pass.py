import sys
import mysql.connector
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout, QFrame
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt


class ForgotPasswordWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Forgot Password - Baymax")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("background-color: #f0f8ff;")
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)

        # Left: Baymax image
        image_frame = QFrame()
        image_layout = QVBoxLayout(image_frame)
        image_label = QLabel()
        pixmap = QPixmap("baymax2.png")
        image_label.setPixmap(pixmap.scaled(350, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(image_label)

        # Right: Form
        form_frame = QFrame()
        form_layout = QVBoxLayout(form_frame)
        form_layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Reset Your Password")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username or email")
        self.username_input.setFixedHeight(40)
        self.username_input.setStyleSheet("padding: 10px; font-size: 14px; border: 1px solid #ccc; border-radius: 6px;")

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Enter new password")
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setFixedHeight(40)
        self.new_password_input.setStyleSheet("padding: 10px; font-size: 14px; border: 1px solid #ccc; border-radius: 6px;")

        reset_button = QPushButton("Reset Password")
        reset_button.setFixedHeight(40)
        reset_button.setStyleSheet("background-color: #007BFF; color: white; font-size: 15px; border-radius: 6px;")
        reset_button.clicked.connect(self.reset_password)

        form_layout.addWidget(title)
        form_layout.addSpacing(20)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.new_password_input)
        form_layout.addSpacing(10)
        form_layout.addWidget(reset_button)

        layout.addWidget(image_frame, 1)
        layout.addWidget(form_frame, 1)

    def reset_password(self):
        username = self.username_input.text()
        new_password = self.new_password_input.text()

        if not username or not new_password:
            QMessageBox.warning(self, "Missing Fields", "Please fill in all fields.")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="baymax"
            )
            cursor = conn.cursor()

            # Check if user exists
            cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, username))
            result = cursor.fetchone()

            if result:
                cursor.execute("UPDATE users SET password = %s WHERE username = %s OR email = %s", 
                               (new_password, username, username))
                conn.commit()
                QMessageBox.information(self, "Success", "Password reset successfully!")
                self.close()
            else:
                QMessageBox.warning(self, "Not Found", "No account found with that username/email.")

            conn.close()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ForgotPasswordWindow()
    window.show()
    sys.exit(app.exec_())
