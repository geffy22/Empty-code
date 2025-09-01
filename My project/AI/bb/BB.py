import sys
import threading
import pyttsx3
import speech_recognition as sr
import openai
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLineEdit, QLabel, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPixmap

#  API 
client = openai.OpenAI(api_key="API")

def ask_bb(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка API: {str(e)}"

# PyQt
class BBChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BB Chat")
        self.setGeometry(200, 100, 600, 700)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background-color: #1e1e1e; font-family: Helvetica; color: #fff;")
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.top_bar = QFrame()
        self.top_bar.setFixedHeight(40)
        self.top_bar.setStyleSheet("background-color: #2c2c2c;")
        self.top_layout = QHBoxLayout()
        self.top_layout.setContentsMargins(10,0,10,0)
        self.top_bar.setLayout(self.top_layout)
        self.title_label = QLabel("BB Chat")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff;")
        self.top_layout.addWidget(self.title_label)
        self.top_layout.addStretch()
        self.min_button = QPushButton("–")
        self.min_button.setFixedSize(30,30)
        self.min_button.setStyleSheet("background-color: #4e4e4e; border:none; color: white; font-weight:bold;")
        self.min_button.clicked.connect(self.showMinimized)
        self.top_layout.addWidget(self.min_button)
        self.close_button = QPushButton("✕")
        self.close_button.setFixedSize(30,30)
        self.close_button.setStyleSheet("background-color: #ff5c5c; border:none; font-weight:bold; color: white;")
        self.close_button.clicked.connect(self.close)
        self.top_layout.addWidget(self.close_button)
        self.layout.addWidget(self.top_bar)
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("background-color: #2e2e2e; border-radius: 0px; padding:5px; font-size: 12pt;")
        self.layout.addWidget(self.chat_area)
        self.input_frame = QFrame()
        self.input_layout = QHBoxLayout()
        self.input_layout.setContentsMargins(10,5,10,5)
        self.input_frame.setLayout(self.input_layout)
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Введите сообщение...")
        self.entry.setStyleSheet("background-color: #3e3e3e; border-radius: 5px; padding:5px; color: #ffffff; font-size: 12pt;")
        self.entry.returnPressed.connect(self.send_message)
        self.input_layout.addWidget(self.entry)
        self.send_button = QPushButton("Отправить")
        self.send_button.setStyleSheet("background-color: #4e8cff; border-radius:5px; padding:5px; font-weight:bold;")
        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.send_button)
        self.voice_button = QPushButton("🎤 Голосовой ввод")
        self.voice_button.setStyleSheet("background-color: #9b59b6; border-radius:5px; padding:5px; font-weight:bold;")
        self.voice_button.clicked.connect(self.start_voice_input)
        self.input_layout.addWidget(self.voice_button)
        self.layout.addWidget(self.input_frame)
        self.offset = None
        self.top_bar.mousePressEvent = self.mouse_press_event
        self.top_bar.mouseMoveEvent = self.mouse_move_event
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def send_message(self):
        msg = self.entry.text().strip()
        if msg:
            self.chat_area.append(f"<b>Вы:</b> {msg}")
            self.entry.clear()
            threading.Thread(target=self.get_response, args=(msg,)).start()

    def get_response(self, msg):
        response = ask_bb(msg)
        self.chat_area.append(f"<b>BB:</b> {response}\n")
        threading.Thread(target=self.speak, args=(response,)).start()

    # Голосовой ввод 
    def start_voice_input(self):
        threading.Thread(target=self.voice_input_thread).start()

    def voice_input_thread(self):
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                self.chat_area.append("<b>BB:</b> Слушаю...")
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio, language="ru-RU")
                self.chat_area.append(f"<b>Вы:</b> {text}")
                threading.Thread(target=self.get_response, args=(text,)).start()
        except Exception as e:
            self.chat_area.append(f"<b>BB:</b> Ошибка распознавания: {str(e)}\n")

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def mouse_press_event(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.offset = event.position()

    def mouse_move_event(self, event):
        if self.offset is not None:
            x = event.globalPosition().x() - self.offset.x()
            y = event.globalPosition().y() - self.offset.y()
            self.move(int(x), int(y))

    def mouseReleaseEvent(self, event):
        self.offset = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BBChatApp()
    window.show()
    sys.exit(app.exec())
