import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
import os.path, os
from ftplib import FTP
from zipfile import ZipFile


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
f = open("conf", "r")
file_text = f.read()
f.close()

ip_server = ""
username = ""
password = ""

cut_server = file_text.partition('\n')
cut_username = cut_server[2].partition('\n')
cut_password = cut_username[2].partition('\n')

# ip server
cut2 = cut_server[0].partition(" = ")
ip_server = cut2[2]
print(ip_server)

# username
cut2 = cut_username[0].partition(" = ")
username = cut2[2]
print(username)

# password
cut2 = cut_password[0].partition(" = ")
password = cut2[2]
print(password)

SERVER_HOST = ip_server
SERVER_PORT = 5002 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

# # initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

f = FTP(ip_server)
f.login(username, password)

# am i the one that uploads?

i_am_sendall = False

def cmd_ls():
    print('Directory list: ')
    ftpResponse = f.dir()
    print(ftpResponse)
    print('\n')

def cmd_pwd():
    print('Current working directory: ' + f.pwd())
    names = f.nlst()
    print('List of directory: ' + str(names) + '\n')

def cmd_cwd(folder_name):
    f.cwd(folder_name)
    cmd_pwd()

def cmd_mkdir(folder_name):
    f.mkd(folder_name)
    print("A file named "+folder_name+" has been created.")

def cmd_sendall(filename):
    fd = open(filename, 'wb')
    f.retrbinary('RETR '+ filename, fd.write, 1024)
    fd.close()
    print('You has downloaded a file.\n')

    file = open(filename, "r")
    file_text = file.read()
    file.close()

    filename = "SENDALL " + filename

    s.sendto(filename.encode(), (SERVER_HOST, SERVER_PORT))
    s.sendto(str(file_text).encode(), (SERVER_HOST, SERVER_PORT))

def welcome():  
    print("\n-- Welcome to the program, "+username+"! --")
    print("You can enter commands below to interact with FTP:")
    print("LIST - show all files in FTP")
    print("PWD - show present working directory")
    print("CD <folder name> - change to another directory")
    print("MKDIR <folder name> - create a new directory")
    print("SENDALL <file name> - send a file to all clients")
    print("\n")
    chat()

def listen_for_messages():
    global i_am_sendall
    while True:
        message = s.recv(1024).decode()
        if message.startswith("SENDALL"):
            file_text = s.recv(1024).decode()
            arg = message.partition(' ')
            if i_am_sendall == False:
                fd = open(arg[2], 'w')
                fd.write(file_text)
                fd.close()
                print('You have received a file.')
            else:
                i_am_sendall = False

                printed = file_text.partition('SENDALL')

                print("The file contains: "+printed[0])
        else:
            print("\n" + message)

def chat():
    global i_am_sendall
    t = Thread(target=listen_for_messages)
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()
    print("\n-- Welcome to the chatroom! --")
    while True:
        # input message we want to send to the server
        to_send =  input()

        # command checker
        if to_send.startswith("LIST"):
            cmd_ls()
        elif to_send.startswith("PWD"):
            cmd_pwd()
        elif to_send.startswith("CD"):
            arg = to_send.partition(' ')
            cmd_cwd(arg[2])
        elif to_send.startswith("MKDIR"):
            arg = to_send.partition(' ')
            cmd_mkdir(arg[2])
        elif to_send.startswith("SENDALL"):
            arg = to_send.partition(' ')
            cmd_sendall(arg[2])
            s.send(to_send.encode())
            i_am_sendall = True
        else:
            # add the datetime, name & the color of the sender
            date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
            to_send = f"{client_color}[{date_now}] {username}{separator_token}{to_send}{Fore.RESET}"
            # finally, send the message
            s.send(to_send.encode())

    # close the socket
    s.close()

# make a thread that listens for messages to this client & print them
welcome()


