"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config

class State(rx.State):
    """The app state."""

    pass

# Define the main page
def index():
    return rx.vstack(
        # Header
        rx.heading("My Portfolio", size="lg", margin_bottom="20px"),
        
        # About Me Section
        rx.box(
            rx.text("About Me", font_size="1.5em", font_weight="bold"),
            rx.text(
                "Hi, I'm [Your Name], a passionate Python developer with experience in building web applications. "
                "I love creating tools that solve real-world problems."
            ),
            padding="20px",
            border="1px solid #ddd",
            border_radius="8px",
            margin_bottom="20px",
            width="100%",
        ),
        
        # Projects Section
        rx.box(
            rx.text("Projects", font_size="1.5em", font_weight="bold"),
            rx.vstack(
                rx.text("Project 1: Portfolio Website - Built with Reflex in pure Python."),
                rx.text("Project 2: Data Dashboard - A tool for visualizing data trends."),
                rx.text("Project 3: Chat App - A real-time messaging app using WebSockets."),
                spacing="10px",
            ),
            padding="20px",
            border="1px solid #ddd",
            border_radius="8px",
            margin_bottom="20px",
            width="100%",
        ),
        
        # Contact Section
        rx.box(
            rx.text("Contact", font_size="1.5em", font_weight="bold"),
            rx.text("Email: your.email@example.com"),
            rx.text("GitHub: github.com/yourusername"),
            rx.text("LinkedIn: linkedin.com/in/yourusername"),
            padding="20px",
            border="1px solid #ddd",
            border_radius="8px",
            width="100%",
        ),
        
        # Styling
        align_items="center",
        padding="40px",
        max_width="800px",
        margin="0 auto",
    )

# def index() -> rx.Component:
#     # Welcome Page (Index)
#     return rx.container(
#         rx.color_mode.button(position="top-right"),
#         rx.vstack(
#             rx.heading("Welcome to Reflex!", size="9"),
#             rx.text(
#                 "Get started by editing ",
#                 rx.code(f"{config.app_name}/{config.app_name}.py"),
#                 size="5",
#             ),
#             rx.link(
#                 rx.button("Check out our docs!"),
#                 href="https://reflex.dev/docs/getting-started/introduction/",
#                 is_external=True,
#             ),
#             spacing="5",
#             justify="center",
#             min_height="85vh",
#         ),
#         rx.logo(),
#     )


app = rx.App()
app.add_page(index)
