import customtkinter as ctk
import csv
from datetime import datetime
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

class Encryptor:
    def __init__(self):
        # Generate a random AES-256 key for the instance
        pass
    
    def encrypt_mid(self, password):
        """Hashes, encodes, and encrypts the password."""
        hashed_password = self._hash_string(password)
        print(f"Hashed Password (Hex): {hashed_password.hex()}")
        
        encoded_hash = self._base64_encode(hashed_password)
        print(f"Encoded Hashed Password: {encoded_hash}")
        
        key = get_random_bytes(32)  # AES-256 requires a 32-byte key
        encoded_key = base64.b64encode(key).decode('utf-8')  # Store this
        print(f"key :\t{key}")
        iv, encrypted_password = self._aes_encrypt(encoded_hash,key)
        print(f"\nEncrypted Password (Base64): {encrypted_password}")
        print(f"IV (Base64): {iv}")
        print(f"Key: {key},{type(key)}\n")
        print(f"EncodedKey: {encoded_key},{type(encoded_key)}\n")
        
        return [iv, encrypted_password, encoded_key]
    
    def decrypt_mid(self, enc_data):
        if enc_data!="Username":
            iv, encrypted_password, encoded_key = enc_data[0], enc_data[1], enc_data[2]
            key = base64.b64decode(encoded_key)  # Decode back to 32 bytes

        """Decrypts and decodes the password."""
        decrypted_password = self._aes_decrypt(encrypted_password, iv, key)
        print(f"Decrypted Password: {decrypted_password}")
        
        decoded_hash = self._base64_decode(decrypted_password.encode('utf-8'))
        print(f"Decoded Hashed Password (Hex): {decoded_hash.hex()}")
        return decoded_hash.hex()

    def _hash_string(self, input_string):
        """Hashes the input string using SHA-256."""
        return hashlib.sha256(input_string.encode('utf-8')).digest()

    def _base64_encode(self, data):
        """Encodes the data in Base64."""
        return base64.b64encode(data).decode('utf-8')

    def _base64_decode(self, data):
        """Decodes Base64 encoded data."""
        return base64.b64decode(data)

    def _aes_encrypt(self, data, key):
        """Encrypts data using AES-256 in CBC mode."""
        cipher = AES.new(key, AES.MODE_CBC)
        encrypted_data = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
        iv = base64.b64encode(cipher.iv).decode('utf-8')
        encrypted_data_base64 = base64.b64encode(encrypted_data).decode('utf-8')
        return iv, encrypted_data_base64

    def _aes_decrypt(self, encrypted_data_base64, iv_base64, key):
        """ Decrypt data using AES-256. """
        iv = base64.b64decode(iv_base64)
        encrypted_data = base64.b64decode(encrypted_data_base64)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        return decrypted_data.decode('utf-8')

class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # App settings
        self.title("Chat App")
        self.geometry("525x600")
        self.dark_mode = True  # Default mode
        self.user_name = "User"  # Placeholder for the logged-in user's name

        # Initialize chat log CSV file
        self.csv_file = "chat_log.csv"
        self.create_csv_file()

        # Setup UI components
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface with a beautiful, modern design."""
        # Header
        self.header_label = ctk.CTkLabel(self, text=f"Chat App", font=("Helvetica", 20, "bold"))
        self.header_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(20, 10))

        # Chat area (Textbox for displaying messages)
        self.chat_area = ctk.CTkTextbox(self, width=480, height=400, corner_radius=15, state="disabled", wrap="word", font=("Helvetica", 14))
        self.chat_area.grid(row=1, column=0, columnspan=2, padx=20, pady=10)  # Span across both columns

        # Message input field with placeholder text
        self.message_input = ctk.CTkEntry(self, width=350, placeholder_text="Enter your message...", corner_radius=10, font=("Helvetica", 14))
        self.message_input.grid(row=2, column=0, padx=20, pady=(10, 20))

        # Send button with modern style
        self.send_button = ctk.CTkButton(self, text="Send", command=self.send_message, corner_radius=15, width=100, height=40, font=("Helvetica", 14))
        self.send_button.grid(row=2, column=1, padx=20, pady=(10, 20))

        # Dark/Light mode switch with custom style
        self.mode_switch = ctk.CTkSwitch(self, text="Dark Mode", command=self.toggle_mode, onvalue=True, offvalue=False, font=("Helvetica", 12))
        self.mode_switch.grid(row=3, column=0, padx=20, pady=10, columnspan=2)  # Center the switch across both columns

        # Bind Enter key to send message
        self.message_input.bind("<Return>", self.send_message_event)

        # Update the initial theme
        self.update_theme()

    def create_csv_file(self):
        """Create the CSV file if it doesn't exist and add headers."""
        try:
            with open(self.csv_file, mode='x', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['[Timestamp]', '[Sender]', '[Message]'])
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
        self.geometry("450")
        self.dark_mode = True  # Default mode
        
        # Initialize cred CSV file
        self.csv_file = "cred.csv"
        self.create_csv_file()
        
        # Setup UI components
        self.setup_ui()

    def setup_ui(self):
        """Setup the login/register screen with a beautiful design."""
        # Header
        self.header_label = ctk.CTkLabel(self, text="Login / Register", font=("Helvetica", 20, "bold"))
        self.header_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))

        # Username field
        self.username_label = ctk.CTkLabel(self, text="Username:", font=("Helvetica", 14))
        self.username_label.grid(row=1, column=0, padx=20, pady=10)

        self.username_entry = ctk.CTkEntry(self, font=("Helvetica", 14), corner_radius=10)
        self.username_entry.grid(row=1, column=1, padx=20, pady=10)

        # Password field
        self.password_label = ctk.CTkLabel(self, text="Password:", font=("Helvetica", 14))
        self.password_label.grid(row=2, column=0, padx=20, pady=10)

        self.password_entry = ctk.CTkEntry(self, font=("Helvetica", 14), show="*", corner_radius=10)
        self.password_entry.grid(row=2, column=1, padx=20, pady=10)

        # Login button
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login, corner_radius=15, width=100, height=40, font=("Helvetica", 14))
        self.login_button.grid(row=3, column=0, padx=20, pady=20)

        # Register button
        self.register_button = ctk.CTkButton(self, text="Register", command=self.register, corner_radius=15, width=100, height=40, font=("Helvetica", 14))
        self.register_button.grid(row=3, column=1, padx=20, pady=20)

        # Error message label
        self.error_label = ctk.CTkLabel(self, text="", text_color="red", font=("Helvetica", 12))
        self.error_label.grid(row=4, column=0, columnspan=2, padx=20, pady=10)
        
        # Dark/Light mode switch with custom style
        self.mode_switch = ctk.CTkSwitch(self, text="Dark Mode", command=self.toggle_mode, onvalue=True, offvalue=False, font=("Helvetica", 12))
        self.mode_switch.grid(row=5, column=0, padx=20, pady=10, columnspan=2)  # Center the switch across both columns

        # Update the initial theme
        self.update_theme()
            
    def create_csv_file(self):
        """Create the CSV file if it doesn't exist and add headers."""
        try:
            with open(self.csv_file, mode='x', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['[Timestamp]', '[Username]', '[Password]'])
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

    def login(self):
        """Handle the login process."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        print("\t\t",username,password)

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
        encrypt = Encryptor()
        usr = encrypt._hash_string(username).hex()
        pwd = encrypt._hash_string(password).hex()
        with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            users = []
            pwds = []
            print(reader)
            for row in reader:
                r1 = row[1]
                r1 = r1[1:-1]
                if r1!="Username":
                    r1 = r1.split(",")
                    r2 = row[2]
                    r2 = r2[1:-1]
                    r2 = r2.split(",")
                    print(r1)
                    ur = encrypt.decrypt_mid(r1)
                    pw = encrypt.decrypt_mid(r2)
                    users += [ur,]
                    pwds += [pw,]
                    print(row[2])
        return usr in users and pwd in pwds 
    
    def register_user(self, username, password):
        """Register the user (you can add logic to store usernames and passwords)."""
        encrypt = Encryptor()
        usr = encrypt.encrypt_mid(username)
        pwd = encrypt.encrypt_mid(password)
        print(f"\t\tusr :\n{usr},{type(usr[2])}\n\t\tpwd :{pwd}")
        
        """To check if username already exists"""
        with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            users = []
            pwds = []
            print(reader)
            for row in reader:
                users += [row[1],]
                pwds += [row[2],]
                print(row[0])

        """Store the credentials in the CSV file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if usr not in users:
            with open(self.csv_file, mode='a+', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, usr, pwd])
        return usr not in users

    def show_error(self, message):
        """Display an error message."""
        self.error_label.configure(text=message)
        
if __name__ == "__main__":
    login_screen = LoginRegisterScreen()  # Start with login/register screen
    login_screen.mainloop()
