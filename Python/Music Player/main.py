import os
import sys
import threading
from cryptography.fernet import Fernet, InvalidToken
import pygame
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QSlider,
    QListWidget, QHBoxLayout, QGridLayout
)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from PySide6.QtGui import QIcon, QFont


class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Music Player with Encryption")
        self.setGeometry(200, 200, 800, 600)

        # Setup encryption key
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

        # Initialize pygame mixer
        pygame.mixer.init()

        # Main widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Grid layout for file lists and buttons
        self.grid_layout = QGridLayout()

        # Left list: Music folder
        self.left_list_label = QLabel("Music Folder Files")
        self.left_list = QListWidget()
        self.grid_layout.addWidget(self.left_list_label, 0, 0)
        self.grid_layout.addWidget(self.left_list, 1, 0)

        # Right list: Encrypted folder
        self.right_list_label = QLabel("Encrypted Folder Files")
        self.right_list = QListWidget()
        self.right_list.itemClicked.connect(self.decrypt_and_load_file)
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

        # Label for status
        self.label = QLabel("No file selected", alignment=Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 16))
        self.layout.addWidget(self.label)

        # Current time and total duration display
        self.time_label = QLabel("0:00 / 0:00", alignment=Qt.AlignCenter)
        self.layout.addWidget(self.time_label)

        # Slider for controlling playback position
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.valueChanged.connect(self.slider_changed)
        self.layout.addWidget(self.slider)

        # Playback buttons
        self.button_layout = QHBoxLayout()
        self.play_button = QPushButton("Play")
        self.play_button.setIcon(QIcon.fromTheme("media-playback-start"))
        self.play_button.clicked.connect(self.play_music)

        self.pause_button = QPushButton("Pause")
        self.pause_button.setIcon(QIcon.fromTheme("media-playback-pause"))
        self.pause_button.clicked.connect(self.pause_resume_music)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setIcon(QIcon.fromTheme("media-playback-stop"))
        self.stop_button.clicked.connect(self.stop_music)

        self.button_layout.addWidget(self.play_button)
        self.button_layout.addWidget(self.pause_button)
        self.button_layout.addWidget(self.stop_button)
        self.layout.addLayout(self.button_layout)

        # Timer for updating slider and time
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_slider)
        self.animation = QPropertyAnimation(self.label, b"geometry")
        self.animation.setDuration(1000)
        self.animation.setStartValue(QRect(200, 150, 100, 50))
        self.animation.setEndValue(QRect(300, 150, 100, 50))
        self.animation.setLoopCount(-1)

        # Refresh lists
        self.refresh_lists()

    def setup_encryption_key(self):
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
        selected_item = self.left_list.currentItem()
        if not selected_item:
            return

        music_folder = os.path.join(os.path.dirname(__file__), "music")
        encrypted_folder = os.path.join(os.path.dirname(__file__), "encrypted")

        source_path = os.path.join(music_folder, selected_item.text())
        encrypted_path = os.path.join(encrypted_folder, f"{selected_item.text()}.enc")

        if not os.path.exists(source_path):
            return

        with open(source_path, "rb") as f:
            data = f.read()
        encrypted_data = self.cipher.encrypt(data)

        with open(encrypted_path, "wb") as f:
            f.write(encrypted_data)

        self.refresh_lists()

    def decrypt_and_load_file(self, item):
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
            self.current_file = decrypted_path
            self.label.setText(f"Loaded: {item.text().replace('.enc', '')}")
        except InvalidToken:
            self.label.setText("Invalid or corrupted file.")

    def update_slider(self):
        if pygame.mixer.music.get_busy():
            current_pos = pygame.mixer.music.get_pos() // 1000
            self.slider.setValue(current_pos)

            song_length = pygame.mixer.Sound(self.current_file).get_length()
            current_time = current_pos
            self.time_label.setText(f"{self.format_time(current_time)} / {self.format_time(song_length)}")

    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        seconds = int(seconds)
        return f"{minutes}:{str(seconds)}"

    def play_music(self):
        """Play the selected music file."""
        if not hasattr(self, 'current_file'):
            print("[ERROR] No file selected.")
            return

        pygame.mixer.music.load(self.current_file)
        pygame.mixer.music.play()
        def self_timer_start(t):
            self.timer.start(1000)#pdate every second
        threading.Thread(target=self_timer_start, args=1000).start()
        self.play_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        print(f"[DEBUG] Playing: {self.current_file}")

    def pause_resume_music(self):
        """Pause and resume the music."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.pause_button.setText("Resume")
            print("[DEBUG] Paused playback.")
        else:
            pygame.mixer.music.unpause()
            self.pause_button.setText("Pause")
            print("[DEBUG] Resumed playback.")

    def stop_music(self):
        """Stop the music."""
        pygame.mixer.music.stop()
        self.timer.stop()
        self.slider.setValue(0)
        self.time_label.setText("0:00 / 0:00")
        self.play_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.pause_button.setText("Pause")
        print("[DEBUG] Stopped playback.")

    def slider_changed(self):
        """Sync slider with music playback."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_pos(self.slider.value())
            print(f"[DEBUG] Slider moved to: {self.slider.value()}")

    def closeEvent(self, event):
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
