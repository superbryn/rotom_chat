import socket   

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("",6767))
sock.settimeout(2)

while True:
    try:
        data,addr = sock.recvfrom(1024)
        print(data.decode())
    except socket.timeout:
        pass
