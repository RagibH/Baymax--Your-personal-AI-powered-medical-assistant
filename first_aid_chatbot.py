import sys
import os
import json
import pickle
import random
import traceback
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QFrame, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QFont, QColor, QPalette, QPainter, QBrush
from PyQt5.QtCore import Qt
from tensorflow.keras.models import load_model
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer

# === Load resources ===
lemmatizer = WordNetLemmatizer()
tokenizer = TreebankWordTokenizer()

model = load_model("chatbot_model.h5")
intents = json.load(open("intents.json", encoding="utf-8"))
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))

# === Preprocessing ===
def clean_up_sentence(sentence):
    sentence_words = tokenizer.tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(w.lower()) for w in sentence_words if w.isalpha()]
    return sentence_words

def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [1 if w in sentence_words else 0 for w in words]
    return np.array(bag)

def predict_class(sentence):
    input_data = bow(sentence, words)
    input_data = np.array([input_data])
    res = model.predict(input_data, verbose=0)[0]

    ERROR_THRESHOLD = 0.3
    results = [(i, r) for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)

    if not results:
        return []

    predicted = [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]
    return predicted

def get_response(ints, intents_json):
    if not ints:
        return "I'm not sure how to help with that. 🤔"
    tag = ints[0]['intent']
    for intent in intents_json['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])
    return "Hmm... I don't have an answer for that."

# === Chat UI ===
class ChatbotUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Baymax First Aid Chatbot")
        self.setGeometry(200, 100, 600, 700)
        self.setStyleSheet("background-color: white;")
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Title & Logo
        title = QLabel("Baymax Chatbot 💬")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Transparent Baymax background logo
        bg_logo = QLabel(self)
        pixmap = QPixmap("baymax_logo.png")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            bg_logo.setPixmap(pixmap)
            bg_logo.setAlignment(Qt.AlignCenter)
            bg_logo.setStyleSheet("opacity: 0.04; position: absolute;")
            main_layout.addWidget(bg_logo)

        # Scrollable chat area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setSpacing(10)
        self.chat_layout.addStretch(1)
        self.scroll_area.setWidget(self.chat_container)
        main_layout.addWidget(self.scroll_area)

        # Input + Send
        input_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type your message...")
        self.input_box.returnPressed.connect(self.chat)
        self.input_box.setStyleSheet("padding: 10px; font-size: 14px;")
        send_btn = QPushButton("Send")
        send_btn.setStyleSheet("background-color: #3399ff; color: white; font-weight: bold; padding: 10px;")
        send_btn.clicked.connect(self.chat)

        input_layout.addWidget(self.input_box)
        input_layout.addWidget(send_btn)
        main_layout.addLayout(input_layout)

    def add_message(self, text, is_user):
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setFont(QFont("Segoe UI", 11))
        bubble.setContentsMargins(10, 10, 10, 10)
        bubble.setStyleSheet(
            "background-color: #d4fcd4; border-radius: 10px; padding: 8px 12px;" if is_user else
            "background-color: #d4e6fc; border-radius: 10px; padding: 8px 12px;"
        )
        bubble.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)
        if is_user:
            layout.addStretch()
            layout.addWidget(bubble)
        else:
            layout.addWidget(bubble)
            layout.addStretch()

        wrapper = QFrame()
        wrapper.setLayout(layout)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, wrapper)

        # Auto-scroll
        QApplication.processEvents()
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )

    def chat(self):
        try:
            user_input = self.input_box.text().strip()
            self.input_box.clear()
            if not user_input:
                return

            self.add_message(user_input, is_user=True)
            predictions = predict_class(user_input)
            response = get_response(predictions, intents)
            self.add_message(response, is_user=False)

        except Exception:
            self.add_message("Sorry, something went wrong. 😓", is_user=False)
            print("Chatbot Error:\n", traceback.format_exc())

# === Main ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatbotUI()
    window.show()
    sys.exit(app.exec_())
