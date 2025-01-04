import os
import sys
from cryptography.fernet import Fernet, InvalidToken
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QSlider, QListWidget, QHBoxLayout
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from PySide6.QtGui import QIcon, QFont


class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Music Player with Encryption")
        self.setGeometry(200, 200, 600, 400)

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

        # Media player setup
        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

        # File list widget
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.decrypt_and_load_file)
        self.layout.addWidget(self.file_list)

        # Load and encrypt files
        self.load_and_encrypt_files()

        # Widgets
        self.label = QLabel("No file selected", alignment=Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 16))
        self.layout.addWidget(self.label)

        self.animation_label = QLabel("🎵", alignment=Qt.AlignCenter)
        self.animation_label.setFont(QFont("Arial", 48))
        self.layout.addWidget(self.animation_label)

        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.sliderMoved.connect(self.set_position)
        self.layout.addWidget(self.slider)

        # Playback buttons
        self.play_button = QPushButton("Play")
        self.play_button.setIcon(QIcon.fromTheme("media-playback-start"))
        self.play_button.clicked.connect(self.play_music)

        self.pause_button = QPushButton("Pause")
        self.pause_button.setIcon(QIcon.fromTheme("media-playback-pause"))
        self.pause_button.clicked.connect(self.pause_music)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setIcon(QIcon.fromTheme("media-playback-stop"))
        self.stop_button.clicked.connect(self.stop_music)

        self.button_layout.addWidget(self.play_button)
        self.button_layout.addWidget(self.pause_button)
        self.button_layout.addWidget(self.stop_button)
        self.layout.addLayout(self.button_layout)

        # Timer and animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_slider)
        self.animation = QPropertyAnimation(self.animation_label, b"geometry")
        self.animation.setDuration(1000)
        self.animation.setStartValue(QRect(200, 150, 100, 50))
        self.animation.setEndValue(QRect(300, 150, 100, 50))
        self.animation.setLoopCount(-1)

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

    def load_and_encrypt_files(self):
        """Encrypt files in 'music' folder and populate the file list."""
        source_folder = os.path.join(os.path.dirname(__file__), "music")
        encrypted_folder = os.path.join(os.path.dirname(__file__), "encrypted")
        os.makedirs(source_folder, exist_ok=True)
        os.makedirs(encrypted_folder, exist_ok=True)

        for file in os.listdir(source_folder):
            if file.lower().endswith((".mp3", ".wav", ".ogg", ".flac")):
                source_path = os.path.join(source_folder, file)
                encrypted_path = os.path.join(encrypted_folder, f"{file}.enc")
                if not os.path.exists(encrypted_path):
                    with open(source_path, "rb") as f:
                        encrypted_data = self.cipher.encrypt(f.read())
                    with open(encrypted_path, "wb") as f:
                        f.write(encrypted_data)
                self.file_list.addItem(f"{file}.enc")

    def decrypt_and_load_file(self, item):
        """Decrypt and load the selected file."""
        encrypted_folder = os.path.join(os.path.dirname(__file__), "encrypted")
        temp_folder = os.path.join(os.path.dirname(__file__), "temp")
        os.makedirs(temp_folder, exist_ok=True)

        encrypted_path = os.path.join(encrypted_folder, item.text())
        decrypted_path = os.path.join(temp_folder, item.text().replace(".enc", ""))

        try:
            with open(encrypted_path, "rb") as f:
                decrypted_data = self.cipher.decrypt(f.read())
            with open(decrypted_path, "wb") as f:
                f.write(decrypted_data)
            self.media_player.setSource(decrypted_path)
            self.label.setText(f"Loaded: {item.text().replace('.enc', '')}")
        except InvalidToken:
            self.label.setText("Invalid or corrupted file.")

    def play_music(self):
        if self.media_player.mediaStatus() == QMediaPlayer.NoMedia:
            self.label.setText("No file loaded")
            return
        self.media_player.play()
        self.label.setText("Playing...")
        self.timer.start(1000)
        self.animation.start()

    def pause_music(self):
        self.media_player.pause()
        self.label.setText("Paused")
        self.timer.stop()
        self.animation.stop()

    def stop_music(self):
        self.media_player.stop()
        self.label.setText("Stopped")
        self.timer.stop()
        self.animation.stop()
        self.slider.setValue(0)

    def set_position(self, position):
        self.media_player.setPosition(position * 1000)

    def update_slider(self):
        if self.media_player.duration() > 0:
            position = self.media_player.position() // 1000
            duration = self.media_player.duration() // 1000
            self.slider.setValue(position)
            self.label.setText(f"Playing... {position}s / {duration}s")

    def closeEvent(self, event):
        """Clean up temporary files on exit."""
        temp_folder = os.path.join(os.path.dirname(__file__), "temp")
        if os.path.exists(temp_folder):
            import shutil
            shutil.rmtree(temp_folder)
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Music Player with Encryption")
    window = MusicPlayer()
    window.show()
    sys.exit(app.exec())
