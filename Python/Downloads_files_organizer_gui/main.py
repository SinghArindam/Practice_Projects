# Downloads Folder Organizer GUI
import os
import shutil
import time
import json
import threading
from pathlib import Path
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

# Default configuration
DEFAULT_CONFIG = {
    "file_types": {
        "Documents": [".pdf", ".docx", ".doc", ".txt", ".rtf", ".odt", ".xlsx", ".xls", ".pptx", ".ppt", ".csv"],
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".tiff", ".webp"],
        "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"],
        "Audio": [".mp3", ".wav", ".ogg", ".m4a", ".flac", ".aac"],
        "Compressed": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
        "Executables": [".exe", ".msi", ".app", ".dmg", ".deb", ".rpm"],
        "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".go", ".php", ".rb", ".sh"]
    },
    "source_directory": str(Path.home() / "Downloads"),
    "destination_directory": str(Path.home() / "Downloads"),
    "handle_duplicates": "rename",  # Options: "rename", "replace", "skip"
    "organize_interval": 0,  # 0 means run once, >0 means watch folder and organize every X seconds
    "move_unknown_types": True,  # Move files with unknown extensions to "Others" folder
    "create_date_subfolders": False,  # Create YYYY-MM subfolders
    "ignore_extensions": [],  # Extensions to ignore
    "ignored_files": [".DS_Store", "desktop.ini"],  # Files to ignore
    "simulate": False  # Simulate organization without moving files
}

class DownloadsOrganizer:
    """Organizes files in a downloads folder based on their extensions."""
    
    def __init__(self, config=None, log_callback=None):
        """Initialize the organizer with configuration."""
        self.config = DEFAULT_CONFIG.copy()
        if config:
            self.config.update(config)
        
        self.source_dir = Path(self.config["source_directory"])
        self.dest_dir = Path(self.config["destination_directory"])
        self.log_callback = log_callback
        self.running = False
        self.watch_thread = None
        
        # Create category folders if not simulating
        if not self.config["simulate"]:
            self._create_category_folders()
        
        self.log(f"Source directory: {self.source_dir}")
        self.log(f"Destination directory: {self.dest_dir}")
        if self.config["simulate"]:
            self.log("SIMULATION MODE: No files will be moved")
    
    def log(self, message):
        """Log a message to the console and through the callback if available."""
        print(message)
        if self.log_callback:
            self.log_callback(message)
    
    def _create_category_folders(self):
        """Create folders for each category and the Others folder."""
        self.dest_dir.mkdir(parents=True, exist_ok=True)
        
        for category in self.config["file_types"]:
            category_path = self.dest_dir / category
            category_path.mkdir(exist_ok=True)
        
        if self.config["move_unknown_types"]:
            others_path = self.dest_dir / "Others"
            others_path.mkdir(exist_ok=True)
    
    def get_category(self, file_path):
        """Determine the category of a file based on its extension."""
        extension = file_path.suffix.lower()
        
        # Check if the extension should be ignored
        if extension in self.config["ignore_extensions"]:
            return None
        
        # Check file against each category
        for category, extensions in self.config["file_types"].items():
            if extension in extensions:
                return category
        
        # If no category matched and move_unknown_types is True
        if self.config["move_unknown_types"]:
            if extension:
                return f"Others/{extension.lstrip('.')}"
            else:
                return "Others/No_Extension"
        
        return None
    
    def handle_duplicate(self, destination):
        """Handle duplicate files according to configuration."""
        if not destination.exists():
            return destination
        
        if self.config["handle_duplicates"] == "replace":
            return destination
        elif self.config["handle_duplicates"] == "skip":
            self.log(f"Skipping duplicate file: {destination}")
            return None
        else:  # "rename" (default)
            counter = 1
            new_destination = destination
            while new_destination.exists():
                stem = destination.stem
                suffix = destination.suffix
                new_destination = destination.with_name(f"{stem}_{counter}{suffix}")
                counter += 1
            return new_destination
    
    def organize_file(self, file_path):
        """Organize a single file."""
        # Skip if this is a directory or an ignored file
        if file_path.is_dir() or file_path.name in self.config["ignored_files"]:
            return False
        
        # Get the category for this file
        category = self.get_category(file_path)
        if not category:
            return False
        
        # Prepare destination path
        if "/" in category:
            main_category, sub_category = category.split("/", 1)
            destination_dir = self.dest_dir / main_category / sub_category
        else:
            destination_dir = self.dest_dir / category
        
        # Add date subfolder if configured
        if self.config["create_date_subfolders"]:
            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            date_folder = mod_time.strftime("%Y-%m")
            destination_dir = destination_dir / date_folder
        
        # Create destination directory if not simulating
        if not self.config["simulate"]:
            destination_dir.mkdir(parents=True, exist_ok=True)
        
        # Full destination path
        destination = destination_dir / file_path.name
        
        # Handle duplicates
        destination = self.handle_duplicate(destination)
        if destination is None:
            return False
        
        # Move the file if not simulating
        if self.config["simulate"]:
            self.log(f"SIMULATION: Would move {file_path} to {destination}")
            return True
        else:
            try:
                shutil.move(str(file_path), str(destination))
                self.log(f"Moved {file_path.name} to {destination}")
                return True
            except Exception as e:
                self.log(f"Error moving file {file_path}: {e}")
                return False
    
    def organize(self):
        """Organize all files in the source directory."""
        stats = {
            "total_files": 0,
            "organized_files": 0,
            "skipped_files": 0,
            "errors": 0
        }
        
        # Process all files in the source directory
        for item in self.source_dir.iterdir():
            if not self.running and self.watch_thread:
                break
                
            if item.is_file() and item.name not in self.config["ignored_files"]:
                stats["total_files"] += 1
                try:
                    if self.organize_file(item):
                        stats["organized_files"] += 1
                    else:
                        stats["skipped_files"] += 1
                except Exception as e:
                    self.log(f"Error organizing {item.name}: {e}")
                    stats["errors"] += 1
        
        mode = "SIMULATION" if self.config["simulate"] else "Organization"
        self.log(f"{mode} complete: {stats['organized_files']} organized, {stats['skipped_files']} skipped, {stats['errors']} errors")
        return stats
    
    def watch_and_organize(self):
        """Watch the source directory and organize periodically."""
        self.log(f"Watching directory: {self.source_dir}")
        self.log(f"Organization interval: {self.config['organize_interval']} seconds")
        
        self.running = True
        try:
            while self.running:
                stats = self.organize()
                self.log(f"Waiting {self.config['organize_interval']} seconds for next organization...")
                for _ in range(self.config['organize_interval']):
                    if not self.running:
                        break
                    time.sleep(1)
        except Exception as e:
            self.log(f"Error in watching thread: {e}")
        finally:
            self.log("Watching stopped")
    
    def start_watching(self):
        """Start watching in a separate thread."""
        if self.watch_thread and self.watch_thread.is_alive():
            self.log("Already watching folder")
            return False
            
        self.running = True
        self.watch_thread = threading.Thread(target=self.watch_and_organize)
        self.watch_thread.daemon = True
        self.watch_thread.start()
        return True
    
    def stop_watching(self):
        """Stop the watching thread."""
        self.running = False
        if self.watch_thread:
            self.log("Stopping folder watching...")
            # Let the thread exit gracefully
            if self.watch_thread.is_alive():
                self.watch_thread.join(timeout=2)
            return True
        return False

class FileTypeFrame(ctk.CTkFrame):
    """Frame for managing file type categories and extensions."""
    
    def __init__(self, master, file_types, on_update_callback):
        super().__init__(master)
        self.file_types = file_types.copy()
        self.on_update_callback = on_update_callback
        
        # Create the UI
        self.create_widgets()
        
    def create_widgets(self):
        # Create a label
        ctk.CTkLabel(self, text="File Types & Extensions", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Create a frame for file types
        self.file_types_frame = ctk.CTkScrollableFrame(self, width=400, height=300)
        self.file_types_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add file type widgets
        self.type_frames = {}
        self.extensions_vars = {}
        
        row = 0
        for category, extensions in self.file_types.items():
            # Create label for category
            category_frame = ctk.CTkFrame(self.file_types_frame)
            category_frame.grid(row=row, column=0, padx=5, pady=5, sticky="ew")
            
            # Store the frame for later updates
            self.type_frames[category] = category_frame
            
            # Add category label
            ctk.CTkLabel(category_frame, text=category, width=100).grid(row=0, column=0, padx=5, pady=5)
            
            # Add extensions entry
            extensions_str = ", ".join(extensions)
            extensions_var = ctk.StringVar(value=extensions_str)
            self.extensions_vars[category] = extensions_var
            
            extensions_entry = ctk.CTkEntry(category_frame, width=200, textvariable=extensions_var)
            extensions_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            
            # Add update button
            update_btn = ctk.CTkButton(category_frame, text="Update", width=70, 
                                     command=lambda cat=category: self.update_extensions(cat))
            update_btn.grid(row=0, column=2, padx=5, pady=5)
            
            # Add delete button
            delete_btn = ctk.CTkButton(category_frame, text="Delete", width=70, fg_color="red", 
                                     command=lambda cat=category: self.delete_category(cat))
            delete_btn.grid(row=0, column=3, padx=5, pady=5)
            
            category_frame.grid_columnconfigure(1, weight=1)
            row += 1
        
        # Add new category section
        add_frame = ctk.CTkFrame(self)
        add_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(add_frame, text="New Category:").grid(row=0, column=0, padx=5, pady=5)
        
        self.new_category_var = ctk.StringVar()
        new_category_entry = ctk.CTkEntry(add_frame, textvariable=self.new_category_var)
        new_category_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(add_frame, text="Extensions:").grid(row=0, column=2, padx=5, pady=5)
        
        self.new_extensions_var = ctk.StringVar()
        new_extensions_entry = ctk.CTkEntry(add_frame, textvariable=self.new_extensions_var)
        new_extensions_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        add_btn = ctk.CTkButton(add_frame, text="Add Category", command=self.add_category)
        add_btn.grid(row=0, column=4, padx=5, pady=5)
        
        add_frame.grid_columnconfigure(1, weight=1)
        add_frame.grid_columnconfigure(3, weight=1)
    
    def update_extensions(self, category):
        """Update extensions for the given category."""
        extensions_str = self.extensions_vars[category].get()
        extensions = [ext.strip() for ext in extensions_str.split(",") if ext.strip()]
        
        # Ensure all extensions start with a dot
        extensions = [ext if ext.startswith(".") else f".{ext}" for ext in extensions]
        
        self.file_types[category] = extensions
        self.on_update_callback(self.file_types)
    
    def delete_category(self, category):
        """Delete a category."""
        del self.file_types[category]
        self.type_frames[category].destroy()
        del self.type_frames[category]
        del self.extensions_vars[category]
        self.on_update_callback(self.file_types)
    
    def add_category(self):
        """Add a new category."""
        category = self.new_category_var.get().strip()
        extensions_str = self.new_extensions_var.get().strip()
        
        if not category:
            messagebox.showerror("Error", "Category name cannot be empty")
            return
        
        if category in self.file_types:
            messagebox.showerror("Error", f"Category '{category}' already exists")
            return
        
        extensions = [ext.strip() for ext in extensions_str.split(",") if ext.strip()]
        
        # Ensure all extensions start with a dot
        extensions = [ext if ext.startswith(".") else f".{ext}" for ext in extensions]
        
        if not extensions:
            messagebox.showerror("Error", "Must provide at least one extension")
            return
        
        # Add the new category
        self.file_types[category] = extensions
        
        # Clear the entry fields
        self.new_category_var.set("")
        self.new_extensions_var.set("")
        
        # Rebuild the UI
        for widget in self.file_types_frame.winfo_children():
            widget.destroy()
        self.create_widgets()
        
        self.on_update_callback(self.file_types)

class OptionsFrame(ctk.CTkFrame):
    """Frame for various organization options."""
    
    def __init__(self, master, config, on_update_callback):
        super().__init__(master)
        self.config = config.copy()
        self.on_update_callback = on_update_callback
        
        # Create the UI
        self.create_widgets()
    
    def create_widgets(self):
        # Heading
        ctk.CTkLabel(self, text="Organization Options", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Create a frame for options
        options_frame = ctk.CTkFrame(self)
        options_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Duplicate handling
        ctk.CTkLabel(options_frame, text="Handle duplicates:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.duplicate_var = ctk.StringVar(value=self.config["handle_duplicates"])
        duplicate_options = ["rename", "replace", "skip"]
        duplicate_dropdown = ctk.CTkOptionMenu(options_frame, variable=self.duplicate_var, values=duplicate_options,
                                            command=self.update_duplicate_handling)
        duplicate_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Unknown file types
        self.unknown_var = ctk.BooleanVar(value=self.config["move_unknown_types"])
        unknown_checkbox = ctk.CTkCheckBox(options_frame, text="Move unknown file types to 'Others' folder",
                                         variable=self.unknown_var, command=self.update_unknown_types)
        unknown_checkbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        
        # Date subfolders
        self.date_var = ctk.BooleanVar(value=self.config["create_date_subfolders"])
        date_checkbox = ctk.CTkCheckBox(options_frame, text="Create date-based subfolders (YYYY-MM)",
                                      variable=self.date_var, command=self.update_date_subfolders)
        date_checkbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        
        # Simulation mode
        self.simulate_var = ctk.BooleanVar(value=self.config["simulate"])
        simulate_checkbox = ctk.CTkCheckBox(options_frame, text="Simulation mode (don't actually move files)",
                                         variable=self.simulate_var, command=self.update_simulate)
        simulate_checkbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        
        # Interval for watching
        ctk.CTkLabel(options_frame, text="Watch interval (seconds):").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        
        self.interval_var = ctk.StringVar(value=str(self.config["organize_interval"]))
        interval_entry = ctk.CTkEntry(options_frame, textvariable=self.interval_var, width=100)
        interval_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        
        update_interval_btn = ctk.CTkButton(options_frame, text="Update Interval", 
                                         command=self.update_interval)
        update_interval_btn.grid(row=4, column=2, padx=10, pady=10)
        
        # Ignored files
        ctk.CTkLabel(options_frame, text="Ignored files:").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        
        self.ignored_files_var = ctk.StringVar(value=", ".join(self.config["ignored_files"]))
        ignored_files_entry = ctk.CTkEntry(options_frame, textvariable=self.ignored_files_var, width=200)
        ignored_files_entry.grid(row=5, column=1, columnspan=2, padx=10, pady=10, sticky="ew")
        
        update_ignored_btn = ctk.CTkButton(options_frame, text="Update Ignored Files", 
                                        command=self.update_ignored_files)
        update_ignored_btn.grid(row=5, column=3, padx=10, pady=10)
        
        # Ignored extensions
        ctk.CTkLabel(options_frame, text="Ignored extensions:").grid(row=6, column=0, padx=10, pady=10, sticky="w")
        
        self.ignored_extensions_var = ctk.StringVar(value=", ".join(self.config["ignore_extensions"]))
        ignored_extensions_entry = ctk.CTkEntry(options_frame, textvariable=self.ignored_extensions_var, width=200)
        ignored_extensions_entry.grid(row=6, column=1, columnspan=2, padx=10, pady=10, sticky="ew")
        
        update_ignored_ext_btn = ctk.CTkButton(options_frame, text="Update Ignored Extensions", 
                                            command=self.update_ignored_extensions)
        update_ignored_ext_btn.grid(row=6, column=3, padx=10, pady=10)
    
    def update_duplicate_handling(self, choice):
        """Update duplicate handling strategy."""
        self.config["handle_duplicates"] = choice
        self.on_update_callback(self.config)
    
    def update_unknown_types(self):
        """Update unknown types handling."""
        self.config["move_unknown_types"] = self.unknown_var.get()
        self.on_update_callback(self.config)
    
    def update_date_subfolders(self):
        """Update date subfolders option."""
        self.config["create_date_subfolders"] = self.date_var.get()
        self.on_update_callback(self.config)
    
    def update_simulate(self):
        """Update simulation mode."""
        self.config["simulate"] = self.simulate_var.get()
        self.on_update_callback(self.config)
    
    def update_interval(self):
        """Update organization interval."""
        try:
            interval = int(self.interval_var.get())
            if interval < 0:
                raise ValueError("Interval must be a positive number")
            self.config["organize_interval"] = interval
            self.on_update_callback(self.config)
        except ValueError:
            messagebox.showerror("Error", "Interval must be a positive number")
    
    def update_ignored_files(self):
        """Update ignored files list."""
        files_str = self.ignored_files_var.get()
        files = [f.strip() for f in files_str.split(",") if f.strip()]
        self.config["ignored_files"] = files
        self.on_update_callback(self.config)
    
    def update_ignored_extensions(self):
        """Update ignored extensions list."""
        extensions_str = self.ignored_extensions_var.get()
        extensions = [ext.strip() for ext in extensions_str.split(",") if ext.strip()]
        
        # Ensure all extensions start with a dot
        extensions = [ext if ext.startswith(".") else f".{ext}" for ext in extensions]
        
        self.config["ignore_extensions"] = extensions
        self.on_update_callback(self.config)

class OrganizerApp(ctk.CTk):
    """Main application window for Downloads Folder Organizer."""
    
    def __init__(self):
        super().__init__()
        
        # Configure the window
        self.title("Downloads Folder Organizer")
        self.geometry("900x700")
        self.minsize(800, 600)
        
        # Load or create configuration
        self.config_path = Path.home() / ".downloads_organizer_config.json"
        self.config = self.load_config()
        
        # Create the organizer
        self.organizer = DownloadsOrganizer(self.config, self.log_message)
        
        # Create the UI
        self.create_widgets()
        
        # Log initial state
        self.log_message("Downloads Folder Organizer started")
        self.log_message("Configure options and click 'Organize Now' to begin")
    
    def load_config(self):
        """Load configuration from file or use default."""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                return config
            except Exception as e:
                print(f"Error loading configuration: {e}")
        
        return DEFAULT_CONFIG.copy()
    
    def save_config(self):
        """Save current configuration to file."""
        try:
            with open(self.config_path, "w") as f:
                json.dump(self.config, f, indent=4)
            self.log_message("Configuration saved")
            return True
        except Exception as e:
            self.log_message(f"Error saving configuration: {e}")
            return False
    
    def create_widgets(self):
        """Create all UI widgets."""
        # Create a main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create the directory selection section
        self.create_directory_section(main_frame)
        
        # Create tabs for options
        self.create_tabs(main_frame)
        
        # Create log section
        self.create_log_section(main_frame)
        
        # Create action buttons
        self.create_action_buttons(main_frame)
    
    def create_directory_section(self, parent):
        """Create the directory selection section."""
        dir_frame = ctk.CTkFrame(parent)
        dir_frame.pack(fill="x", padx=10, pady=5)
        
        # Source directory
        ctk.CTkLabel(dir_frame, text="Source Directory:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.source_var = ctk.StringVar(value=self.config["source_directory"])
        source_entry = ctk.CTkEntry(dir_frame, textvariable=self.source_var, width=300)
        source_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        source_btn = ctk.CTkButton(dir_frame, text="Browse", command=self.browse_source)
        source_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Destination directory
        ctk.CTkLabel(dir_frame, text="Destination Directory:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.dest_var = ctk.StringVar(value=self.config["destination_directory"])
        dest_entry = ctk.CTkEntry(dir_frame, textvariable=self.dest_var, width=300)
        dest_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        dest_btn = ctk.CTkButton(dir_frame, text="Browse", command=self.browse_dest)
        dest_btn.grid(row=1, column=2, padx=10, pady=10)
        
        # Make source and destination entries expandable
        dir_frame.grid_columnconfigure(1, weight=1)
    
    def create_tabs(self, parent):
        """Create tabs for different settings."""
        self.tabview = ctk.CTkTabview(parent)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Add tabs
        self.tabview.add("File Types")
        self.tabview.add("Options")
        
        # File types tab
        self.file_type_frame = FileTypeFrame(self.tabview.tab("File Types"), 
                                            self.config["file_types"], 
                                            self.update_file_types)
        self.file_type_frame.pack(fill="both", expand=True)
        
        # Options tab
        self.options_frame = OptionsFrame(self.tabview.tab("Options"), 
                                         self.config, 
                                         self.update_config)
        self.options_frame.pack(fill="both", expand=True)
    
    def create_log_section(self, parent):
        """Create the log display section."""
        log_frame = ctk.CTkFrame(parent)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(log_frame, text="Activity Log", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
        
        # Create a text widget for logs
        self.log_text = ctk.CTkTextbox(log_frame, height=150, wrap="word")
        self.log_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Make the text read-only
        self.log_text.configure(state="disabled")
    
    def create_action_buttons(self, parent):
        """Create action buttons section."""
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        # Organize now button
        organize_btn = ctk.CTkButton(button_frame, text="Organize Now", 
                                   fg_color="green", text_color="white",
                                   command=self.organize_now)
        organize_btn.pack(side="left", padx=10, pady=10)
        
        # Simulate button
        simulate_btn = ctk.CTkButton(button_frame, text="Simulate", 
                                   command=self.simulate)
        simulate_btn.pack(side="left", padx=10, pady=10)
        
        # Start watching button
        self.watch_btn = ctk.CTkButton(button_frame, text="Start Watching", 
                                     command=self.toggle_watching)
        self.watch_btn.pack(side="left", padx=10, pady=10)
        
        # Save config button
        save_btn = ctk.CTkButton(button_frame, text="Save Configuration", 
                               command=self.save_config)
        save_btn.pack(side="right", padx=10, pady=10)
    
    def browse_source(self):
        """Browse for a source directory."""
        directory = filedialog.askdirectory(initialdir=self.source_var.get())
        if directory:
            self.source_var.set(directory)
            self.config["source_directory"] = directory
            self.organizer.source_dir = Path(directory)
            self.log_message(f"Source directory set to: {directory}")
    
    def browse_dest(self):
        """Browse for a destination directory."""
        directory = filedialog.askdirectory(initialdir=self.dest_var.get())
        if directory:
            self.dest_var.set(directory)
            self.config["destination_directory"] = directory
            self.organizer.dest_dir = Path(directory)
            self.log_message(f"Destination directory set to: {directory}")
    
    def update_file_types(self, file_types):
        """Update file types configuration."""
        self.config["file_types"] = file_types
        self.organizer.config["file_types"] = file_types
        self.log_message("File types updated")
    
    def update_config(self, updated_config):
        """Update configuration with settings from options."""
        for key, value in updated_config.items():
            if key != "file_types":  # We handle file_types separately
                self.config[key] = value
                self.organizer.config[key] = value
        self.log_message("Configuration updated")
    
    def log_message(self, message):
        """Log a message to the log display."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Enable editing, add text, then disable again
        self.log_text.configure(state="normal")
        self.log_text.insert("end", log_entry)
        self.log_text.see("end")  # Scroll to the end
        self.log_text.configure(state="disabled")
    
    def organize_now(self):
        """Organize files immediately."""
        # Update config from UI
        self.config["source_directory"] = self.source_var.get()
        self.config["destination_directory"] = self.dest_var.get()
        
        # Create a new organizer with updated config
        self.organizer = DownloadsOrganizer(self.config, self.log_message)
        
        # Run the organization in a separate thread
        threading.Thread(target=self.organizer.organize, daemon=True).start()
    
    def simulate(self):
        """Run a simulation without moving files."""
        # Create a config with simulation mode enabled
        sim_config = self.config.copy()
        sim_config["simulate"] = True
        
        # Update source and destination from UI
        sim_config["source_directory"] = self.source_var.get()
        sim_config["destination_directory"] = self.dest_var.get()
        
        # Create a temporary organizer with simulation mode
        sim_organizer = DownloadsOrganizer(sim_config, self.log_message)
        
        # Run the simulation in a separate thread
        threading.Thread(target=sim_organizer.organize, daemon=True).start()
    
    def toggle_watching(self):
        """Toggle the folder watching state."""
        if self.organizer.running:
            # Stop watching
            if self.organizer.stop_watching():
                self.watch_btn.configure(text="Start Watching")
        else:
            # Update config from UI
            self.config["source_directory"] = self.source_var.get()
            self.config["destination_directory"] = self.dest_var.get()
            
            # Create a new organizer with updated config
            self.organizer = DownloadsOrganizer(self.config, self.log_message)
            
            # Start watching
            if self.organizer.start_watching():
                self.watch_btn.configure(text="Stop Watching")

def main():
    """Main entry point for the application."""
    app = OrganizerApp()
    app.mainloop()

if __name__ == "__main__":
    main()
