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

        timestamp = str(datetime.now())
        data = client_socket.recv(1024).decode()

        if data == "asklog":
            f = open("log.txt", "r")
            msg = f.read()
            client_socket.send(msg.encode())
        else:
            log = "Timestamp: " + timestamp + "\nIP Client: " + client_address[0] + "\nIP Port: " + str(client_address[1]) + "\nPesan: " + data + "\n"

            f = open("log.txt", "a")
            f.write(log)
            f.close()

            client_socket.send(log.encode())

        print(client_address)
except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)