import os
import sys
from cryptography.fernet import Fernet, InvalidToken
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QSlider,
    QListWidget, QHBoxLayout, QGridLayout
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from PySide6.QtGui import QIcon, QFont


class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Music Player with Encryption")
        self.setGeometry(200, 200, 800, 400)

        # Set up encryption key
        self.setup_encryption_key()

        # Set modern stylesheet
        self.setStyleSheet("""
            QMainWindow { background-color: #2c3e50; }
            QLabel { color: #ecf0f1; font-size: 18px; font-family: Arial, sans-serif; }
            QListWidget { background-color: #34495e; color: #ecf0f1; border: 2px solid #1abc9c; border-radius: 10px; padding: 5px; }
            QPushButton { background-color: #34495e; color: #ecf0f1; border: 2px solid #1abc9c; border-radius: 10px; padding: 10px; }
            QPushButton:hover { background-color: #1abc9c; color: #2c3e50; }
            QSlider::groove:horizontal { background: #34495e; height: 8px; border-radius: 4px; }
            QSlider::handle:horizontal { background: #1abc9c; width: 14px; height: 14px; margin: -3px 0; border-radius: 7px; }
        """)

        # Main widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.button_layout = QHBoxLayout()

        # Grid layout for lists and buttons
        self.grid_layout = QGridLayout()

        # Left list: Music folder
        self.left_list_label = QLabel("Music Folder Files")
        self.left_list = QListWidget()
        self.grid_layout.addWidget(self.left_list_label, 0, 0)
        self.grid_layout.addWidget(self.left_list, 1, 0)

        # Right list: Encrypted folder
        self.right_list_label = QLabel("Encrypted Folder Files")
        self.right_list = QListWidget()
        self.grid_layout.addWidget(self.right_list_label, 0, 2)
        self.grid_layout.addWidget(self.right_list, 1, 2)

        # Buttons
        self.encrypt_button = QPushButton("Encrypt Selected File")
        self.encrypt_button.clicked.connect(self.encrypt_selected_file)
        self.grid_layout.addWidget(self.encrypt_button, 2, 0)

        self.refresh_button = QPushButton("Refresh Lists")
        self.refresh_button.clicked.connect(self.refresh_lists)
        self.grid_layout.addWidget(self.refresh_button, 2, 2)

        self.layout.addLayout(self.grid_layout)

        # Media player setup
        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

        # Timer and animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_slider)

        # Load files into lists
        self.refresh_lists()

    def setup_encryption_key(self):
        """Setup encryption key, saving it if not already present."""
        key_path = os.path.join(os.path.dirname(__file__), "encryption.key")
        if os.path.exists(key_path):
            with open(key_path, "rb") as key_file:
                self.encryption_key = key_file.read()
        else:
            self.encryption_key = Fernet.generate_key()
            with open(key_path, "wb") as key_file:
                key_file.write(self.encryption_key)
        self.cipher = Fernet(self.encryption_key)

    def refresh_lists(self):
        """Refresh the file lists for music and encrypted folders."""
        self.left_list.clear()
        self.right_list.clear()

        music_folder = os.path.join(os.path.dirname(__file__), "music")
        encrypted_folder = os.path.join(os.path.dirname(__file__), "encrypted")
        os.makedirs(music_folder, exist_ok=True)
        os.makedirs(encrypted_folder, exist_ok=True)

        music_files = [f for f in os.listdir(music_folder) if f.lower().endswith((".mp3", ".wav", ".ogg", ".flac"))]
        encrypted_files = [f for f in os.listdir(encrypted_folder) if f.endswith(".enc")]

        self.left_list.addItems(music_files)
        self.right_list.addItems(encrypted_files)

    def encrypt_selected_file(self):
        """Encrypt the selected file from the left list and add it to the right list."""
        selected_item = self.left_list.currentItem()
        if not selected_item:
            return

        music_folder = os.path.join(os.path.dirname(__file__), "music")
        encrypted_folder = os.path.join(os.path.dirname(__file__), "encrypted")

        source_path = os.path.join(music_folder, selected_item.text())
        encrypted_path = os.path.join(encrypted_folder, f"{selected_item.text()}.enc")

        if not os.path.exists(source_path):
            return

        # Encrypt file
        with open(source_path, "rb") as f:
            data = f.read()
        encrypted_data = self.cipher.encrypt(data)

        with open(encrypted_path, "wb") as f:
            f.write(encrypted_data)

        self.refresh_lists()

    def update_slider(self):
        """Update slider position based on the media player's position."""
        if self.media_player.duration() > 0:
            position = self.media_player.position() // 1000  # Convert milliseconds to seconds
            self.slider.setValue(position)

    def play_music(self):
        """Start playing the selected music file."""
        if self.media_player.mediaStatus() == QMediaPlayer.NoMedia:
            self.label.setText("No file loaded")
            return
        self.media_player.play()
        self.label.setText("Playing...")
        self.timer.start(1000)

    def pause_music(self):
        """Pause the music."""
        self.media_player.pause()
        self.label.setText("Paused")
        self.timer.stop()

    def stop_music(self):
        """Stop the music."""
        self.media_player.stop()
        self.label.setText("Stopped")
        self.timer.stop()
        self.slider.setValue(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Music Player with Encryption")
    window = MusicPlayer()
    window.show()
    sys.exit(app.exec())
