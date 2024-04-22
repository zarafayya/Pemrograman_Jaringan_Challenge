from ftplib import FTP
f = FTP('localhost')

print('Welcome: ' + f.getwelcome())

f.login('zara')
print('Current working directory' + f.pwd())
names = f.nlst()
print('List of directory: ' + str(names))
f.quit