#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""ShuttleBackup"""

import os
import sys
import time
import subprocess
import shutil
import datetime
import smtplib
import socket
from email.message import EmailMessage

class ShuttleBackup:
    """ShuttleBackup Main Body"""
    def __init__(self):
        try:
            self.argument = sys.argv[1]
        except:
            self.argument = "no-arg"
        self.max_backup_days = 20
        self.backups_folder = "/var/local/shuttlebackup"
        self.emails_file = "/root/.shuttle.mails"
        self.log_file = "/var/log/shuttlebackup.log"
        self.all_mails = ''
        self.send_to_mails = []
        self.requirements_check()

        if self.argument == "--add-mails":
            email = ''
            while True:
                email = email + input("Email: ") + '\n'
                yes_no = input("Do you want to add another email? (y/n): ")
                if yes_no == "n" or yes_no == "N" or yes_no == "no" or yes_no == "No":
                    with open(self.emails_file, "a") as emails:
                        emails.write(email)
                    print("Emails added.")
                    break
                else:
                    continue
        elif self.argument == "--clear-mails":
            file = open(self.emails_file, "w")
            file.close()
        elif self.argument == "no-arg":
            self.load_emails()
            self.command_output, self.command_error, self.command_status = self.create_backup()
            self.clean_backups()
            try:
                self.command_output = self.command_output.split('\n')
                self.dump_location = self.command_output[-2].replace('A backup of your data can be found at ', '')
                backup_time = datetime.datetime.now()
                shutil.copy2(self.dump_location,
                             self.backups_folder +
                             "/bk-" +
                             str(backup_time.year) +
                             "-" +
                             str("%02d" % (backup_time.month, )) +
                             "-" +
                             str("%02d" % (backup_time.day, )) +
                             "-" +
                             str("%02d" % (backup_time.hour, )) +
                             ":" +
                             str("%02d" % (backup_time.minute, )) +
                             ".tgz")
            except:
                self.error_log_and_mail()
        else:
            print("Unknown argument")

    def requirements_check(self):
        """Checks if the required files and folders exist"""
        if not os.path.exists(self.backups_folder):
            os.makedirs(self.backups_folder)
        try:
            os.stat(self.emails_file)
        except:
            file = open(self.emails_file, "w")
            file.close()
        try:
            os.stat(self.log_file)
        except:
            file = open(self.log_file, "w")
            file.close()

    def load_emails(self):
        """Load all email form file"""
        with open(self.emails_file) as mail:
            mails = mail.readlines()
            for single_mail in mails:
                if single_mail == "\n":
                    break
                else:
                    self.send_to_mails.append(single_mail.replace('\n', ''))

    def error_log_and_mail(self):
        """Write the error to the log file and send email notification"""
        backup_time = datetime.datetime.now()
        with open(self.log_file, "a") as log:
            log.write(str(backup_time.year) +
                      "-" + str(backup_time.month) +
                      "-" + str(backup_time.day) +
                      "-" + str(backup_time.hour) +
                      ":" + str(backup_time.minute) +
                      ":" + str(backup_time.second) +
                      '\n' +
                      str("Status: " +
                          str(self.command_status) +
                          '\n' +
                          str(self.command_error) +
                          '\n' +
                          str(self.command_output)) +
                      '\n')
        try:
            for send_to_mail in self.send_to_mails:
                msg = EmailMessage()
                msg.set_content(str("Status: " +
                                    str(self.command_status) +
                                    '\n' +
                                    str(self.command_error) +
                                    '\n' +
                                    str(self.command_output)))
                msg['Subject'] = 'Shuttle Backup error!'
                msg['From'] = "Shuttle" + "@" + socket.gethostname()
                msg['To'] = send_to_mail
                to_send = smtplib.SMTP('localhost')
                to_send.send_message(msg)
                to_send.quit()
        except:
            with open(self.log_file, "a") as log:
                log.write("Error! Could not send email!\n")

    def create_backup(self):
        """Generate the backup tgz dump"""
        self.process = subprocess.Popen(['snap',
                                         'run',
                                         'rocketchat-server.backupdb'],
                                        stdout=subprocess.PIPE)
        self.output = self.process.communicate()
        self.status = self.process.wait()
        if self.output[1] is None:
            return self.output[0].decode(), "Error but no error output...", self.status
        elif self.output[0] is None:
            return "No command output...", self.output[1].decode(), self.status
        elif self.output[0] is None and self.output[1] is None:
            return "No command output...", "Error but no error output...", self.status
        else:
            return self.output[0].decode(), self.output[1].decode(), self.status

    def clean_backups(self):
        now = time.time()
        cutoff = now - (self.max_backup_days * 86400)
        files = os.listdir(self.backups_folder)
        for xfile in files:
            if os.path.isfile( self.backups_folder + "/" + xfile ):
                t = os.stat( self.backups_folder + "/" + xfile )
                c = t.st_ctime
                if c < cutoff:
                    os.remove( self.backups_folder + "/" + xfile )

def main():
    """Load the main class"""
    ShuttleBackup()

if __name__ == "__main__":
    main()
