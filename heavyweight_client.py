from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Input, Header, Footer, Log, Button
from textual.containers import Vertical
import socket
import threading
import sys


class RotomClient:
    def __init__(self, SERVER: str, PORT: int, username: str, on_msg):
        self.server = SERVER
        self.port = PORT
        self.username = username
        self.on_msg = on_msg  # callback for messages
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True

    def connect(self):
        self.client.connect((self.server, self.port))
        self.client.send(self.username.encode())
        threading.Thread(target=self.receive, daemon=True).start()

    def receive(self):
        while self.running:
            try:
                msg = self.client.recv(1024).decode()
                if msg:
                    self.on_msg(msg)
            except:
                break

    def send(self, msg):
        try:
            self.client.send(f"[{self.username}]: {msg}".encode())
        except:
            pass

    def disconnect(self):
        self.running = False
        try:
            self.client.close()
        except:
            pass


class Login(Screen):
    def compose(self) -> ComposeResult:
        yield Static("Enter Your Username", id="label")
        yield Input(placeholder="Your Username", id="username")
        yield Button("Enter Chat", id="join_button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        username = self.query_one("#username", Input).value.strip()
        if username:
            self.app.username = username
            self.app.push_screen("chat")
    

class Chat(Screen):
    BINDINGS = [
        ("ctrl+o", "quit" , "Quit")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            self.chat_log = Log(id="chatlog")
            yield self.chat_log
            self.msg_input = Input(placeholder="Type your message...", id="msg_input")
            yield self.msg_input
        yield Footer(show_command_palette=False)

    def on_mount(self):
        self.client = RotomClient("192.168.8.133", 5000, self.app.username, self.add_message)
        self.client.connect()
        self.chat_log.write(f"[SYSTEM]: Connected to server as {self.app.username}.\n")

    def add_message(self, msg: str):
        self.chat_log.write(f"{msg}\n")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        msg = event.value.strip()
        if msg:
            self.client.send(msg)
            self.chat_log.write(f"[{self.app.username}]: {msg}\n")
            self.msg_input.value = ""
    
    def action_quit(self):
        return sys.exit()

class RotomChat(App):
    CSS = """
    Log {
        height: 1fr;
        border: solid blue;
    }
    Input {
        border: solid grey;
    }
    """
    def on_mount(self):
        self.username = None
        self.install_screen(Login(), name="login")
        self.install_screen(Chat(), name="chat")
        self.push_screen("login")  # start at login screen

if __name__ == "__main__":
    RotomChat().run()
