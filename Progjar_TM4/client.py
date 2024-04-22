import socket
import sys
from threading import Thread

server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)


filename = ""
reply = ""
YES = 0

def thread_input():
    global filename 
    filename = input(">> ")

def thread_recv():
    global reply 
    reply = client_socket.recv(1024).decode()


if __name__ == "__main__":
    thread1 = Thread(target = thread_input)
    thread2 = Thread(target = thread_recv)

    thread1.start()
    thread2.start()

    while True:
        if filename:
            # Input sudah masuk
            # baca file
            f = open(filename, "r")
            msg = f.read()
            f.close()

            # kirim data ke server
            client_socket.send(filename.encode())
            
            # filename dikembalikan menjadi false
            filename = ""
            thread1.join()
            YES = 1

        if reply:
            reply = reply.replace("b", "")
            reply = reply.replace("'", "")
            if YES:
                sys.stdout.write("File terkirim ke client 2 dan client 3")
            else:
                print("Menerima file dari client 1. Nama file: " + str(reply))
            client_socket.send(reply.encode())
            thread1.join()
            thread2.join()
            break

    client_socket.close()
    sys.exit(0)