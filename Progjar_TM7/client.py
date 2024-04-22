import socket
import os

s_addr = input("Enter server address: ")

server_address = (s_addr, 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

filename = input("Enter file name: ")

f = open(filename, "r")
file_text = f.read()
f.close()

cwd = os.getcwd()
file_size = os.path.getsize(cwd + "\\" + filename)

client_socket.sendto(filename.encode(), server_address)
client_socket.sendto(str(file_size).encode(), server_address)

with open(cwd + "\\" + filename, "rb") as fi:
            buf = fi.read(1024)
            while (buf):
               client_socket.sendto(buf, server_address)
               buf = fi.read(1024)

msg, client_address = client_socket.recvfrom(1024)
print(str(msg.decode()))
               


