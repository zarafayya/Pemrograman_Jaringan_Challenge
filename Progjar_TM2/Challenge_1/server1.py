import socket

server_address = ('localhost', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(server_address)
server_socket.listen(1)

client_socket, client_address = server_socket.accept()
data = client_socket.recv(1024).decode()
print(str(data))

client_socket.close()
server_socket.close()