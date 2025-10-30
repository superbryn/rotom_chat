import socket
import threading
from IpAddrs import local_ip

SERVER_NAME = input("Enter The Name For Your Server: ")
HOST = local_ip()
PORT = 5000 

clients = {}  # Store {socket: username}

def broadcast(sender_socket, message):
    # Send message to all clients except the sender.
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                del clients[client]

def handle_client(client_socket, addr):
    print(f"[+] Connection from {addr}")
    username = client_socket.recv(1024).decode()
    clients[client_socket] = username

    # Joining Broadcast
    broadcast(client_socket, f"[SERVER]: {username} has joined the chat.")
    print(f"[+] {username} connected")

    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break
            broadcast(client_socket, msg)
            print(msg)
        except:
            break

    # Leaving Broadcast
    print(f"[-] {username} disconnected")
    broadcast(client_socket, f"[SERVER]: {username} has left the chat.")
    del clients[client_socket]
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER] Listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()