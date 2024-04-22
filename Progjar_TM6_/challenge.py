import os.path, os
from ftplib import FTP
from zipfile import ZipFile

def cmd_pwd():
    print('Current working directory: ' + f.pwd())
    names = f.nlst()
    print('List of directory: ' + str(names) + '\n')

def cmd_download():
    print('Insert filename that you wish to download: ')
    filename = input('>> ')
    fd = open(filename, 'wb')
    f.retrbinary('RETR '+ filename, fd.write, 1024)
    fd.close()
    print('Download successful.\n')

def cmd_ls():
    print('Directory list: ')
    ftpResponse = f.dir()
    print(ftpResponse)
    print('\n')

def cmd_mkdir():
    print('Insert new directory name: ')
    dirname = input('>> ')
    f.mkd(dirname)
    print('\n')

def cmd_upload():
    print('Insert filename that you wish to upload: ')
    up_filename = input('>> ')
    up_file = open(up_filename,'rb')                  
    f.storbinary('STOR ' + up_filename, up_file)    
    up_file.close()  

def cmd_uptract():
    print('Insert zip you wish to upload and extract: ')
    uptract_name = input('>> ')

    new_name = uptract_name.replace('.zip', '')

    with ZipFile("D:\\Kuliah\\Semester 6\\Pemrograman Jaringan\\Progjar_TM6\\"+uptract_name, 'r') as zObject:
        zObject.extractall(
            path="D:\\Kuliah\\Semester 6\\Pemrograman Jaringan\\Progjar_TM6\\"+ new_name)

    f.mkd(new_name)
    entries = []
    for path in os.listdir(new_name + '/' + new_name + '/'):
        if os.path.isfile(os.path.join(new_name + '/' + new_name + '/', path)):
            entries.append(path)

    for entry in entries:
        up_file = open(new_name + '/'+ new_name + '/' + entry,'rb')                  
        f.storbinary('STOR ' + new_name + '/' + entry, up_file)    
        up_file.close()  



print('Insert IP FTP server:')
ftp_ip = input('>> ')
print('Insert username:')
username = input('>> ')
print('Insert password:')
password = input('>> ')

f = FTP(ftp_ip)
print('Welcome: ' + f.getwelcome() + '\n')
f.login(username, password)


while True:
    print('Insert command: ')
    cmd = input('>> ')

    if cmd == "PWD": cmd_pwd()
    elif cmd == "LS": cmd_ls()
    elif cmd == "MKDIR": cmd_mkdir()
    elif cmd == "DOWNLOAD": cmd_download()
    elif cmd == "UPLOAD": cmd_upload()
    elif cmd == "UPTRACT": cmd_uptract()

f.quit











