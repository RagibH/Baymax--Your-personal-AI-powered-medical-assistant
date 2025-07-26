import sys, random, hashlib, webbrowser, os
from datetime import datetime, time
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea, QFrame, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPainter, QColor, QClipboard
from PyQt5.QtCore import Qt, QTimer

ACTIVE_START = time(9, 30)
ACTIVE_END = time(21, 0)
AVATAR_DIR = "avatars"


class EmergencyDirectoryPage(QWidget):
    def __init__(self, csv_path="data/bangladesh_doctors.csv", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Baymax — Emergency Directory")
        self.setWindowIcon(QIcon("baymax.png"))
        self.resize(1280, 850)

        # ----  GLOBAL STYLE  -------------------------------------------------
        self.setStyleSheet("""
            QWidget {                       /* App‑wide */
                background-color: #0d1b2a;  /* Navy */
                color: white;
                font-family: 'Segoe UI';
            }
        """)

        # ----  DATA PREP  ----------------------------------------------------
        self.df = pd.read_csv(csv_path, dtype=str).fillna("")
        self.df["ContactNo"] = self.df["ContactNo"].apply(
            lambda x: "0" + x.lstrip("0") if not x.startswith("0") else x
        )

        # ----  MAIN LAYOUT  --------------------------------------------------
        root = QVBoxLayout(self)
        root.setSpacing(20)

        self._build_header(root)
        self._build_filter_bar(root)
        self._build_scroll_area(root)

        # populate cascading combos
        self._populate_combo(self.division_cb, sorted(self.df["Division"].unique()))
        self._update_districts()

    # --------------------------------------------------------------------- #
    #  HEADER                                                               #
    # --------------------------------------------------------------------- #
    def _build_header(self, parent_layout):
        top = QHBoxLayout()

        logo = QLabel()
        logo.setPixmap(QPixmap("baymax.png").scaled(48, 48,
                                                   Qt.KeepAspectRatio,
                                                   Qt.SmoothTransformation))
        logo.setStyleSheet("background: transparent;")

        title = QLabel("Baymax — Emergency Directory")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color:#ffffff; background:transparent;")

        self.clock = QLabel()
        self._update_clock()
        self.clock.setStyleSheet("""
            font-size: 14px; color:#0d1b2a;
            padding: 6px 12px; background:#ffffff; border-radius:12px;
        """)
        QTimer.singleShot(1000, self._refresh_clock)

        top.addWidget(logo)
        top.addWidget(title)
        top.addStretch()
        top.addWidget(self.clock)
        parent_layout.addLayout(top)

    # --------------------------------------------------------------------- #
    #  FILTER BAR                                                           #
    # --------------------------------------------------------------------- #
    def _build_filter_bar(self, parent_layout):
        layout = QHBoxLayout()

        # Search box
        self.search_line = QLineEdit()
        self.search_line.setPlaceholderText("🔍  Search doctor name…")
        self.search_line.textChanged.connect(self._update_cards)
        self.search_line.setFixedWidth(350)
        layout.addWidget(self.search_line)

        # Combos
        self.division_cb = self._add_combo("All Divisions", layout, self._update_districts)
        self.district_cb  = self._add_combo("All Districts", layout, self._update_upazilas)
        self.upazila_cb   = self._add_combo("All Upazilas", layout, self._update_departments)
        self.dept_cb      = self._add_combo("All Departments", layout, self._update_hospitals)
        self.hospital_cb  = self._add_combo("All Hospitals", layout, self._update_cards)

        # Reset Button
        reset = QPushButton("🔄 Reset")
        reset.clicked.connect(self._reset_filters)
        layout.addWidget(reset)
        layout.addStretch()
        parent_layout.addLayout(layout)

        # Styling
        self.setStyleSheet(self.styleSheet() + """
            QLineEdit, QComboBox {
                min-width: 160px;
                min-height: 48px;
                padding: 12px 16px;
                border-radius: 12px;
                border: 2px solid #1d3557;
                background-color: #ffffff;
                color: #0d1b2a;
                font-size: 14px;
            }

            QComboBox::drop-down {
                width: 30px;
            }

            QComboBox QAbstractItemView {
                background-color: #ffffff;
                selection-background-color: #a8dadc;
                padding: 4px;
                font-size: 14px;
            }

            QPushButton {
                min-height: 48px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                background-color: #1d3557;
                color: white;
                border-radius: 12px;
            }

            QPushButton:hover {
                background-color: #457b9d;
            }
        """)


    def _add_combo(self, placeholder, layout, slot):
        cb = QComboBox()
        cb.addItem(placeholder)
        cb.currentTextChanged.connect(slot)
        layout.addWidget(cb)
        return cb

    # --------------------------------------------------------------------- #
    #  SCROLL AREA (Doctor Cards)   lkkk                                        #
    # --------------------------------------------------------------------- #
    def _build_scroll_area(self, parent_layout):
        self.scroll = QScrollArea(); self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border:none;")
        content = QWidget()
        self.grid = QGridLayout(content); self.grid.setSpacing(20)
        self.scroll.setWidget(content)
        parent_layout.addWidget(self.scroll)

    # --------------------------------------------------------------------- #
    #  CASCADING COMBO HELPERS                                              #
    # --------------------------------------------------------------------- #
    def _populate_combo(self, cb, items, keep_current=True):
        placeholder = cb.itemText(0)
        current = cb.currentText() if keep_current else ""
        cb.blockSignals(True)
        cb.clear()
        cb.addItem(placeholder)
        cb.addItems(items)
        cb.setCurrentText(current if current in items else placeholder)
        cb.blockSignals(False)

    def _reset_filters(self):
        self.search_line.blockSignals(True); self.search_line.clear()
        self.search_line.blockSignals(False)
        for cb in [self.division_cb, self.district_cb,
                   self.upazila_cb, self.dept_cb, self.hospital_cb]:
            cb.blockSignals(True); cb.setCurrentIndex(0); cb.blockSignals(False)
        self._update_districts()

    def _cascade_df(self, levels):
        df = self.df
        mapping = {"Division": self.division_cb, "District": self.district_cb,
                   "Upazila": self.upazila_cb, "Department": self.dept_cb,
                   "Address": self.hospital_cb}
        for lvl in levels:
            val = mapping[lvl].currentText()
            if val.startswith("All ") or val.strip() == "":  # skip placeholder
                continue
            df = df[df[lvl] == val]
        return df

    def _update_districts(self):
        self._populate_combo(self.district_cb,
                             sorted(self._cascade_df(["Division"])["District"].unique()))
        self._update_upazilas()

    def _update_upazilas(self):
        self._populate_combo(self.upazila_cb,
                             sorted(self._cascade_df(["Division", "District"])["Upazila"].unique()))
        self._update_departments()

    def _update_departments(self):
        self._populate_combo(self.dept_cb,
                             sorted(self._cascade_df(["Division", "District",
                                                      "Upazila"])["Department"].unique()))
        self._update_hospitals()

    def _update_hospitals(self):
        self._populate_combo(self.hospital_cb,
                             sorted(self._cascade_df(["Division", "District",
                                                      "Upazila", "Department"])["Address"].unique()))
        self._update_cards()

    # --------------------------------------------------------------------- #
    #  CARD GRID UPDATE                                                     #
    # --------------------------------------------------------------------- #
    def _update_cards(self):
        df = self._cascade_df(
            ["Division", "District", "Upazila", "Department", "Address"]
        )
        # Friday off
        if datetime.today().weekday() == 4:
            df = df.iloc[0:0]

        term = self.search_line.text().strip().lower()
        if term:
            df = df[df["Provider"].str.lower().str.contains(term)]

        df = df.reset_index(drop=True)

        # Clear previous widgets
        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        cols = 3 if len(df) >= 3 else max(len(df), 1)
        for idx, row in df.iterrows():
            card = self._make_card(row)
            r, c = divmod(idx, cols)
            self.grid.addWidget(card, r, c)

    # --------------------------------------------------------------------- #
    #  SINGLE CARD CREATION                                                 #
    # --------------------------------------------------------------------- #
    def _make_card(self, row):
        frame = QFrame(); frame.setObjectName("card")
        frame.setStyleSheet("""
            QFrame#card {
                background: #ffffff;
                border-radius: 18px;
                padding: 18px;
                border: 2px solid #cccccc;
            }
        """)
        v = QVBoxLayout(frame); v.setSpacing(12)

        # -- Avatar with white circle background
        avatar_container = QLabel()
        avatar_container.setFixedSize(90, 90)
        avatar_container.setStyleSheet("""
            background:#ffffff; border-radius:45px;
            border:2px solid #1d3557;
        """)
        avatar_container.setAlignment(Qt.AlignCenter)

        avatar_path = os.path.join(
            AVATAR_DIR, f"{row['Provider'].replace(' ', '_').lower()}.png"
        )
        if os.path.exists(avatar_path):
            pix = QPixmap(avatar_path).scaled(
                80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            pix = self._create_avatar(row["Provider"]).scaled(
                80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        avatar_container.setPixmap(pix)
        v.addWidget(avatar_container, alignment=Qt.AlignCenter)

        # -- Text fields (each on white background)
        def make_label(text, bold=False, color="#1d3557"):
            lab = QLabel(text)
            lab.setFont(QFont("Segoe UI", 13 if bold else 11,
                              QFont.Bold if bold else QFont.Normal))
            lab.setAlignment(Qt.AlignCenter)
            lab.setStyleSheet(f"""
                background:#ffffff; color:{color};
                padding:4px; border-radius:6px;
            """)
            return lab

        v.addWidget(make_label(row["Provider"], bold=True))
        v.addWidget(make_label(row["Post"], color="#444444"))
        v.addWidget(make_label(f"📞 {row['ContactNo']}", color="#222222"))
        v.addWidget(make_label(f"🏥 {row['Department']}"))

        # -- Buttons
        buttons = QHBoxLayout()
        copy_btn = QPushButton("📋 Copy Number")
        copy_btn.setStyleSheet("""
            background:#e63946; color:white;
            padding:6px 14px; border-radius:10px;
        """)
        copy_btn.clicked.connect(
            lambda _, p=row["ContactNo"]: self._copy_phone(p))

        map_btn = QPushButton("📍 View Map")
        map_btn.setStyleSheet("""
            background:#457b9d; color:white;
            padding:6px 14px; border-radius:10px;
        """)
        map_btn.clicked.connect(
            lambda _, l=row["Address"]:
            webbrowser.open(f"https://www.google.com/maps/search/{l.replace(' ', '+')}", new=2)
        )

        buttons.addStretch()
        buttons.addWidget(copy_btn)
        buttons.addWidget(map_btn)
        buttons.addStretch()
        v.addLayout(buttons)

        return frame

    # ------------------------------------------------------------------ #
    #  UTILITIES                                                          #
    # ------------------------------------------------------------------ #
    def _copy_phone(self, phone):
        QApplication.clipboard().setText(phone, mode=QClipboard.Clipboard)
        QMessageBox.information(self, "Copied", f"{phone} copied to clipboard!")

    def _create_avatar(self, name, size=96):
        initials = "".join([p[0] for p in name.split()[:2]]).upper() or "?"
        h = int(hashlib.sha256(name.encode()).hexdigest(), 16)
        random.seed(h)
        r, g, b = [int(130 + random.random() * 100) for _ in range(3)]

        pix = QPixmap(size, size); pix.fill(Qt.transparent)
        painter = QPainter(pix)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setBrush(QColor(r, g, b)); painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, size, size)
        painter.setPen(QColor("#ffffff"))
        painter.setFont(QFont("Segoe UI", int(size/3), QFont.Bold))
        painter.drawText(pix.rect(), Qt.AlignCenter, initials)
        painter.end()
        return pix

    # clock helpers
    def _update_clock(self):
        self.clock.setText(datetime.now().strftime(
            "%A, %d %B %Y | %I:%M:%S %p"))

    def _refresh_clock(self):
        self._update_clock()
        QTimer.singleShot(1000, self._refresh_clock)


# ---------------------------------------------------------------------- #
#  ENTRY                                                                 #
# ---------------------------------------------------------------------- #
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmergencyDirectoryPage("bangladesh_doctors.csv")
    window.show()
    sys.exit(app.exec_())
