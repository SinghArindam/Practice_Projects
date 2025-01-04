import os
import sys
import shutil
from cryptography.fernet import Fernet
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QSlider, QLineEdit, QStackedWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.title = QLabel("SPOTIFY CLONE", alignment=Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; padding: 20px;")

        self.home_button = QPushButton("Home")
        self.library_button = QPushButton("Library")
        self.search_button = QPushButton("Search")
        self.settings_button = QPushButton("Settings")

        buttons = [self.home_button, self.library_button, self.search_button, self.settings_button]
        for button in buttons:
            button.setStyleSheet("background-color: #1DB954; color: white; border: none; padding: 10px; font-size: 16px; margin-bottom: 10px;")
            button.setCursor(Qt.PointingHandCursor)

        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.home_button)
        layout.addWidget(self.library_button)
        layout.addWidget(self.search_button)
        layout.addWidget(self.settings_button)
        layout.addStretch()

        self.setLayout(layout)

class CentralArea(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search for songs, artists, or albums...")
        self.search_bar.setStyleSheet("background-color: #282828; color: white; padding: 10px; font-size: 16px; margin: 10px; border: none;")

        self.file_list_label = QLabel("Your Music Files")
        self.file_list_label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        self.file_list_label.setAlignment(Qt.AlignCenter)

        self.file_list = QListWidget()
        self.file_list.setStyleSheet("background-color: #282828; color: white; border: none; padding: 10px; font-size: 16px;")

        self.encrypt_button = QPushButton("Encrypt and Move Files")
        self.encrypt_button.setStyleSheet("background-color: #1DB954; color: white; border-radius: 5px; padding: 10px; font-size: 16px;")
        self.encrypt_button.setCursor(Qt.PointingHandCursor)

        layout.addWidget(self.search_bar)
        layout.addWidget(self.file_list_label)
        layout.addWidget(self.file_list)
        layout.addWidget(self.encrypt_button)

        self.setLayout(layout)

        self.load_music_files()
        self.encrypt_button.clicked.connect(self.encrypt_and_move_files)

    def load_music_files(self, folder="music"):
        self.file_list.clear()
        if not os.path.exists(folder):
            os.makedirs(folder)
        for file in os.listdir(folder):
            if file.endswith(".mp3") or file.endswith(".wav"):
                self.file_list.addItem(file)

    def encrypt_and_move_files(self, source_folder="music", dest_folder="encrypted"):
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        key = Fernet.generate_key()
        cipher = Fernet(key)

        with open(os.path.join(dest_folder, "encryption_key.key"), "wb") as key_file:
            key_file.write(key)

        for file in os.listdir(source_folder):
            if file.endswith(".mp3") or file.endswith(".wav"):
                source_path = os.path.join(source_folder, file)
                dest_path = os.path.join(dest_folder, file)

                with open(source_path, "rb") as f:
                    encrypted_data = cipher.encrypt(f.read())

                with open(dest_path, "wb") as f:
                    f.write(encrypted_data)

                os.remove(source_path)

        self.load_music_files(dest_folder)

class MediaPlayer(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        controls_layout = QHBoxLayout()

        self.previous_button = QPushButton("Previous")
        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        self.next_button = QPushButton("Next")

        buttons = [self.previous_button, self.play_button, self.pause_button, self.next_button]
        for button in buttons:
            button.setStyleSheet("background-color: #1DB954; color: white; border-radius: 5px; padding: 10px; font-size: 16px;")
            button.setCursor(Qt.PointingHandCursor)

        controls_layout.addWidget(self.previous_button)
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.pause_button)
        controls_layout.addWidget(self.next_button)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.volume_slider.setToolTip("Volume")
        self.volume_slider.setStyleSheet("background-color: #282828; color: white; padding: 5px; margin: 10px;")

        layout.addLayout(controls_layout)
        layout.addWidget(QLabel("Volume", alignment=Qt.AlignCenter))
        layout.addWidget(self.volume_slider)

        self.setLayout(layout)

class SpotifyClone(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spotify Clone")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #121212; color: white;")

        # Main Widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Main Layout
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # Components
        self.sidebar = Sidebar()
        self.central_area = CentralArea()
        self.media_player = MediaPlayer()

        # Central Stack for future navigation
        self.central_stack = QStackedWidget()
        self.central_stack.addWidget(self.central_area)

        # Add components to layout
        main_layout.addWidget(self.sidebar, 1)
        main_layout.addWidget(self.central_stack, 3)
        main_layout.addWidget(self.media_player, 2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpotifyClone()
    window.show()
    sys.exit(app.exec())
