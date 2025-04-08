import reflex as rx

# The application state (we'll add more later)
class State(rx.State):
    """The app state."""
    pass # No state variables needed yet

# The main page UI
@rx.page(route="/") # Decorator to define a page at the root URL
def index() -> rx.Component:
    """The main page of the app."""
    return rx.vstack( # Vertical stack layout
        rx.heading("My Reflex Reader", size="2em"), # Large heading
        rx.text("Welcome! Upload a PDF or EPub to start reading."), # Simple text
        spacing="5", # Add some space between elements
        justify="center", # Center content vertically
        align="center", # Center content horizontally
        height="100vh" # Make the layout take full viewport height
    )

# Create the app instance
app = rx.App()
# Add the page to the app
# The route is already defined in the @rx.page decorator
# app.add_page(index) # Not needed if using @rx.page