from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFillRoundFlatButton  # Another alternative button


# Set the window size for desktop applications (if desired)
Window.size = (360, 640)

KV = '''
BoxLayout:
    orientation: "vertical"
    spacing: dp(5)

    MDToolbar:
        title: "Chat App"
        md_bg_color: app.theme_cls.primary_color
        elevation: 10

    ChatBox:
        id: chat_box

    MDBoxLayout:
        padding: dp(10)
        spacing: dp(5)
        size_hint_y: None
        height: dp(50)

        MDTextField:
            id: message_input
            hint_text: "Type your message"
            multiline: False
            on_text_validate: app.send_message()

        MDRaisedButton:
            text: "Send"
            on_release: app.send_message()
'''

class ChatMessage(MDCard):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = dp(10)
        self.md_bg_color = (0.2, 0.6, 0.8, 1)

        self.add_widget(MDLabel(text=text, theme_text_color="Primary"))

class ChatBox(MDScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', padding=10, spacing=5, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_widget(self.layout)

    def add_message(self, message_text):
        if message_text:
            message = ChatMessage(text=message_text)
            self.layout.add_widget(message)
            self.scroll_to(message)

class ChatApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)

    def send_message(self):
        message_input = self.root.ids.message_input
        chat_box = self.root.ids.chat_box
        message_text = message_input.text.strip()

        if message_text:
            chat_box.add_message(message_text)
            message_input.text = ""

ChatApp().run()
