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
        data = client_socket.recv(1024).decode()

        f = open("log.txt", "a")
        f.write("data = " + data + "\n")
        f.write("ip address = " + str(client_address[0]) + "\n")
        f.write("port = " + str(client_address[1]) + "\n")
        f.write("tanggal = " + str(datetime.now()) + "\n")
        f.close()

        print(client_address)
except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)