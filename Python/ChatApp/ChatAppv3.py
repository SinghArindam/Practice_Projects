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
        self.user_name = "User"  # Placeholder for the logged-in user's name

        # Initialize chat log CSV file
        self.csv_file = "chat_log.csv"
        self.create_csv_file()

        # Setup UI components
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface."""
        # Chat area (Textbox for displaying messages), spans across two columns (0 and 1)
        self.chat_area = ctk.CTkTextbox(self, width=480, height=400, corner_radius=10, state="disabled", wrap="word")
        self.chat_area.grid(row=0, column=0, columnspan=2, padx=20, pady=20)  # Span across both columns

        # Message input field with placeholder text
        self.message_input = ctk.CTkEntry(self, width=350, placeholder_text="Enter your message...", corner_radius=10)
        self.message_input.grid(row=1, column=0, padx=10, pady=10)

        # Send button with modern style
        self.send_button = ctk.CTkButton(self, text="Send", command=self.send_message, corner_radius=10)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        # Dark/Light mode switch with custom style
        self.mode_switch = ctk.CTkSwitch(self, text="Dark Mode", command=self.toggle_mode, onvalue=True, offvalue=False)
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
            sender_name = self.user_name  # Placeholder for the user's name
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


class LoginRegisterScreen(ctk.CTk):
    def __init__(self):
        super().__init__()

        # App settings
        self.title("Login/Register")
        self.geometry("400x300")
        self.dark_mode = True  # Default mode
        
        # Setup UI components
        self.setup_ui()

    def setup_ui(self):
        """Setup the login/register screen."""
        # Username field
        self.username_label = ctk.CTkLabel(self, text="Username:", font=("Helvetica", 14))
        self.username_label.grid(row=0, column=0, padx=20, pady=15)

        self.username_entry = ctk.CTkEntry(self, font=("Helvetica", 14), corner_radius=10)
        self.username_entry.grid(row=0, column=1, padx=20, pady=15)

        # Password field
        self.password_label = ctk.CTkLabel(self, text="Password:", font=("Helvetica", 14))
        self.password_label.grid(row=1, column=0, padx=20, pady=15)

        self.password_entry = ctk.CTkEntry(self, font=("Helvetica", 14), show="*", corner_radius=10)
        self.password_entry.grid(row=1, column=1, padx=20, pady=15)

        # Login button
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login, corner_radius=10, font=("Helvetica", 14))
        self.login_button.grid(row=2, column=0, padx=20, pady=20)

        # Register button
        self.register_button = ctk.CTkButton(self, text="Register", command=self.register, corner_radius=10, font=("Helvetica", 14))
        self.register_button.grid(row=2, column=1, padx=20, pady=20)

        # Error message label
        self.error_label = ctk.CTkLabel(self, text="", text_color="red", font=("Helvetica", 12))
        self.error_label.grid(row=3, column=0, columnspan=2, padx=20, pady=10)
        
        # Dark/Light mode switch with custom style
        self.mode_switch = ctk.CTkSwitch(self, text="Dark Mode", command=self.toggle_mode, onvalue=True, offvalue=False)
        self.mode_switch.grid(row=4, column=0, padx=20, pady=10, columnspan=2)  # Center the switch across both columns

        # Update the initial theme
        self.update_theme()
        
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

    def login(self):
        """Handle the login process."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.authenticate_user(username, password):
            self.destroy()  # Close the login/register window
            app = ChatApp()  # Open the chat app window
            app.user_name = username  # Set the username in the chat app
            app.mainloop()
        else:
            self.show_error("Invalid username or password.")

    def register(self):
        """Handle the registration process."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.register_user(username, password):
            self.show_error("Registration successful! You can now login.")
        else:
            self.show_error("Username already exists.")

    def authenticate_user(self, username, password):
        """Authenticate the user (here you can add real authentication logic)."""
        # For now, this is just a placeholder
        return username == "user" and password == "password"  # Replace with your authentication logic

    def register_user(self, username, password):
        """Register the user (you can add logic to store usernames and passwords)."""
        # For simplicity, this is just a placeholder
        return username != "user"  # Ensure "user" is not already taken

    def show_error(self, message):
        """Display an error message."""
        self.error_label.configure(text=message)


if __name__ == "__main__":
    login_screen = LoginRegisterScreen()  # Start with login/register screen
    login_screen.mainloop()
