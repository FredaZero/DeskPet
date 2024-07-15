from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QMenu, QSystemTrayIcon, QGraphicsPixmapItem, QGraphicsItem, QVBoxLayout, QGridLayout
from PyQt6.QtGui import QIcon, QPixmap, QMovie, QAction, QImage, QTransform
from PyQt6.QtCore import  Qt, QTimer, QObject, QPoint, QUrl, QEvent, QRectF, QRect, QSize, QThread, pyqtSignal
import sys
import openai as openai
import os
import gtts
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import *
from dotenv import load_dotenv
from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QPlainTextEdit, \
    QLineEdit
from playsound import playsound
######
## Chat Function
######
chat_log: None


# Chatbox class/gui for Clippy
class ClippyChat(QWidget):
    def __init__(self):
        super(ClippyChat, self).__init__()
        # Load dot env file and pass API key to open.ai
        self.layout = None
        self.info_sentence = None
        self.chat_box = None
        self.input_txt = None
        self.send_button = None
        self.sound_button = None
        self.think_label = None
        self.worker = None
        self.worker_speak = None
        self.d = None
        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        self.player.mediaStatusChanged.connect(self.player_status_callback)

        # self._player.errorOccurred.connect(self._player_error)
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        print(openai.api_key)

        # NoNo's chat log
        global chat_log
        chat_log = [{"role": "system", "content": "You are a helpful and kind assistant on your master's daily work, "
                                                  "specifically you are Super 'NoNo' Robot with code name: Naib from Cruise Seer. "
                                                  "Also, you are designed based on the personality of a young mercenary, try to be accurate, direct, tactiturn and caring."
                                                  "play together"}]

        # Bool for NoNo's talking animation
        self.talking = False

        # Initialize the UI
        self.init_ui()

    def init_ui(self):
        self.layout = QGridLayout(self)
        self.info_sentence = QLabel("Let's Have a chat!", self)
        self.chat_box = QPlainTextEdit(self)
        self.chat_box.setReadOnly(True)
        self.input_txt = QLineEdit(self)
        self.input_txt.setFocus()
        self.input_txt.returnPressed.connect(self.send_to_gpt)
        self.input_txt.setPlaceholderText("Ask a question!")
        self.send_button = QPushButton('send', self)
        # Mute Button
        self.sound_button = QPushButton('', self)
        self.sound_button.setStyleSheet("border-image: url(../img/sound.png);")
        self.sound_button.setFixedSize(30, 30)
        self.sound_button.setCheckable(True)
        self.sound_button.clicked.connect(self.change_sound_style)

        # Send Question to chat GPT
        self.send_button.clicked.connect(self.send_to_gpt)
        self.think_label = QLabel("Listening ... ", self)

        # Add widgets to grid
        self.layout.addWidget(self.sound_button, 0, 1)
        self.layout.addWidget(self.info_sentence, 0, 0)
        self.layout.addWidget(self.chat_box, 1, 0, 2, 2)
        self.layout.addWidget(self.input_txt, 4, 0)
        self.layout.addWidget(self.send_button, 4, 1)
        self.layout.addWidget(self.think_label, 3, 0, 1, 1)
        self.setLayout(self.layout)

    # Changes the sound button styling to match the state
    def change_sound_style(self):
        if self.sound_button.isChecked():
            self.sound_button.setStyleSheet("border-image: url(../img/silent.png);")
            self.audio_output.setVolume(0)
        else:
            self.sound_button.setStyleSheet("border-image: url(../img/sound.png);")
            self.audio_output.setVolume(50)

    # Sends text from input to Chat GPT
    def send_to_gpt(self):
        question = self.input_txt.text()
        chat_log.append({"role": "user", "content": question})
        # Thread to allow gui to function while it queries chatGPT
        self.worker = Type()
        self.worker.gpt_result.connect(self.complete)
        self.chat_box.appendHtml("<b>You: </b>" + question)
        self.input_txt.clear()
        # Disable buttons to user doesn't overwhelm chatGPT
        self.input_txt.setDisabled(True)
        self.send_button.setDisabled(True)
        self.think_label.setText("Thinking ...")
        self.worker.start()

    """
    Callback function for worker thread that's sending and receiving data from chatgpt api
    Re enables the buttons
    Appends ChatGPT text to chat box
    Starts another thread for speaking
    Set talking boolean for chatting animation
    """

    def complete(self, ai_response_msg):
        self.input_txt.setFocus()
        self.chat_box.appendHtml("<b>Naib: </b>" + ai_response_msg)

        # check if mute button is active
        if not self.sound_button.isChecked():
            self.worker_speak = LoadReply(ai_response_msg)
            self.worker_speak.done_loading_reply.connect(self.done_loading_sound)
            self.worker_speak.start()
        else:
            self.think_label.setText("Talking (telepathically)...")
            self.input_txt.setDisabled(False)
            self.send_button.setDisabled(False)

    # Callback for speech worker
    def done_loading_sound(self):
        self.think_label.setText("Listening ...")
        self.player.setSource(QUrl.fromLocalFile("../audio/talk2.m4a"))
        self.player.play()
        self.input_txt.setDisabled(False)
        self.send_button.setDisabled(False)

    def player_status_callback(self, status):
        if status == QMediaPlayer.MediaStatus.BufferedMedia:
            self.talking = True
            self.think_label.setText("Talking ...")
        else:
            self.talking = False
            self.think_label.setText("Listening ...")


# Thread for ChatGPT inquiries
class Type(QThread):
    gpt_result = pyqtSignal(object)

    def __init__(self):
        super(QThread, self).__init__()

    def run(self):
        ai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_log,
            temperature=.9
        )
        # parse for the response text
        ai_response_msg = ai_response['choices'][0]['message']['content']
        chat_log.append({"role": "assistant", "content": ai_response_msg})
        self.gpt_result.emit(ai_response_msg)

    # Thread for speaking
class LoadReply(QThread):
    done_loading_reply = pyqtSignal()

    def __init__(self, reply):
        super(QThread, self).__init__()
        pyqtSignal()
        self.reply = reply

    # Plays Audio received from gTTS
    def run(self):
        tts = gtts.gTTS(self.reply)
        tts.save("../audio/talk3.m4a")
        self.done_loading_reply.emit()



class ClothesChange(QWidget):
    def __init__(self, change_outfit_callback):
        super(ClothesChange, self).__init__()
        self.change_outfit_callback = change_outfit_callback
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Change Clothes")
        self.setGeometry(100, 100, 300, 400)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(self)

        # Title label
        title = QLabel("Select an Outfit", self)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Grid layout for outfits
        grid_layout = QGridLayout()
        outfit_icons = ["../img/Naib_outfit.png", " ", " ", " "]
        self.buttons = []

        positions = [(i, j) for i in range(2) for j in range(2)]
        for position, outfit_icon in zip(positions, outfit_icons):
            button = QPushButton(self)
            if outfit_icon != " ":
                button.setIcon(QIcon(outfit_icon))
                button.setIconSize(QSize(80, 80))
            button.setFixedSize(QSize(100, 100))
            button.setStyleSheet("border-image: url('img/SelectBox_NotChose.png');")
            button.clicked.connect(lambda checked, btn=button, icon=outfit_icon: self.on_button_click(btn,icon))
            grid_layout.addWidget(button, *position)
            self.buttons.append(button)

        layout.addLayout(grid_layout)

        # Close button
        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    
    def on_button_click(self, button, icon):
        for btn in self.buttons:
            btn.setStyleSheet("border-image: url('../img/SelectBox_NotChose.png');")
        button.setStyleSheet("border-image: url('../img/SelectBox_Chose.png');")
        self.change_outfit_callback(icon)