import select
import socket
import sys
import threading
from datetime import datetime

class Group:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.member = []

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

client_sockets = set()
groups = set()

id = 1
group_id = 1

def create_group(cs, name):
    global group_id
    g = Group() # kurang args
    g.name = name
    g.id = group_id
    groups.add(g)
    group_id += 1

    str = f"[+] Group ID: {g.id} Group Name: {g.name}"
    print(str)

    to_send = f"A new group named {name} is successfully created."
    cs.client.send(to_send.encode())

def show_group(cs):
    to_send = ''
    for group in groups:
        str = f"[+] Group ID: {group.id} Group Name: {group.name}\n"
        to_send += str
    
    cs.client.send(to_send.encode())

def join_group(cs, id):
    for group in groups:
        if group.id == int(id):
            group.member.append(cs)
            str = f"You have joined group {group.name}.~{group.id}"
            cs.client.send(str.encode())
            break

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
    to_send = ''
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
            if msg.startswith("/name"):
                name = msg.replace('/name ', '')
                cs.name = name
                print("[+] "+str(cs.address)+" has username "+str(cs.name))
            elif msg == "/list":
                ask_list(cs)
            elif msg.startswith("/private"):
                raw = msg.replace('/private ', '')
                args = raw.split()
                private_msg(cs, args)
            elif msg.startswith("/group create"):
                name = msg.replace('/group create ', '')
                create_group(cs, name)
            elif msg.startswith("/group list"):
                show_group(cs)
            elif msg.startswith("/group join"):
                group_id = msg.replace('/group join ', '')
                join_group(cs, group_id)
            else:
                msg = msg.replace(separator_token, ": ")
                # iterate over all connected sockets
                identifier = msg.split('~')
                for group in groups:
                    if group.id == int(identifier[0]):
                        for client_socket in group.member:
                            # and send the message
                            client_socket.client.send(identifier[1].encode())


if __name__ == "__main__":
    s = Server()
    print(f"[*] Listening as {s.host}:{s.port}")
    s.run()
