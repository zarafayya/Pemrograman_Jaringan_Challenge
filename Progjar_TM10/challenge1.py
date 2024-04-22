import smtplib
import time
import imaplib
import email
import sys
import os
import shutil

ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "zahra.fayyadiyati" + ORG_EMAIL
FROM_PWD = "UwU sensor hehe"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993

directory = "mails"
parent_dir = "D:/Kuliah/Semester 6/Pemrograman Jaringan/Progjar_TM10"
path = os.path.join(parent_dir, directory)


if os.path.exists(path):
   print("folder exist") 
else: 
    os.mkdir(path)

cmd = input()



try:
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL, FROM_PWD)
    mail.select('inbox')

    if (cmd.startswith("downmail")):
        arg = int(cmd.partition(' ')[2])
        type, data = mail.search(None, 'ALL')
    elif (cmd.startswith("findmail")):
        split = str(cmd.partition(' ')[2]).partition(' ')
        arg = int(split[2])
        keyword = split[0]
        type, data = mail.search(None, 'SUBJECT', keyword)

    mail_ids = data[0]
    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    i = 0

    for num in reversed(data[0].split()):
        print(num)
        if (i == arg): break
        i += 1 
        typ, data = mail.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])


        for part in msg.walk():
            if part.get_content_maintype() == "multipart":
                continue
            if part.get("Content-Disposition") is None:
                continue

            # Extract the attachment filename
            filename = part.get_filename()

            directory = str(i)
            parent_dir = "D:/Kuliah/Semester 6/Pemrograman Jaringan/Progjar_TM10/mails"
            path = os.path.join(parent_dir, directory)

            os.mkdir(path)

            file_path = parent_dir + '/' + directory + '/' + filename

            # Download the attachment
            if filename:
                with open(file_path, "wb") as f:
                    f.write(part.get_payload(decode=True))

        email_from = msg['from']
        email_subject = msg['subject']

        filename = 'mails/' + str(i) + '.txt'
        original_stdout = sys.stdout 

        with open(filename, 'w') as f:
            sys.stdout = f 
            print('From: ' + email_from + '\n')
            print('Subject: ' + email_subject + '\n')
            sys.stdout = original_stdout
except Exception as e:
    print(str(e))

archived = shutil.make_archive("D:\\Kuliah\\Semester 6\\Pemrograman Jaringan\\Progjar_TM10\\mails", 'zip', "D:\\Kuliah\\Semester 6\\Pemrograman Jaringan\\Progjar_TM10\\mails")



