#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys, subprocess, shutil, datetime, smtplib, socket
from email.message import EmailMessage

bkdir = "/var/local/shuttlebackup"
mfile = "/root/.shuttle.mails"

if not os.path.exists(bkdir):
        os.makedirs(bkdir)

try:
    os.stat(mfile)
except:
    file = open(mfile, "w")
    file.close()

send_to_mails = []

with open(cfile) as m:
	allmails = m.readlines()

for single_mail in lines:
	if single_mail == "\n":
		break
	else:
		send_to_mails.append(single_mail.replace('\n',''))

process = subprocess.Popen(['snap', 'run', 'rocketchat-server.backupdb'], stdout=subprocess.PIPE)

out, err = process.communicate()

now = datetime.datetime.now()

if err == None:
        out = out.decode().split('\n')
        out = out[-2].replace('A backup of your data can be found at ', '')
        shutil.copy2(out,
                "/var/local/shuttlebackup/bk-" + 
                str(now.year) + 
                "-" + 
                str(now.month) + 
                "-" + 
                str(now.day) + 
                "-" + 
                str(now.hour) + 
                ":" + 
                str(now.minute) + 
                ".tgz")
else:
	with open("/var/log/shuttlebackup.log", "a") as logfile:
            logfile.write(str(now.year) + 
            "-" + str(now.month) + 
            "-" + str(now.day) + 
            "-" + str(now.hour) + 
            ":" + str(now.minute) + 
            ":" + str(now.second) + 
            '\n' + 
            str(err) + 
            '\n')
    try:
		for send_to_mail in send_to_mails:
		    msg = EmailMessage()
		    msg.set_content('Error: ' + str(err))
		    msg['Subject'] = 'Shuttle Backup error!'
		    msg['From'] = "Shuttle" + "@" + socket.gethostname()
		    msg['To'] = send_to_mail
		    s = smtplib.SMTP('localhost')
		    s.send_message(msg)
		    s.quit()
    except:
    	pass
