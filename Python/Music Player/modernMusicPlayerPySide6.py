import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QFileDialog, QHBoxLayout
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFont


class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Music Player")
        self.setGeometry(200, 200, 500, 300)

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

        # Widgets
        self.label = QLabel("No file loaded", alignment=Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 16))
        self.layout.addWidget(self.label)

        self.load_button = QPushButton("Load File")
        self.load_button.setIcon(QIcon.fromTheme("document-open"))
        self.load_button.clicked.connect(self.load_file)
        self.layout.addWidget(self.load_button)

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

    def load_file(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(
            self, "Open Audio File", "", "Audio Files (*.mp3 *.wav *.ogg *.flac)"
        )
        if file_path:
            self.media_player.setSource(file_path)
            self.label.setText(f"Loaded: {file_path.split('/')[-1]}")

    def play_music(self):
        if self.media_player.mediaStatus() == QMediaPlayer.NoMedia:
            self.label.setText("No file loaded")
            return
        self.media_player.play()
        self.label.setText("Playing...")

    def pause_music(self):
        self.media_player.pause()
        self.label.setText("Paused")

    def stop_music(self):
        self.media_player.stop()
        self.label.setText("Stopped")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Modern Music Player")
    window = MusicPlayer()
    window.show()
    sys.exit(app.exec())