from textual import on
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Input, Header, Footer, Log, Button
from textual.containers import Vertical, ScrollableContainer, Center
import socket, threading, asyncio, json


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
            self.disconnect()

    def disconnect(self):
        self.running = False
        try:
            self.client.close()
        except:
            pass


class Login(Screen):
    ASCII_ART = r"""

/^^^^^^^        /^^^^     /^^^ /^^^^^^    /^^^^     /^^       /^^
/^^    /^^    /^^    /^^       /^^      /^^    /^^  /^ /^^   /^^^
/^^    /^^  /^^        /^^     /^^    /^^        /^^/^^ /^^ / /^^
/^ /^^      /^^        /^^     /^^    /^^        /^^/^^  /^^  /^^
/^^  /^^    /^^        /^^     /^^    /^^        /^^/^^   /^  /^^
/^^    /^^    /^^     /^^      /^^      /^^     /^^ /^^       /^^
/^^      /^^    /^^^^          /^^        /^^^^     /^^       /^^
                                                                   
    """
    CSS = """
    Screen {
        align: center middle;
    }
    #ascii {
        content-align: center middle;
        margin-bottom: 1;
        color: cyan;
    }
    #username{
        border: solid white;
        background: transparent;
        width: 50%
    }
    #next_button{
        background: transparent;
        border: solid white;
        align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, time_format=None)
        yield Static(self.ASCII_ART, markup=False, id="ascii")
        with Center():
            yield Input(placeholder="Enter Your Name", id="username")
        with Center():
            yield Button("Next", id="next_button", flat=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        username = self.query_one("#username", Input).value.strip()
        if username:
            self.app.username = username
            self.app.push_screen("search") # opens server searching screen
    
# UDP Server Finder
class ServerFinder:
    def __init__(self, callback, loop):
        self.callback = callback
        self.loop = loop
        self.running = True

    def start(self, port=6767): # Listen on port 6767
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("",port))
        sock.settimeout(2)

        while self.running:
            try:
                data, addr = sock.recvfrom(1024)
                msg = json.loads(data.decode())
                asyncio.run_coroutine_threadsafe(self.callback(msg), self.loop)
            except socket.timeout:
                continue
            except Exception as e:
                pass

    def stop(self):
        self.running = False

# Server selection window
class SearchScreen(Screen):
    CSS = """
    Screen {
        align: center middle;
    }
    #title{
        content-align: center middle;
    }
    #servers {
        align: center top;
        width: 50%;
    }

    Button {
        align: center top;
        margin: 1;
        width: 100%;
        height: 3;
        text-align: center;
        border: round $accent;
    }
    """
    ASCII_ART = """
┏━┓╻ ╻┏━┓╻╻  ┏━┓┏┓ ╻  ┏━╸   ┏━┓┏━╸┏━┓╻ ╻┏━╸┏━┓┏━┓
┣━┫┃┏┛┣━┫┃┃  ┣━┫┣┻┓┃  ┣╸    ┗━┓┣╸ ┣┳┛┃┏┛┣╸ ┣┳┛┗━┓
╹ ╹┗┛ ╹ ╹╹┗━╸╹ ╹┗━┛┗━╸┗━╸   ┗━┛┗━╸╹┗╸┗┛ ┗━╸╹┗╸┗━┛
"""

    def __init__(self,):
        super().__init__()
        self.servers = {}
        self.listener = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Static(self.ASCII_ART, classes="title", id="title")
        with Center():
            self.container = ScrollableContainer(id="servers")
            yield self.container
        yield Footer(show_command_palette=False)

    async def on_mount(self) -> None:
        loop = asyncio.get_running_loop()
        self.listener = ServerFinder(self.add_server, loop)
        threading.Thread(target=self.listener.start, daemon=True).start()
    
    async def add_server(self, packet: dict):
        ip:str = packet.get("ipaddr")
        port:int = packet.get("port")
        self.server_name:str = packet.get("name", "Unnamed Server")

        if ip not in self.servers:
            self.servers[ip] = (self.server_name, port)
            safe_id = f"btn_{ip.replace(".","_")}_{port}"
            await self.container.mount(Button(f"{self.server_name} ({ip}:{port})", id=safe_id, name=f"{ip}:{port}", flat=True))

    @on(Button.Pressed)
    def on_button_pressed(self, event:Button.Pressed) -> None:
        server = event.button.name
        ip, port = server.split(":")
        self.app.selected_server = (ip, int(port))
        self.notify(f"Joined {self.server_name} :- {ip}")
        self.app.install_screen(Chat(), name="chat")
        self.app.push_screen("chat")
    
    async def on_unmount(self):
        self.listener.stop()

class Chat(Screen):
    CSS = """
    Log {
        height: 1fr;
        border: solid white;
    }
    #msg_input {
        border: solid grey;
        color: white;
    }
    """
    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            self.chat_log = Log(id="chatlog")
            yield self.chat_log
            self.msg_input = Input(placeholder="Type your message...", id="msg_input")
            yield self.msg_input
        yield Footer(show_command_palette=False)

    def on_mount(self):
        ip_addrs, port = self.app.selected_server
        self.client = RotomClient(ip_addrs, port, self.app.username, self.add_message)
        self.client.connect()
        self.chat_log.write(f"[CLIENT]: Connected to server as {self.app.username}.\n")

    def add_message(self, msg: str):
        self.chat_log.write(f"{msg}\n")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        msg = event.value.strip()
        if msg:
            self.client.send(msg)
            self.chat_log.write(f"[{self.app.username}]: {msg}\n")
            self.msg_input.value = ""
    
    def action_quit(self):
        self.client.disconnect()
        self.app.exit()
        

class RotomChat(App):
    BINDINGS = [
        ("ctrl+q", "quit" , "Quit")
    ]

    def on_mount(self):
        self.username = None
        self.selected_server = None
        self.install_screen(Login(), name="login")
        self.install_screen(SearchScreen(), name="search")
        self.push_screen("login")  # start

if __name__ == "__main__":
    try:
        RotomChat().run()
    except LookupError:
        pass