import os
import customtkinter as ctk
from tkinter import messagebox
from CTkListbox import *

# Function to create subject and subfolder structure
def create_subject_folders(subjects, subfolders):
    for subject in subjects:
        subject_path = os.path.join(".", subject)
        if not os.path.exists(subject_path):
            os.makedirs(subject_path)
        
        for subfolder in subfolders:
            subfolder_path = os.path.join(subject_path, subfolder)
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)

# GUI Class
def gui_app():
    # Initialize CustomTkinter theme
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("dark-blue")

    # Initialize main application window
    app = ctk.CTk()
    app.title("Folder Organizer")
    app.geometry("600x400")

    # Subject and Subfolder lists
    subjects = []
    subfolders = []

    def add_subject():
        subject = subject_entry.get()
        if subject and subject not in subjects:
            subjects.append(subject)
            subject_listbox.insert(ctk.END, subject)
            subject_entry.delete(0, ctk.END)
        else:
            messagebox.showerror("Error", "Subject is empty or already exists!")

    def delete_subject():
        selected = subject_listbox.curselection()
        if selected:
            subjects.remove(subject_listbox.get(selected))
            subject_listbox.delete(selected)
        else:
            messagebox.showerror("Error", "No subject selected!")

    def add_subfolder():
        subfolder = subfolder_entry.get()
        if subfolder and subfolder not in subfolders:
            subfolders.append(subfolder)
            subfolder_listbox.insert(ctk.END, subfolder)
            subfolder_entry.delete(0, ctk.END)
        else:
            messagebox.showerror("Error", "Subfolder is empty or already exists!")

    def delete_subfolder():
        selected = subfolder_listbox.curselection()
        if selected:
            subfolders.remove(subfolder_listbox.get(selected))
            subfolder_listbox.delete(selected)
        else:
            messagebox.showerror("Error", "No subfolder selected!")

    def create_folders():
        if subjects and subfolders:
            create_subject_folders(subjects, subfolders)
            messagebox.showinfo("Success", "Folders created successfully!")
        else:
            messagebox.showerror("Error", "Subjects or Subfolders list is empty!")

    def toggle_theme():
        theme = theme_switch_var.get()
        ctk.set_appearance_mode("dark" if theme else "light")

    # Subject Frame
    subject_frame = ctk.CTkFrame(app)
    subject_frame.pack(pady=10, padx=10, fill="both", expand=True, side="left")

    ctk.CTkLabel(subject_frame, text="Subjects", font=("Arial", 16)).pack(pady=5)

    subject_entry = ctk.CTkEntry(subject_frame, placeholder_text="Enter subject")
    subject_entry.pack(pady=5)

    ctk.CTkButton(subject_frame, text="Add Subject", command=add_subject).pack(pady=5)
    ctk.CTkButton(subject_frame, text="Delete Subject", command=delete_subject).pack(pady=5)

    subject_listbox = CTkListbox(subject_frame)
    subject_listbox.pack(pady=5)

    # Subfolder Frame
    subfolder_frame = ctk.CTkFrame(app)
    subfolder_frame.pack(pady=10, padx=10, fill="both", expand=True, side="left")

    ctk.CTkLabel(subfolder_frame, text="Subfolders", font=("Arial", 16)).pack(pady=5)

    subfolder_entry = ctk.CTkEntry(subfolder_frame, placeholder_text="Enter subfolder")
    subfolder_entry.pack(pady=5)

    ctk.CTkButton(subfolder_frame, text="Add Subfolder", command=add_subfolder).pack(pady=5)
    ctk.CTkButton(subfolder_frame, text="Delete Subfolder", command=delete_subfolder).pack(pady=5)

    subfolder_listbox = CTkListbox(subfolder_frame)
    subfolder_listbox.pack(pady=5)

    # Footer Frame
    footer_frame = ctk.CTkFrame(app)
    footer_frame.pack(fill="x", pady=10)

    theme_switch_var = ctk.BooleanVar()
    theme_switch = ctk.CTkSwitch(footer_frame, text="Dark Mode", variable=theme_switch_var, command=toggle_theme)
    theme_switch.pack(side="left", padx=10)

    ctk.CTkButton(footer_frame, text="Create Folders", command=create_folders).pack(side="right", padx=10)

    # Run the app
    app.mainloop()

# Run GUI
if __name__ == "__main__":
    gui_app()
