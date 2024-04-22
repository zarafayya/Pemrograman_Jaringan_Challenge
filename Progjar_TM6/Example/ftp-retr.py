from ftplib import FTP
f = FTP('localhost')

f.login('zara')
fd = open('halo.txt', 'wb')
f.retrbinary('RETR '+'halo.txt', fd.write, 1024)
fd.close()
f.quit()