# user_data_management.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QGroupBox
)
from PyQt5.QtCore import Qt
import db_utils                       # must expose get_conn()

class UserDataManagement(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.user_id  = None          # filled after load
        self.setWindowTitle(f"Account Settings – {username}")
        self.setGeometry(300, 200, 400, 250)
        self._build_ui()
        self._load_user_info()

    # ───────────────────────────────────────────────────────────
    def _build_ui(self):
        layout = QVBoxLayout(self)

        box = QGroupBox("Edit account details")
        form = QVBoxLayout(box)

        self.user_edit = QLineEdit(); self.user_edit.setPlaceholderText("Username")
        self.mail_edit = QLineEdit(); self.mail_edit.setPlaceholderText("Email")
        self.pass_edit = QLineEdit(); self.pass_edit.setPlaceholderText("New password")
        self.pass_edit.setEchoMode(QLineEdit.Password)

        save_btn = QPushButton("Save changes")
        save_btn.clicked.connect(self._save)

        form.addWidget(QLabel("Username:")); form.addWidget(self.user_edit)
        form.addWidget(QLabel("Email:"));    form.addWidget(self.mail_edit)
        form.addWidget(QLabel("Password (leave blank to keep current):"))
        form.addWidget(self.pass_edit)
        form.addWidget(save_btn)

        layout.addWidget(box)
        layout.addStretch()

    # ───────────────────────────────────────────────────────────
    def _load_user_info(self):
        try:
            conn = db_utils.get_connection()
            cur  = conn.cursor(dictionary=True)
            cur.execute("SELECT id, username, email FROM users WHERE username=%s",
                        (self.username,))
            row = cur.fetchone()
            cur.close(); conn.close()
            if row:
                self.user_id = row["id"]
                self.user_edit.setText(row["username"])
                self.mail_edit.setText(row["email"])
        except Exception as e:
            QMessageBox.critical(self, "DB error", str(e))

    # ───────────────────────────────────────────────────────────
    def _save(self):
        new_user = self.user_edit.text().strip()
        new_mail = self.mail_edit.text().strip()
        new_pwd  = self.pass_edit.text().strip()

        if not new_user or not new_mail:
            QMessageBox.warning(self, "Input error", "Username and email required.")
            return

        try:
            conn = db_utils.get_connection(); cur = conn.cursor()
            cur.execute("UPDATE users SET username=%s, email=%s WHERE id=%s",
                        (new_user, new_mail, self.user_id))
            if new_pwd:
                cur.execute("UPDATE users SET password=%s WHERE id=%s",
                            (new_pwd, self.user_id))
            conn.commit(); cur.close(); conn.close()
            QMessageBox.information(self, "Saved", "Account updated.")
            self.username = new_user
            self.pass_edit.clear()
        except Exception as e:
            QMessageBox.critical(self, "DB error", str(e))


# Stand‑alone test
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = UserDataManagement("testuser")
    w.show()
    sys.exit(app.exec_())
