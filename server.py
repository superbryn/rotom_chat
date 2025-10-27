import socket
import threading

HOST = "192.168.1.2"
PORT = 5000
clients = []

def broadcast(sender, message):
    for client in clients:
            if client != sender:
                try:
                     client.send(message)
                except:
                     clients.remove(client)

def handle_client(client_socket, addr):
    print(f"[+] {addr} connected")
    while True:
        try:
            msg = client_socket.recv(1024)
            if not msg:
                 break
            broadcast(msg, client_socket)
        except:
             break
    print(f"[-] {addr} disconnected")
    clients.remove(client_socket)
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST,PORT))
    server.listen()
    print(f"Listning on {HOST}:{PORT}")
    while True:
        client_socket , addr = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket,addr))
        thread.start()

if __name__ == "__main__":
     start_server()