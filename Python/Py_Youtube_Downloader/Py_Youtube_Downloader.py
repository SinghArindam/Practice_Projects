import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from pytube import YouTube
import os

def download_video():
    url = entry_url.get()
    resolution = resolution_var.get()
    print(url,": ",resolution)
    progress_label.pack(pady=(1, 5))
    progress_bar.pack(pady=(1, 5))
    status_label.pack(pady=(1, 5))
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(res=resolution).first()
        title = str(yt.title())
        status_label.configure(text=f"{title}", text_color="white", fg_color="red")
        
        #stream.download()
    except Exception as e:
        status_label.configure(text=f"Error : {str(e)}", text_color="white", fg_color="red")
        print("Please enter Valid Public Video URL!")

# create a  root window
root = ctk.CTk()
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Title of the window
root.title("Youtube Video Downloader - Arie")

# set min and max width and height
root.geometry("720x480")
root.minsize(720, 480)
root.maxsize(1080, 720)

# create a frame to hold the content
content_frame = ctk.CTkFrame(root)
content_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

# create a label and entry widget for video URL
url_label = ctk.CTkLabel(content_frame, text="Enter Youtube URL : ")
entry_url = ctk.CTkEntry(content_frame, width=400, height=40)
url_label.pack(pady=(1, 5))
entry_url.pack(pady=(1, 5))

# create a download button
download_button = ctk.CTkButton(content_frame, text="Download", command=download_video)
download_button.pack(pady=(1, 5))

# create the resolutions combo box
resolutions = ["Highest","4K - 2160p","2K - 1440p","Full HD - 1080p","HD - 720p", "SD - 480p", "Medium Quslity - 360p",
               "Low Quslity - 240p","Very Low Quslity - 140p", "Lowest", "MP3"]
resolution_var = ctk.StringVar()
resolution_combobox = ttk.Combobox(content_frame, values=resolutions, textvariable=resolution_var)
resolution_combobox.pack(pady=(1, 5))
resolution_combobox.set("Full HD - 1080p")

# create a label and progress bar to display the download progress
progress_label = ctk.CTkLabel(content_frame, text="0%")


progress_bar = ctk.CTkProgressBar(content_frame, width=400)
progress_bar.set(0.6)
progress_bar.pack(pady=(1, 5))

# create a status label
status_label = ctk.CTkLabel(content_frame, text="Downloaded")
status_label.pack(pady=(1, 5))

# to start the application
root.mainloop()