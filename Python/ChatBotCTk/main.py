import customtkinter as ctk
import ollama
import csv
from datetime import datetime

# Function to get the AI response from Ollama
def get_ai_response(user_input):
    try:
        response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": user_input}])
        return response['text']
    except Exception as e:
        return f"Error: {e}"

# Function to handle sending the user's message
def send_message():
    user_message = entry.get()
    if user_message:
        # Add the user's message to the chat history (bubble style)
        chat_history.insert(ctk.END, f"{generate_user_bubble(user_message)}\n")
        chat_history.yview(ctk.END)  # Scroll to the latest message
        
        # Get AI response
        ai_response = get_ai_response(user_message)
        
        # Add the AI's response to the chat history (bubble style)
        chat_history.insert(ctk.END, f"{generate_ai_bubble(ai_response)}\n")
        chat_history.yview(ctk.END)  # Scroll to the latest message

        # Store chat messages in the CSV file
        store_chat("User", user_message)
        store_chat("AI", ai_response)

        # Clear the entry field
        entry.delete(0, ctk.END)

# Function to generate user message bubble
def generate_user_bubble(message):
    return f"{create_bubble(message, 'blue', 'white')}"

# Function to generate AI response bubble
def generate_ai_bubble(message):
    return f"{create_bubble(message, 'green', 'white')}"

# Function to create a message bubble with customizable colors
def create_bubble(message, bg_color, fg_color):
    return f"[{bg_color} bubble] {message}"

# Function to store chat messages in a CSV file
def store_chat(sender, message):
    # Get the current time for timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Append the message to the CSV file
    with open("chat_history.csv", mode="a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, sender, message])

# Create the main window
root = ctk.CTk()
root.title("ChatGPT-like Chatbot")
root.geometry("500x700")

# Set the appearance mode (Dark/Light) and color theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Create the chat history box (scrollable)
chat_history_frame = ctk.CTkScrollableFrame(root, height=500, width=460, corner_radius=10)
chat_history_frame.grid(row=0, column=0, padx=20, pady=20)

# Create the entry widget for user input
entry = ctk.CTkEntry(root, width=400, placeholder_text="Type your message...", corner_radius=10, height=40)
entry.grid(row=1, column=0, padx=20, pady=10)

# Create the send button
send_button = ctk.CTkButton(root, text="Send", width=100, height=40, corner_radius=10, command=send_message)
send_button.grid(row=2, column=0, pady=10)

# Initialize the CSV file with a header (if it doesn't already exist)
try:
    with open("chat_history.csv", mode="r", newline='', encoding="utf-8") as file:
        pass  # File exists, no need to write headers
except FileNotFoundError:
    with open("chat_history.csv", mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Sender", "Message"])

# Start the main loop
root.mainloop()
