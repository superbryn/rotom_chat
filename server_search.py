from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Input, Header, Footer, Log, Button
from textual.containers import Vertical
import socket
import threading
import sys

class ServerSearch(App):
    def compose(self) -> ComposeResult:
        yield Static("Choose A Server")
        #with Vertical():
