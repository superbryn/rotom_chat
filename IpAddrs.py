import socket

def local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try: s.connect(("8.8.8.8", 80)); return s.getsockname()[0]
        except: return "127.0.0.1"