import socket
import select
import sys
import os

server_address = ('127.0.0.1', 80)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

def list_dir(list, dir_path):
    response_data = ''
    for x in list:
        response_data += '<a href='+dir_path+x+'> '+x+'</a><br>'
    return response_data

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])

        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
            else:
                data = sock.recv(4096).decode()

                request_header = data.split('\r\n')
                parse = request_header[0].split()

                if (len(parse) != 0 ):
                    request_file = parse[1]
                else: continue

                if request_file == 'index.html' or request_file == '/' or request_file == '' or request_file == 'index.php':
                    if (os.path.isfile('htdocs/index.html')):
                        f = open('htdocs/index.html', 'r')
                        response_data = f.read()
                        f.close()
                    elif (os.path.isfile('htdocs/index.php')):
                        f = open('htdocs/index.php', 'r')
                        response_data = f.read()
                        f.close()
                    else:
                        listdir = os.listdir('htdocs')
                        response_data = list_dir(listdir, '')
                elif request_file == 'favicon.ico': continue
                else:
                    path = 'htdocs/'+request_file

                    if(os.path.isfile(path)):
                        f = open('htdocs/'+request_file, 'r')
                        response_data = f.read()
                        f.close()
                    else:
                        request_file += '/'
                        listdir = os.listdir(path)
                        listed_link = list_dir(listdir, request_file)

                        back_path_split = path.split('/')
                        back_path = ''

                        for x in back_path_split[:-1]:
                            if x == 'htdocs': continue
                            back_path += x + '/'
                        
                        response_data = '<a href='+back_path+'>..</a><br>' + listed_link

                content_length = len(response_data)
                response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: ' + str(content_length) + '\r\n\r\n'
                
                msg = response_header + response_data
                sock.send(msg.encode())

except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)