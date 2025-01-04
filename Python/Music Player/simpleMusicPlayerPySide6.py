import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QFileDialog
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt


class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Music Player")
        self.setGeometry(200, 200, 400, 200)

        # Create main widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout
        self.layout = QVBoxLayout(self.central_widget)

        # Media Player
        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

        # Widgets
        self.label = QLabel("No file loaded", alignment=Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_music)
        self.layout.addWidget(self.play_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_music)
        self.layout.addWidget(self.pause_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_music)
        self.layout.addWidget(self.stop_button)

        self.load_button = QPushButton("Load File")
        self.load_button.clicked.connect(self.load_file)
        self.layout.addWidget(self.load_button)

    def load_file(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(
            self, "Open Audio File", "", "Audio Files (*.mp3 *.wav *.ogg *.flac)"
        )
        if file_path:
            self.media_player.setSource(file_path)
            self.label.setText(f"Loaded: {file_path}")

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
    window = MusicPlayer()
    window.show()
    sys.exit(app.exec())