import socket

server_ip = input("Enter Server IP: ")
server_port = input("Enter Server Port: ")
filename = input("Enter File Name: ")
server_port = int(server_port)
server_address = (server_ip, server_port)

f = open(filename, "r")
msg = f.read()
f.close()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

client_socket.send(filename.encode())

ack = client_socket.recv(1024)
print(ack)

client_socket.send(msg.encode())

client_socket.close()