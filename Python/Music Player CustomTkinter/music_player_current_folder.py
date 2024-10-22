import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar

import customtkinter as ctk

from mutagen.mp3 import MP3

import threading
import pygame, time, os

# Pygame mixer
# Initialise
pygame.mixer.init()

# current position
current_position = 0
paused = False
selected_folder_path = ""

# Update Progress Bar
def update_progress_bar():
    global current_position
    while True:
        if pygame.mixer.music.get_busy() and not paused:
            current_position = pygame.mixer.music.get_pos()/1000
            progress_bar["value"] = current_position
            
            if current_position >= progress_bar["maximum"]:
                stop_song()
                progress_bar["value"] = 0
            win.update()
        time.sleep(0.1)

# functions
def select_music_folder():
    global selected_folder_path
    selected_folder_path = ""#filedialog.askdirectory()
    if selected_folder_path:
        lbox.delete(0,tk.END)
        for filename in os.listdir(selected_folder_path):
            if filename.endswith(".mp3"):
                lbox.insert(tk.END, filename)

def previous_song():
    if len(lbox.curselection())>0:
        current_index = lbox.curselection()[0]
        if current_index>0:
            lbox.selection_clear(0,tk.END)
            lbox.selection_set(current_index-1)
            play_selected_song()

def play_song():
    global paused
    if paused:
        pygame.mixer.unpause()
        paused = False
    else:
        play_selected_song()
    
def play_selected_song():
    global current_position, paused
    if len(lbox.curselection())>0:
        current_index = lbox.curselection()[0]
        selected_song = lbox.get(current_index)
        full_path = os.path.join(selected_folder_path, selected_song)
        pygame.mixer.music.load(full_path)
        pygame.mixer.play(start=current_position)
        paused = False
        audio = MP3(full_path)
        song_duration = audio.info.length
        progress_bar["maximum"] = song_duration  

def pause_song():
    global paused
    pygame.mixer.music.pause()
    paused = True

def next_song():
    if len(lbox.curselection())>0:
        current_index = lbox.curselection()[0]
        if current_index < lbox.size()-1:
            lbox.selection_clear(0,tk.END)
            lbox.selection_set(current_index+1)
            play_selected_song()
            
def stop_song():
    global paused
    
    pygame.mixer.music.stop()
    paused = False

# Thread to update progressbar
pt = threading.Thread(target=update_progress_bar)
pt.daemon = True
pt.start()

# Main Window
win = tk.Tk()
win.title("Music Player")
win.geometry("600x500")
win.configure(bg='#333333')

# Music Player Label
l_music_player = tk.Label(win, text="Music Player", bg="#333333", fg="#d9d9d9",font=("Helvetica",30,"bold"))
l_music_player.pack(pady=10)

# Select music folder button
btn_select_folder = ctk.CTkButton(win, text="Select Current Folder",
                                command=select_music_folder,
                                font=("Helvetica",18))
btn_select_folder.pack(pady=20)

# listbox for files
lbox = tk.Listbox(win, width=50, bg="#333333", fg="#d9d9d9", font=("Helvetica",16))
lbox.pack(pady=10)

# Frame for buttons
btn_frame = tk.Frame(win)
btn_frame.pack(pady=20)
btn_frame.configure(bg="#333333")

# Buttons
# Previous Song
btn_previous_song = ctk.CTkButton(btn_frame, text= "<",command=previous_song,
                                  width=50, font=("Helvetica",20))
btn_previous_song.pack(side=tk.LEFT, padx=5)

# Play Song
btn_play_song = ctk.CTkButton(btn_frame, text= "PLAY",command=play_song,
                                  width=50, font=("Helvetica",18))
btn_play_song.pack(side=tk.LEFT, padx=5)

# pause Song
btn_pause_song = ctk.CTkButton(btn_frame, text= "PAUSE",command=pause_song,
                                  width=50, font=("Helvetica",18))
btn_pause_song.pack(side=tk.LEFT, padx=5)

# Next Song
btn_next_song = ctk.CTkButton(btn_frame, text= ">",command=next_song,
                                  width=50, font=("Helvetica",20))
btn_next_song.pack(side=tk.LEFT, padx=5)

# Progress Bar
progress_bar = Progressbar(win, length=300, mode="determinate")
progress_bar.pack(pady=10)

# Mainloop
win.mainloop()