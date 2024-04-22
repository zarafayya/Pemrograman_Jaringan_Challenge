import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
target_name = '127.0.0.1'
server_address = ('127.0.0.1', 80)
client_socket.connect(server_address)

request_header = 'GET / HTTP/1.0\r\nHost: ' + target_name + '\r\n\r\n'
client_socket.send(request_header.encode())

response = client_socket.recv(1024).decode()

print(response)
client_socket.close()