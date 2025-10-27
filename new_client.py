import socket
import threading
import sys

SERVER = input("Enter Host Addr: ")
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

username = input("Enter your username: ")
client.send(username.encode())  # Send username first


def receive_message():
    while True:
        try:
            msg = client.recv(1024).decode()
            sys.stdout.write(f"\r{msg}\n[{username}] : ")
            sys.stdout.flush()
        except:
            print("\nDisconnected from server.")
            break


def send_message():
    while True:
        msg = input(f"[{username}] : ")
        if msg:
            if msg.lower() == "/exit":
                client.close()
                break
            client.send(f"[{username}] : {msg}".encode())


recv_thread = threading.Thread(target=receive_message, daemon=True)
recv_thread.start()
send_message()
