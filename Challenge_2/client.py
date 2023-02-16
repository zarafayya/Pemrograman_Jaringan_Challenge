import socket

server_ip = input("Enter Server IP: ")
server_port = input("Enter Server Port: ")
strsend = input("Enter Message: ")
server_port = int(server_port)
server_address = (server_ip, server_port)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

client_socket.send(strsend.encode())

ack = client_socket.recv(1024)
print(ack)

client_socket.close()