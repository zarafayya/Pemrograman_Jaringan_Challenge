import socket
import sys
from datetime import datetime

server_address = ('localhost', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(server_address)
server_socket.listen(1)

try:
    while True:
        client_socket, client_address = server_socket.accept()

        filename = client_socket.recv(1024).decode()
        print(filename)

        f = open(filename, "r")
        msg = f.read()
        f.close()

        client_socket.send("yes".encode())

        file_isi = client_socket.recv(1024).decode()
        print(file_isi)

        f = open(filename, "w")
        f.write(file_isi)
        f.close()

        
        
except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)