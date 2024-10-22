from customtkinter import CTk
from customtkinter import CTkEntry, CTkButton, CTkSwitch
from pytube import Playlist

# Function to download a single video with numbering
def download_video(url, title, order, output_dir):
  try:
    # Create Youtube object
    yt = YouTube(url)

    # Get best available video and audio streams
    stream = yt.streams.filter(progressive=True).order_by('resolution').desc().first()

    # Create filename with order number
    filename = f"{order}. {title}.{stream.extension}"

    # Download video to specified directory
    stream.download(output_path=output_dir, filename=filename)

    print(f"Downloaded: {filename}")
  except Exception as e:
    print(f"Error downloading {title}: {e}")

# Function to download the entire playlist
def download_playlist():
  # Get playlist URL from entry field
  playlist_url = playlist_entry.get().strip()

  # Get output directory from user selection
  output_dir = filedialog.askdirectory(title="Select Output Directory")

  if playlist_url and output_dir:
    try:
      # Create Playlist object
      playlist = Playlist(playlist_url)

      # Loop through videos with numbering
      for order, video in enumerate(playlist.videos, start=1):
        download_video(video.watch_url, video.title, order, output_dir)

      print("Playlist downloaded successfully!")
    except Exception as e:
      print(f"Error downloading playlist: {e}")

# Function to toggle theme
def toggle_theme():
  global is_dark_mode
  is_dark_mode = not is_dark_mode
  if is_dark_mode:
    customtkinter.set_appearance_mode("dark")
  else:
    customtkinter.set_appearance_mode("light")
  update_color_scheme()  # Call function to update colors based on theme

def update_color_scheme():
  if is_dark_mode:
    app.configure(fg_color="#FFFFFF")  # White text for dark mode
  else:
    app.configure(fg_color="#000000")  # Black text for light mode

# Create main window
app = CTk()
app.geometry("500x150")
app.title("YouTube Playlist Downloader with Numbering")

# Theme variables
is_dark_mode = False  # Initial theme is light
customtkinter.set_appearance_mode("light")

# Label and entry field for playlist URL
playlist_label = CTkLabel(app, text="Playlist URL:")
playlist_label.pack(pady=10)

playlist_entry = CTkEntry(app, width=50)
playlist_entry.pack()

# Button to trigger download
download_button = CTkButton(app, text="Download Playlist", command=download_playlist)
download_button.pack(pady=10)

# Switch for light/dark theme
theme_switch = CTkSwitch(app, text="Light", command=toggle_theme)
theme_switch.pack(pady=10)

# Update color scheme based on initial theme
update_color_scheme()

# Run the main event loop
app.mainloop()
