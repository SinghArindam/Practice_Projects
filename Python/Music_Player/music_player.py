import os
import sys
import time
import threading
import tempfile
import pickle
import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk
import pygame
from mutagen.mp3 import MP3  # adjust if you use other formats
from cryptography.fernet import Fernet

# Directories and database filename
AUDIO_DIR = "./audio"
DB_FILE = "db"
KEY_FILE = "secret.key"

# Ensure the audio directory exists
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

# Load or generate the encryption key
def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key

key = load_key()
fernet = Fernet(key)

# Load or initialize the database mapping {encrypted_filename: original_filename}
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "rb") as f:
            return pickle.load(f)
    else:
        return {}

db = load_db()

def save_db():
    with open(DB_FILE, "wb") as f:
        pickle.dump(db, f)

# Function to encrypt an audio file and save it into AUDIO_DIR
def encrypt_and_store(filepath):
    # Read file bytes
    with open(filepath, "rb") as f:
        data = f.read()
    # Encrypt the data
    encrypted_data = fernet.encrypt(data)
    # Encrypt the filename (using only the basename)
    original_name = os.path.basename(filepath)
    encrypted_name = fernet.encrypt(original_name.encode()).decode()  # store as string
    # Use encrypted name as the new filename (no extension – we will remember extension separately)
    # To play the file later, we need the extension. We could store it in the db.
    # For simplicity, we assume the extension is part of the original name.
    new_filename = encrypted_name  # we store the file with this name
    dest_path = os.path.join(AUDIO_DIR, new_filename)
    # Write the encrypted data to the destination file
    with open(dest_path, "wb") as f:
        f.write(encrypted_data)
    # Update the database mapping: key = encrypted filename, value = original filename
    db[new_filename] = original_name
    save_db()

# Function to decrypt an encrypted audio file into a temporary file and return its path
def decrypt_to_temp(encrypted_filename):
    enc_path = os.path.join(AUDIO_DIR, encrypted_filename)
    with open(enc_path, "rb") as f:
        encrypted_data = f.read()
    # Decrypt the data
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except Exception as e:
        print("Decryption error:", e)
        return None
    # Determine file extension from the original filename stored in db
    original_name = db.get(encrypted_filename, "temp.mp3")
    _, ext = os.path.splitext(original_name)
    # Create a temporary file with the proper extension
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    temp_file.write(decrypted_data)
    temp_file.close()
    return temp_file.name

# Initialize pygame mixer
pygame.mixer.init()

# Main application class
class MusicPlayer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Encrypted Music Player")
        self.geometry("800x500")
        
        # Currently playing file info
        self.current_file = None
        self.current_tempfile = None
        self.total_length = 0  # in seconds
        self.playing = False
        self.paused = False
        self.start_time = 0  # time when playback started/resumed
        self.pause_time = 0  # time at which paused
        
        # Left frame for list and add file button
        self.left_frame = ctk.CTkFrame(self, width=250)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        self.file_listbox = tk.Listbox(self.left_frame, width=30, height=20)
        self.file_listbox.pack(padx=10, pady=10)
        self.file_listbox.bind("<<ListboxSelect>>", self.on_file_select)
        
        self.add_file_button = ctk.CTkButton(self.left_frame, text="Add File", command=self.add_file)
        self.add_file_button.pack(padx=10, pady=(0,10))
        
        # Right frame for controls and progress bar
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Control buttons
        self.btn_frame = ctk.CTkFrame(self.right_frame)
        self.btn_frame.pack(pady=10)
        
        self.play_button = ctk.CTkButton(self.btn_frame, text="Play", command=self.play)
        self.play_button.grid(row=0, column=0, padx=5)
        
        self.pause_button = ctk.CTkButton(self.btn_frame, text="Pause", command=self.pause)
        self.pause_button.grid(row=0, column=1, padx=5)
        
        self.resume_button = ctk.CTkButton(self.btn_frame, text="Resume", command=self.resume)
        self.resume_button.grid(row=0, column=2, padx=5)
        
        self.stop_button = ctk.CTkButton(self.btn_frame, text="Stop", command=self.stop)
        self.stop_button.grid(row=0, column=3, padx=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progressbar = ctk.CTkProgressBar(self.right_frame, variable=self.progress_var)
        self.progressbar.set(0)
        self.progressbar.pack(fill="x", padx=20, pady=20)
        # Bind a click event on the progress bar to seek
        self.progressbar.bind("<Button-1>", self.seek)
        
        # Load file list from db
        self.load_file_list()
        
        # Start thread for progress updates
        self.updating = True
        threading.Thread(target=self.update_progress, daemon=True).start()
    
    def load_file_list(self):
        self.file_listbox.delete(0, tk.END)
        for enc_filename, orig_filename in db.items():
            self.file_listbox.insert(tk.END, orig_filename)
    
    def add_file(self):
        file_path = filedialog.askopenfilename(title="Select an audio file",
                                               filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
        if file_path:
            encrypt_and_store(file_path)
            self.load_file_list()
    
    def on_file_select(self, event):
        if self.file_listbox.curselection():
            index = self.file_listbox.curselection()[0]
            # Find the encrypted filename that corresponds to the selected original filename
            selected_orig = self.file_listbox.get(index)
            for enc, orig in db.items():
                if orig == selected_orig:
                    self.current_file = enc
                    break
            # Auto-play on selection (optional)
            self.stop()  # stop any current playback
            self.play()
    
    def play(self):
        if self.current_file is None:
            return
        # Decrypt file into a temporary file
        temp_path = decrypt_to_temp(self.current_file)
        if temp_path is None:
            print("Error decrypting file")
            return
        self.current_tempfile = temp_path
        
        # Load the audio file in pygame
        try:
            pygame.mixer.music.load(temp_path)
        except Exception as e:
            print("Error loading file:", e)
            return
        
        # Use mutagen to get total length (assumes MP3; adjust accordingly for other formats)
        try:
            audio = MP3(temp_path)
            self.total_length = audio.info.length
        except Exception as e:
            print("Error reading audio length:", e)
            self.total_length = 0
        
        pygame.mixer.music.play(loops=0)
        self.start_time = time.time()
        self.playing = True
        self.paused = False
    
    def pause(self):
        if self.playing and not self.paused:
            pygame.mixer.music.pause()
            self.pause_time = time.time()
            self.paused = True
    
    def resume(self):
        if self.playing and self.paused:
            pygame.mixer.music.unpause()
            # Adjust start_time to account for the pause duration
            pause_duration = time.time() - self.pause_time
            self.start_time += pause_duration
            self.paused = False
    
    def stop(self):
        if self.playing:
            pygame.mixer.music.stop()
            self.playing = False
            self.paused = False
            self.progress_var.set(0)
            # Clean up the temporary file if exists
            if self.current_tempfile and os.path.exists(self.current_tempfile):
                os.remove(self.current_tempfile)
                self.current_tempfile = None
    
    def update_progress(self):
        while self.updating:
            if self.playing and not self.paused and self.total_length > 0:
                elapsed = time.time() - self.start_time
                progress = min(elapsed / self.total_length, 1.0)
                self.progress_var.set(progress)
                # Auto-stop if playback finished
                if progress >= 1.0:
                    self.stop()
            time.sleep(0.5)
    
    def seek(self, event):
        if not (self.playing and self.total_length > 0):
            return
        # Determine the click position relative to the width of the progress bar
        widget_width = self.progressbar.winfo_width()
        click_x = event.x
        ratio = click_x / widget_width
        new_time = ratio * self.total_length  # seconds
        
        # To seek, we restart playback from the new time
        try:
            # Stop current playback
            pygame.mixer.music.stop()
            # Restart playback with new start time (pygame supports 'start' in seconds for MP3s)
            pygame.mixer.music.play(loops=0, start=new_time)
            self.start_time = time.time() - new_time
        except Exception as e:
            print("Seeking error:", e)
    
    def on_close(self):
        self.updating = False
        self.stop()
        self.destroy()

if __name__ == "__main__":
    app = MusicPlayer()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
