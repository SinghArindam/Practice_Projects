import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QSlider, QListWidget, QHBoxLayout
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from PySide6.QtGui import QIcon, QFont


class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Music Player with File List")
        self.setGeometry(200, 200, 600, 400)

        # Set modern stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
            }
            QLabel {
                color: #ecf0f1;
                font-size: 18px;
                font-family: Arial, sans-serif;
            }
            QListWidget {
                background-color: #34495e;
                color: #ecf0f1;
                border: 2px solid #1abc9c;
                border-radius: 10px;
                padding: 5px;
                font-size: 14px;
                font-family: Arial, sans-serif;
            }
            QPushButton {
                background-color: #34495e;
                color: #ecf0f1;
                border: 2px solid #1abc9c;
                border-radius: 10px;
                font-size: 14px;
                font-family: Arial, sans-serif;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1abc9c;
                color: #2c3e50;
            }
            QSlider::groove:horizontal {
                background: #34495e;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #1abc9c;
                border: 1px solid #1abc9c;
                width: 14px;
                height: 14px;
                margin: -3px 0;
                border-radius: 7px;
            }
        """)

        # Create main widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layouts
        self.layout = QVBoxLayout(self.central_widget)
        self.button_layout = QHBoxLayout()

        # Media Player
        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

        # File list widget
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.load_file)
        self.layout.addWidget(self.file_list)

        # Load files from the "music" directory
        self.load_files()

        # Widgets
        self.label = QLabel("No file selected", alignment=Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 16))
        self.layout.addWidget(self.label)

        self.animation_label = QLabel("🎵", alignment=Qt.AlignCenter)
        self.animation_label.setFont(QFont("Arial", 48))
        self.layout.addWidget(self.animation_label)

        # Slider for seeking
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.sliderMoved.connect(self.set_position)
        self.layout.addWidget(self.slider)

        # Playback buttons with icons
        self.play_button = QPushButton("Play")
        self.play_button.setIcon(QIcon.fromTheme("media-playback-start"))
        self.play_button.clicked.connect(self.play_music)

        self.pause_button = QPushButton("Pause")
        self.pause_button.setIcon(QIcon.fromTheme("media-playback-pause"))
        self.pause_button.clicked.connect(self.pause_music)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setIcon(QIcon.fromTheme("media-playback-stop"))
        self.stop_button.clicked.connect(self.stop_music)

        # Add buttons to horizontal layout
        self.button_layout.addWidget(self.play_button)
        self.button_layout.addWidget(self.pause_button)
        self.button_layout.addWidget(self.stop_button)

        self.layout.addLayout(self.button_layout)

        # Timer for updating the slider and animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_slider)

        # Animation for playing
        self.animation = QPropertyAnimation(self.animation_label, b"geometry")
        self.animation.setDuration(1000)
        self.animation.setStartValue(QRect(200, 150, 100, 50))
        self.animation.setEndValue(QRect(300, 150, 100, 50))
        self.animation.setLoopCount(-1)

    def load_files(self):
        """Load audio files from the 'files' directory into the list widget."""
        files_dir = os.path.join(os.path.dirname(__file__), "music")
        if not os.path.exists(files_dir):
            os.makedirs(files_dir)  # Create the directory if it doesn't exist

        audio_extensions = (".mp3", ".wav", ".ogg", ".flac")
        files = [f for f in os.listdir(files_dir) if f.lower().endswith(audio_extensions)]

        if files:
            for file in files:
                self.file_list.addItem(file)
        else:
            self.file_list.addItem("No audio files found in 'files' directory")

    def load_file(self, item):
        """Load the selected file into the media player."""
        files_dir = os.path.join(os.path.dirname(__file__), "files")
        file_path = os.path.join(files_dir, item.text())
        self.media_player.setSource(file_path)
        self.label.setText(f"Loaded: {item.text()}")

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
            self.slider.setValue(self.media_player.position() // 1000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Music Player with File List")
    window = MusicPlayer()
    window.show()
    sys.exit(app.exec())