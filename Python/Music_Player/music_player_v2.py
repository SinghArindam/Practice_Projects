import os
import time
import threading
import tempfile
import pickle
import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk
import pygame
from mutagen.mp3 import MP3
from cryptography.fernet import Fernet

# ---------------------------
# Setup: directories, key & database
# ---------------------------
AUDIO_DIR = "./audio"
DB_FILE = "db"
KEY_FILE = "secret.key"

if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

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

# ---------------------------
# Encryption & Decryption Functions
# ---------------------------
def encrypt_and_store(filepath):
    # Read file bytes and encrypt
    with open(filepath, "rb") as f:
        data = f.read()
    encrypted_data = fernet.encrypt(data)
    original_name = os.path.basename(filepath)
    # Encrypt the filename (stored as string)
    encrypted_name = fernet.encrypt(original_name.encode()).decode()
    dest_path = os.path.join(AUDIO_DIR, encrypted_name)
    with open(dest_path, "wb") as f:
        f.write(encrypted_data)
    # Update the database mapping
    db[encrypted_name] = original_name
    save_db()
    return True

def decrypt_to_temp(encrypted_filename):
    enc_path = os.path.join(AUDIO_DIR, encrypted_filename)
    with open(enc_path, "rb") as f:
        encrypted_data = f.read()
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except Exception as e:
        print("Decryption error:", e)
        return None
    original_name = db.get(encrypted_filename, "temp.mp3")
    _, ext = os.path.splitext(original_name)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    temp_file.write(decrypted_data)
    temp_file.close()
    return temp_file.name

# ---------------------------
# Initialize pygame mixer
# ---------------------------
pygame.mixer.init()

# ---------------------------
# Main Application Class
# ---------------------------
class MusicPlayer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Encrypted Spotify-like Music Player")
        self.geometry("900x600")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Set default appearance (dark) and theme.
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.mode = "dark"  # track current mode
        
        # Header frame with title and light/dark toggle switch
        self.header_frame = ctk.CTkFrame(self, height=50)
        self.header_frame.pack(side="top", fill="x", padx=10, pady=(10, 0))
        self.title_label = ctk.CTkLabel(self.header_frame, text="Encrypted Music Player", font=("Helvetica", 20, "bold"))
        self.title_label.pack(side="left", padx=10)
        self.theme_switch = ctk.CTkSwitch(self.header_frame, text="Light Mode", command=self.toggle_theme)
        self.theme_switch.pack(side="right", padx=10)
        
        # Left frame: listbox for files and Add File button
        self.left_frame = ctk.CTkFrame(self, width=300)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.file_listbox = tk.Listbox(self.left_frame, width=30, height=20,
                                       bg="#2b2b2b", fg="white", font=("Helvetica", 12))
        self.file_listbox.pack(padx=10, pady=10, fill="both", expand=True)
        self.file_listbox.bind("<<ListboxSelect>>", self.on_file_select)
        self.add_file_button = ctk.CTkButton(self.left_frame, text="Add File", command=self.add_file)
        self.add_file_button.pack(padx=10, pady=(0, 10))
        
        # Right frame: playback controls and progress bar
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.controls_frame = ctk.CTkFrame(self.right_frame)
        self.controls_frame.pack(pady=20)
        self.play_button = ctk.CTkButton(self.controls_frame, text="Play", command=self.play)
        self.play_button.grid(row=0, column=0, padx=5)
        self.pause_button = ctk.CTkButton(self.controls_frame, text="Pause", command=self.pause)
        self.pause_button.grid(row=0, column=1, padx=5)
        self.resume_button = ctk.CTkButton(self.controls_frame, text="Resume", command=self.resume)
        self.resume_button.grid(row=0, column=2, padx=5)
        self.stop_button = ctk.CTkButton(self.controls_frame, text="Stop", command=self.stop)
        self.stop_button.grid(row=0, column=3, padx=5)
        
        # Progress bar for playback; click to seek
        self.progress_var = tk.DoubleVar()
        self.progressbar = ctk.CTkProgressBar(self.right_frame, variable=self.progress_var, width=600)
        self.progressbar.set(0)
        self.progressbar.pack(pady=20)
        self.progressbar.bind("<Button-1>", self.seek)
        
        # Internal playback state
        self.current_file = None
        self.current_tempfile = None
        self.total_length = 0  # in seconds
        self.playing = False
        self.paused = False
        self.start_time = 0  # when playback started/resumed
        self.pause_time = 0  # when playback paused
        
        self.load_file_list()
        self.updating = True
        threading.Thread(target=self.update_progress, daemon=True).start()
    
    # ---------------------------
    # Light/Dark Theme Toggle
    # ---------------------------
    def toggle_theme(self):
        if self.mode == "dark":
            ctk.set_appearance_mode("light")
            self.mode = "light"
            self.theme_switch.configure(text="Dark Mode")
        else:
            ctk.set_appearance_mode("dark")
            self.mode = "dark"
            self.theme_switch.configure(text="Light Mode")
    
    # ---------------------------
    # File List Management
    # ---------------------------
    def load_file_list(self):
        self.file_listbox.delete(0, tk.END)
        for enc_filename, orig_filename in db.items():
            self.file_listbox.insert(tk.END, orig_filename)
    
    def add_file(self):
        file_path = filedialog.askopenfilename(title="Select an audio file",
                                               filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
        if file_path:
            # Run encryption task with a progress dialog
            self.run_task_with_loading("Encrypting", "Encrypting file...", encrypt_and_store, self.after_encrypt, file_path)
    
    def after_encrypt(self, result):
        if result:
            self.load_file_list()
    
    def on_file_select(self, event):
        if self.file_listbox.curselection():
            index = self.file_listbox.curselection()[0]
            selected_orig = self.file_listbox.get(index)
            for enc, orig in db.items():
                if orig == selected_orig:
                    self.current_file = enc
                    break
            self.stop()  # stop current playback if any
            self.play()   # auto-play selected file
    
    # ---------------------------
    # Playback Controls
    # ---------------------------
    def play(self):
        if self.current_file is None:
            return
        # Run decryption with a progress dialog before playback
        self.run_task_with_loading("Decrypting", "Decrypting file...", lambda: decrypt_to_temp(self.current_file), self.after_decrypt)
    
    def after_decrypt(self, temp_path):
        if temp_path is None:
            print("Error decrypting file")
            return
        self.current_tempfile = temp_path
        try:
            pygame.mixer.music.load(temp_path)
        except Exception as e:
            print("Error loading file:", e)
            return
        # Use mutagen to get the track length (assumes MP3; adjust for other formats)
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
            self.start_time += time.time() - self.pause_time
            self.paused = False
    
    def stop(self):
        if self.playing:
            pygame.mixer.music.stop()
            self.playing = False
            self.paused = False
            self.progress_var.set(0)
            if self.current_tempfile and os.path.exists(self.current_tempfile):
                os.remove(self.current_tempfile)
                self.current_tempfile = None
    
    def update_progress(self):
        while self.updating:
            if self.playing and not self.paused and self.total_length > 0:
                elapsed = time.time() - self.start_time
                progress = min(elapsed / self.total_length, 1.0)
                self.progress_var.set(progress)
                if progress >= 1.0:
                    self.stop()
            time.sleep(0.5)
    
    def seek(self, event):
        if not (self.playing and self.total_length > 0):
            return
        widget_width = self.progressbar.winfo_width()
        click_x = event.x
        ratio = click_x / widget_width
        new_time = ratio * self.total_length
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.play(loops=0, start=new_time)
            self.start_time = time.time() - new_time
        except Exception as e:
            print("Seeking error:", e)
    
    # ---------------------------
    # Modal Progress Dialog for Tasks
    # ---------------------------
    def run_task_with_loading(self, title, message, task_func, callback, *args, **kwargs):
        progress_win = ctk.CTkToplevel(self)
        progress_win.title(title)
        progress_win.geometry("300x100")
        progress_win.grab_set()
        label = ctk.CTkLabel(progress_win, text=message)
        label.pack(pady=10)
        progress_bar = ctk.CTkProgressBar(progress_win)
        progress_bar.pack(pady=10, padx=20, fill="x")
        progress_bar.start()  # indeterminate progress
        
        def thread_target():
            result = task_func(*args, **kwargs)
            self.after(0, finish, result)
        
        def finish(result):
            progress_bar.stop()
            progress_win.destroy()
            callback(result)
        
        threading.Thread(target=thread_target, daemon=True).start()
    
    # ---------------------------
    # Cleanup on Exit
    # ---------------------------
    def on_close(self):
        self.updating = False
        self.stop()
        self.destroy()

# ---------------------------
# Run the Application
# ---------------------------
if __name__ == "__main__":
    app = MusicPlayer()
    app.mainloop()
