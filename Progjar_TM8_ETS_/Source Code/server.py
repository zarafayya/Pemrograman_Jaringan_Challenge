import select
import socket
import sys
import threading
from datetime import datetime

client_sockets = set()
id = 1

def private_msg(cs, args):
    receiver = cs
    for client_socket in client_sockets:
        if str(client_socket.id) == args[0]:
            receiver = client_socket
            break

    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 

    to_send = f"<Private> [{date_now}] {cs.name}: {args[1]}"
    cs.client.send(to_send.encode())
    receiver.client.send(to_send.encode())


def ask_list(cs):
    to_send = '/'
    for client_socket in client_sockets:
        str = f"[+] Online user: {client_socket.id} {client_socket.name}\n"
        to_send += str

    cs.client.send(to_send.encode())

def listen_for_client(cs):
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    separator_token = "<SEP>"
    while True:
        try:
            # keep listening for a message from `cs` socket
            msg = cs.client.recv(1024).decode()
        except Exception as e:
            print(f"[!] Error: {e}")
        else:
                # if we received a message, replace the <SEP> 
                # token with ": " for nice printing
                msg = msg.replace(separator_token, ": ")
                # iterate over all connected sockets
                for client_socket in client_sockets:
                    # and send the message
                    client_socket.client.send(msg.encode())

class Server:
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 5002
        self.backlog = 5
        self.size = 1024
        self.server = None

    def open_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host,self.port))
        self.server.listen(5)

    def run(self):
        global client_sockets
        self.open_socket()
        input = [self.server]
        running = 1
        while running:
            inputready,outputready,exceptready = select.select(input,[],[])

            for s in inputready:
                if s == self.server:
                    # handle the server socket
                    c = Client(self.server.accept())
                    c.start()
                    print(f"[+] {c.address} connected.")
                    client_sockets.add(c)
                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0

	 # close all threads
        self.server.close()
        for c in self.threads:
            c.join()

class Client(threading.Thread):
    def __init__(self, args):
        threading.Thread.__init__(self)
        self.client = args[0]
        self.address = args[1]
        self.name = ''
        self.id = ''
        self.size = 1024

    def run(self):
        global id
        self.id = id
        id += 1

        print(f"[+] {self.address} connected.")
        while True:
            # we keep listening for new connections all the time
            listen_for_client(self)

            


if __name__ == "__main__":
    s = Server()
    print(f"[*] Listening as {s.host}:{s.port}")
    s.run()
