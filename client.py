import socket
import threading

SERVER = input("Enter Host Addrs: ")
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER,PORT))

def receive_message():
    while True:
        try:
            msg = client.recv(1024).decode()
            print(msg)
        except:
            print("Disconnected From Server")
            break

def send_message():
    while True:
        msg = input(":")
        if msg.lower() == "/exit":
            client.close()
            break
        client.send(msg.encode())
recv_thread = threading.Thread(target=receive_message)
recv_thread.start()

send_message()