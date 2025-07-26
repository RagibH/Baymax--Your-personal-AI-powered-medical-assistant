import sys, os, numpy as np, pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog,
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QRubberBand,
    QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap, QFont, QImage
from PyQt5.QtCore import Qt, QPoint, QRect, QRectF, QSize, pyqtSignal

import tensorflow as tf  # primary loader for legacy models
import keras              # secondary loader for Keras‑3 models
from sklearn.preprocessing import LabelEncoder
from PIL import Image

# ────────────────────────────────
#  CONFIG
# ────────────────────────────────
IMG_SIZE       = 224
MODEL_PATH     = "prescription_model.keras"   # ensure this matches your file name
TRAIN_CSV_PATH = "training_labels.csv"        # adjust if needed

# ────────────────────────────────
#  UTILITIES
# ────────────────────────────────

def build_label_encoder(csv_path: str) -> LabelEncoder:
    df = pd.read_csv(csv_path)
    df.dropna(inplace=True)
    le = LabelEncoder()
    le.fit(df["MEDICINE_NAME"])
    return le


def qpixmap_to_model_input(pixmap: QPixmap) -> np.ndarray:
    """Convert QPixmap → (1, 224, 224, 3) float32 tensor in [0, 1] range."""
    qimage = pixmap.toImage().convertToFormat(QImage.Format_RGB888)
    w, h   = qimage.width(), qimage.height()
    ptr    = qimage.bits()
    ptr.setsize(h * w * 3)
    arr    = np.frombuffer(ptr, np.uint8).reshape((h, w, 3))
    img    = Image.fromarray(arr).resize((IMG_SIZE, IMG_SIZE))
    return np.expand_dims(np.asarray(img, dtype=np.float32) / 255.0, axis=0)


# ────────────────────────────────
#  ROBUST MODEL LOADER
# ────────────────────────────────

def robust_load_model(path: str):
    """Load both legacy (TF‑keras ≤ 2.x) and modern (.keras) models without errors."""
    try:
        from tensorflow.keras.layers import InputLayer

        class LegacyInputLayer(InputLayer):
            def __init__(self, *args, **kwargs):
                kwargs.pop("batch_shape", None)  # ignore unrecognized arg
                super().__init__(*args, **kwargs)

        return tf.keras.models.load_model(
            path,
            compile=False,
            custom_objects={"InputLayer": LegacyInputLayer},
        )

    except Exception as e1:
        try:
            return keras.models.load_model(path, compile=False, safe_mode=False)
        except Exception as e2:
            raise RuntimeError(
                "Could not load model.\n\n"
                f"tf.keras loader error:\n{e1}\n\n"
                f"keras (v3) loader error:\n{e2}"
            ) from None



# ────────────────────────────────
#  CROP GRAPHICS VIEW
# ────────────────────────────────
class CropGraphicsView(QGraphicsView):
    selection_made = pyqtSignal(QRect)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.origin      = QPoint()
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.origin = event.pos()
            self.rubber_band.setGeometry(QRect(self.origin, QSize()))
            self.rubber_band.show()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not self.origin.isNull():
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.rubber_band.hide()
            self.selection_made.emit(self.rubber_band.geometry())
        super().mouseReleaseEvent(event)

# ────────────────────────────────
#  MAIN APPLICATION WINDOW
# ────────────────────────────────
class PrescriptionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prescription Recognition – Baymax")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color:#ecf0f1;")

        # ── Load model and labels ───────────────────────────
        try:
            self.model = robust_load_model(MODEL_PATH)
        except Exception as e:
            QMessageBox.critical(self, "Model Load Error",
                                 f"Failed to load model:\n\n{e}")
            sys.exit(1)

        try:
            self.label_encoder = build_label_encoder(TRAIN_CSV_PATH)
        except Exception as e:
            QMessageBox.critical(self, "Label Error",
                                 f"Failed to load labels:\n\n{e}")
            sys.exit(1)

        self.original_pixmap = None
        self.cropped_pixmap  = None
        self.pixmap_item     = None

        self.setup_ui()

    # ───────────────────────── UI SETUP ─────────────────────────
    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 20)

        # Header
        header_layout = QHBoxLayout()
        logo = QLabel()
        logo.setPixmap(QPixmap("baymax2.png").scaled(
            100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        title = QLabel("Prescription Recognition")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setStyleSheet("color:#2c3e50;")

        header_layout.addWidget(logo)
        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addStretch()

        # Image view
        self.view  = CropGraphicsView()
        self.view.setStyleSheet("background-color:white;border:2px solid #bdc3c7;")
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.view.selection_made.connect(self.crop_from_view)

        # Buttons
        button_layout = QHBoxLayout()
        self.upload_btn = QPushButton("Upload Image")
        self.upload_btn.setStyleSheet("background-color:#3498db;color:white;font-weight:bold;padding:10px;")
        self.upload_btn.clicked.connect(self.load_image)

        self.upload_cropped_btn = QPushButton("Upload to Model")
        self.upload_cropped_btn.setStyleSheet("background-color:#2ecc71;color:white;font-weight:bold;padding:10px;")
        self.upload_cropped_btn.clicked.connect(self.upload_cropped_image)

        button_layout.addWidget(self.upload_btn)
        button_layout.addWidget(self.upload_cropped_btn)

        # Cropped preview
        self.cropped_label = QLabel("Cropped image will appear here.")
        self.cropped_label.setAlignment(Qt.AlignCenter)
        self.cropped_label.setStyleSheet("border:2px dashed #95a5a6;color:#7f8c8d;")
        self.cropped_label.setFixedHeight(200)

        # Result label
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.result_label.setStyleSheet("color:#e74c3c;")

        # Assemble layout
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.view)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.cropped_label)
        main_layout.addWidget(self.result_label)
        self.setLayout(main_layout)

    # ─────────────────────── IMAGE HANDLERS ───────────────────────
    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_name:
            self.original_pixmap = QPixmap(file_name)
            self.scene.clear()
            self.pixmap_item = QGraphicsPixmapItem(self.original_pixmap)
            self.scene.addItem(self.pixmap_item)
            self.view.setSceneRect(QRectF(self.original_pixmap.rect()))
            self.result_label.clear()
            self.cropped_label.clear()
            self.cropped_pixmap = None

    def crop_from_view(self, rubberband_rect: QRect):
        if self.original_pixmap:
            scene_rect = self.view.mapToScene(rubberband_rect).boundingRect().toRect()
            if scene_rect.isValid():
                self.cropped_pixmap = self.original_pixmap.copy(scene_rect)
                self.cropped_label.setPixmap(self.cropped_pixmap.scaled(
                    self.cropped_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.result_label.setText("")

    def upload_cropped_image(self):
        if self.cropped_pixmap is None:
            QMessageBox.information(self, "No Crop", "Please crop a region first.")
            return
        try:
            img_batch = qpixmap_to_model_input(self.cropped_pixmap)
            preds     = self.model.predict(img_batch, verbose=0)
            idx       = int(np.argmax(preds, axis=1)[0])
            label     = self.label_encoder.inverse_transform([idx])[0]
            conf      = float(np.max(preds)) * 100.0
            self.result_label.setText(f"Predicted: {label}  ({conf:.2f}%)")
        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", f"Could not process image:\n\n{e}")


# ────────────────────────────────
#  RUN UI
# ────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PrescriptionWindow()
    window.show()
    sys.exit(app.exec_())
