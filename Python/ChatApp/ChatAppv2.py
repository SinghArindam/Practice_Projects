import customtkinter as ctk
import csv
from datetime import datetime

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # App settings
        self.title("Chat App")
        self.geometry("500x600")
        self.dark_mode = True  # Default mode

        # Initialize chat log CSV file
        self.csv_file = "chat_log.csv"
        self.create_csv_file()

        # Setup UI components
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface."""
        # Chat area (Textbox for displaying messages), spans across two columns (0 and 1)
        self.chat_area = ctk.CTkTextbox(self, width=480, height=400, corner_radius=10)
        self.chat_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)  # Span across both columns
        self.chat_area.configure(state="disabled")  # Make it non-editable

        # Message input field
        self.message_input = ctk.CTkEntry(self, width=350, placeholder_text="Enter your message...")
        self.message_input.grid(row=1, column=0, padx=5, pady=5)

        # Send button
        self.send_button = ctk.CTkButton(self, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=2)

        # Dark/Light mode switch
        self.mode_switch = ctk.CTkSwitch(self, text="Dark Mode", command=self.toggle_mode)
        self.mode_switch.grid(row=2, column=0, padx=20, pady=10, columnspan=2)  # Center the switch across both columns

        # Bind Enter key to send message
        self.message_input.bind("<Return>", self.send_message_event)

        # Update the initial theme
        self.update_theme()

    def create_csv_file(self):
        """Create the CSV file if it doesn't exist and add headers."""
        try:
            with open(self.csv_file, mode='x', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Sender', 'Message'])
        except FileExistsError:
            pass  # If the file exists, no need to create it again

    def toggle_mode(self):
        """Toggle between Dark and Light modes."""
        self.dark_mode = not self.dark_mode
        self.update_theme()

    def update_theme(self):
        """Update the theme of the app based on dark_mode status."""
        if self.dark_mode:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def send_message(self):
        """Send the message and store it in CSV."""
        message = self.message_input.get()
        if message.strip():
            sender_name = "You"  # The user is the sender
            self.display_message(sender_name, message)
            self.store_message(sender_name, message)
            self.message_input.delete(0, 'end')  # Clear the input field

            # Simulating a reply from the bot
            self.after(500, self.simulate_reply)

    def send_message_event(self, event):
        """Send the message when Enter is pressed."""
        self.send_message()

    def display_message(self, sender, message):
        """Display message in the chat area."""
        self.chat_area.configure(state="normal")
        self.chat_area.insert("end", f"{sender}: {message}\n")
        self.chat_area.configure(state="disabled")
        self.chat_area.yview("end")  # Scroll to the bottom

    def store_message(self, sender, message):
        """Store the chat message in the CSV file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, sender, message])

    def simulate_reply(self):
        """Simulate a bot reply."""
        bot_reply = "Hello, how can I assist you?"
        self.display_message("Bot", bot_reply)
        self.store_message("Bot", bot_reply)

if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
