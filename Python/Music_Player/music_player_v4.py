import os
import time
import threading
import tempfile
import pickle

import flet
from flet import (
    Page,
    Column,
    Row,
    ElevatedButton,
    ListView,
    ProgressBar,
    Container,
    FilePicker,
    FilePickerResultEvent,
    IconButton,
    icons,
)
import pygame
from mutagen.mp3 import MP3
from cryptography.fernet import Fernet

# Directories and database/key filenames
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

def encrypt_and_store(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    encrypted_data = fernet.encrypt(data)
    original_name = os.path.basename(filepath)
    encrypted_name = fernet.encrypt(original_name.encode()).decode()
    dest_path = os.path.join(AUDIO_DIR, encrypted_name)
    with open(dest_path, "wb") as f:
        f.write(encrypted_data)
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

# Initialize pygame mixer
pygame.mixer.init()

# Global playback state variables
current_file = None       # currently selected (encrypted) filename
current_tempfile = None   # temporary decrypted file path
total_length = 0          # in seconds
playing = False
paused = False
start_time = 0            # playback start (or resume) time
pause_time = 0            # when paused

progress_lock = threading.Lock()

def main(page: Page):
    global current_file, current_tempfile, total_length, playing, paused, start_time, pause_time

    page.title = "Encrypted Music Player (python-flet)"
    page.window_width = 900
    page.window_height = 600
    page.theme_mode = "dark"  # start dark

    # --- Define UI controls ---
    file_list = ListView(expand=True, spacing=10)

    progress_bar = ProgressBar(width=600, value=0)
    progress_container = Container(content=progress_bar, width=600, on_click=lambda e: seek(e))

    visual_container = Container(
        width=50, height=50, border_radius=25, bgcolor="blue"
    )

    pause_resume_btn = ElevatedButton(text="Pause", icon=icons.PAUSE, on_click=lambda e: toggle_pause_resume())
    play_btn = ElevatedButton(text="Play", icon=icons.PLAY_ARROW, on_click=lambda e: play_file())
    stop_btn = ElevatedButton(text="Stop", icon=icons.STOP, on_click=lambda e: stop_playback())
    theme_toggle = ElevatedButton(text="Toggle Light/Dark", on_click=lambda e: toggle_theme())

    file_picker = FilePicker(on_result=lambda e: file_picker_result(e))
    page.overlay.append(file_picker)
    add_file_btn = ElevatedButton(text="Add File", on_click=lambda e: file_picker.pick_files(allow_multiple=False))

    # --- Helper: update file list from db ---
    def update_file_list():
        file_list.controls.clear()
        for enc, orig in db.items():
            file_list.controls.append(
                ElevatedButton(text=orig, on_click=lambda e, enc=enc: select_file(enc))
            )
        page.update()

    update_file_list()

    # --- Handlers ---
    def select_file(enc):
        global current_file
        current_file = enc
        stop_playback()
        play_file()

    def play_file():
        global current_tempfile, total_length, playing, paused, start_time
        if current_file is None:
            return
        temp_path = decrypt_to_temp(current_file)
        if temp_path is None:
            print("Error decrypting file")
            return
        current_tempfile = temp_path
        try:
            pygame.mixer.music.load(temp_path)
        except Exception as ex:
            print("Error loading file:", ex)
            return
        try:
            audio = MP3(temp_path)
            total_length = audio.info.length
        except Exception as ex:
            print("Error reading audio length:", ex)
            total_length = 0
        pygame.mixer.music.play(loops=0)
        start_time = time.time()
        playing = True
        paused = False
        pause_resume_btn.text = "Pause"
        pause_resume_btn.icon = icons.PAUSE
        page.update()

    def stop_playback():
        global playing, paused, current_tempfile
        if playing:
            pygame.mixer.music.stop()
            playing = False
            paused = False
            progress_bar.value = 0
            if current_tempfile and os.path.exists(current_tempfile):
                os.remove(current_tempfile)
            current_tempfile = None
            page.update()

    def toggle_pause_resume():
        global paused, start_time, pause_time
        if playing:
            if not paused:
                pygame.mixer.music.pause()
                pause_time = time.time()
                paused = True
                pause_resume_btn.text = "Resume"
                pause_resume_btn.icon = icons.PLAY_ARROW
            else:
                pygame.mixer.music.unpause()
                start_time += time.time() - pause_time
                paused = False
                pause_resume_btn.text = "Pause"
                pause_resume_btn.icon = icons.PAUSE
            page.update()

    def toggle_theme():
        if page.theme_mode == "dark":
            page.theme_mode = "light"
        else:
            page.theme_mode = "dark"
        page.update()

    def seek(e):
        global start_time
        width = progress_container.width or 600
        click_x = e.offset.x
        ratio = click_x / width
        new_time = ratio * total_length
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.play(loops=0, start=new_time)
            start_time = time.time() - new_time
        except Exception as ex:
            print("Seeking error:", ex)

    def file_picker_result(e: FilePickerResultEvent):
        if e.files:
            for file in e.files:
                if file.path:
                    encrypt_and_store(file.path)
            update_file_list()

    # --- Layout ---
    main_layout = Column(
        controls=[
            Row(controls=[theme_toggle, add_file_btn], alignment="spaceBetween"),
            Row(controls=[file_list], expand=True),
            Row(controls=[play_btn, pause_resume_btn, stop_btn], alignment="center"),
            Row(controls=[progress_container], alignment="center"),
            Row(controls=[visual_container], alignment="center"),
        ],
        expand=True,
    )
    page.add(main_layout)

    def progress_updater():
        while True:
            if playing and not paused and total_length > 0:
                elapsed = time.time() - start_time
                val = min(elapsed / total_length, 1.0)
                with progress_lock:
                    progress_bar.value = val
                visual_container.bgcolor = "green" if int(elapsed * 2) % 2 == 0 else "blue"
                page.update()
                if val >= 1.0:
                    stop_playback()
            time.sleep(0.5)

    threading.Thread(target=progress_updater, daemon=True).start()

    page.update()

    def on_close(e):
        stop_playback()
        page.window_destroy()

    page.on_close = on_close

flet.app(target=main)
