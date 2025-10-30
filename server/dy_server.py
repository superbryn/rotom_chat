import socket
import time
import json

def local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try: s.connect(("8.8.8.8", 80)); return s.getsockname()[0]
        except: return "127.0.0.1"


name = "Neeraj's Rotom Server"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)

msg = json.dumps(
                {
                    "name": name,
                    "ipaddr": local_ip(), 
                    "port": 5000
                }
                )

while True:
    sock.sendto(msg.encode(), ('<broadcast>', 6767))
    time.sleep(2)