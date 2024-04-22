import socket
import sys

server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

filename = input("Enter File Name: ")

f = open(filename, "r")
msg = f.read()
f.close()

client_socket.send(msg.encode())
sys.stdout.write(client_socket.recv(1024).decode())

client_socket.close()
sys.exit(0)