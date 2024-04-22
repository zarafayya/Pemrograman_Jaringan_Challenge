import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back

class Group:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.member = []

# init colors
init()

# set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

# choose a random color for the client
client_color = random.choice(colors)

# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

# prompt the client for a name
name = input("Enter your name: ")
    
def input_name():
    to_send = f"/name {name}"
    s.send(to_send.encode())

def welcome():  
    global name
    print("\n-- Welcome to the program, "+name+"! --")
    print("Please enter commands below to start:")
    print("/list - show all online users with their IP and port")
    print("/group create <group name> - create a new group chat")
    print("/group list - show all available group")
    print("/group join <group ID> - join group based on ID")
    print("/private <receiver ID> <message> - to send a private message")
    print("\n")

    cmd = input()
    if cmd == "/chat": 
        chat()
    elif cmd.startswith("/list"):
        s.send(cmd.encode())
        message = s.recv(1024).decode()
        print(message)
        welcome()
    elif cmd.startswith("/private"):
        s.send(cmd.encode())
        message = s.recv(1024).decode()
        print("\n" + message)
        welcome()
    elif cmd.startswith("/group join"):
        s.send(cmd.encode())
        message = s.recv(1024).decode()
        tok = message.split('~')
        print("\n" + tok[0])
        print("Group ID: "+str(tok[1]))
        chat(int(tok[1]))
    elif cmd.startswith("/group"):
        s.send(cmd.encode())
        message = s.recv(1024).decode()
        print("\n" + message)
        welcome()

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)

def chat(group_id):
    t = Thread(target=listen_for_messages)
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()
    print("\n-- Welcome to the chatroom! --")
    print("Enter q to quit")
    while True:
        # input message we want to send to the server
        to_send =  input()
        # a way to exit the program
        if to_send.lower() == 'q':
            t.stop()
            welcome()
        # add the datetime, name & the color of the sender
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        to_send = f"{group_id}~{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
        # finally, send the message
        s.send(to_send.encode())

    # close the socket
    s.close()

# make a thread that listens for messages to this client & print them

input_name()
welcome()

