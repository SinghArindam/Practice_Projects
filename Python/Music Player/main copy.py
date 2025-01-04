import os
import sys
import pygame
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidget, QVBoxLayout, QWidget, QPushButton
from cryptography.fernet import Fernet, InvalidToken

class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize pygame mixer
        pygame.mixer.init()

        self.setWindowTitle("Music Player with Encryption")
        self.setGeometry(200, 200, 800, 400)

        # Set up encryption key
        self.setup_encryption_key()

        # UI setup
        self.setup_ui()

        # File paths
        self.current_file = None

    def setup_ui(self):
        """Set up the user interface."""
        self.setStyleSheet("""
            QMainWindow { background-color: #2c3e50; }
            QLabel { color: #ecf0f1; font-size: 18px; font-family: Arial, sans-serif; }
            QPushButton { background-color: #34495e; color: #ecf0f1; border: 2px solid #1abc9c; border-radius: 10px; padding: 10px; }
            QPushButton:hover { background-color: #1abc9c; color: #2c3e50; }
        """)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # File list widget
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.decrypt_and_load_file)
        self.layout.addWidget(self.file_list)

        # Playback buttons
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_music)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_music)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_music)

        self.layout.addWidget(self.play_button)
        self.layout.addWidget(self.pause_button)
        self.layout.addWidget(self.stop_button)

        # Load files
        self.load_files()

    def decrypt_and_load_file(self, item):
        """Decrypt and prepare the selected file for playback."""
        encrypted_folder = os.path.join(os.path.dirname(__file__), "encrypted")
        temp_folder = os.path.join(os.path.dirname(__file__), "temp")
        os.makedirs(temp_folder, exist_ok=True)

        encrypted_path = os.path.join(encrypted_folder, item.text())
        decrypted_path = os.path.join(temp_folder, item.text().replace(".enc", ""))

        try:
            # Decrypt the file
            with open(encrypted_path, "rb") as f:
                decrypted_data = self.cipher.decrypt(f.read())
            with open(decrypted_path, "wb") as f:
                f.write(decrypted_data)

            # Load the decrypted file into pygame
            if os.path.exists(decrypted_path):
                self.current_file = decrypted_path
                print(f"[DEBUG] Decrypted and loaded file: {decrypted_path}")
            else:
                print("[ERROR] Decrypted file not found.")
        except InvalidToken:
            print("[ERROR] Decryption failed: Invalid or corrupted file.")

    def play_music(self):
        """Play the selected music file."""
        if not self.current_file:
            print("[ERROR] No file selected.")
            return

        pygame.mixer.music.load(self.current_file)
        pygame.mixer.music.play()
        print(f"[DEBUG] Playing: {self.current_file}")

    def pause_music(self):
        """Pause the music."""
        pygame.mixer.music.pause()
        print("[DEBUG] Paused playback.")

    def stop_music(self):
        """Stop the music."""
        pygame.mixer.music.stop()
        print("[DEBUG] Stopped playback.")

    def load_files(self):
        """Load encrypted files into the list widget."""
        encrypted_folder = os.path.join(os.path.dirname(__file__), "encrypted")
        os.makedirs(encrypted_folder, exist_ok=True)

        encrypted_files = [f for f in os.listdir(encrypted_folder) if f.endswith(".enc")]
        self.file_list.addItems(encrypted_files)

    def setup_encryption_key(self):
        """Set up encryption key, saving it if not already present."""
        key_path = os.path.join(os.path.dirname(__file__), "encryption.key")
        if os.path.exists(key_path):
            with open(key_path, "rb") as key_file:
                self.encryption_key = key_file.read()
        else:
            self.encryption_key = Fernet.generate_key()
            with open(key_path, "wb") as key_file:
                key_file.write(self.encryption_key)
        self.cipher = Fernet(self.encryption_key)

    def closeEvent(self, event):
        """Clean up temporary files on exit."""
        temp_folder = os.path.join(os.path.dirname(__file__), "temp")
        if os.path.exists(temp_folder):
            import shutil
            shutil.rmtree(temp_folder)
        pygame.mixer.quit()  # Ensure pygame shuts down
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MusicPlayer()
    window.show()
    sys.exit(app.exec())
