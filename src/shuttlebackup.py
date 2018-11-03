#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""ShuttleBackup"""

import sys

try:
    assert sys.version_info >= (3,0)
except:
    print('This is a python 3 application, but you are running python 2.')
    sys.exit(1)

import os
import time
import subprocess
import shutil
import datetime
import smtplib
import socket
import sqlite3

from email.message import EmailMessage

class ShuttleBackup:
    """ShuttleBackup Main Body"""
    def __init__(self):
        try:
            self.argument = sys.argv[1]
        except:
            self.argument = None

        self.base_folder = "/var/shuttlebackup"
        self.backups_folder = "/var/shuttlebackup/archives"
        self.backups_log_folder = "/var/shuttlebackup/logs"
        self.log_file = "/var/log/shuttlebackup.log"
        self.db_file = self.base_folder + "/shuttle.db"

        self.requirements_check()

        self.shuttledb = self.init_db_connection()

        self.send_to_mails = self.get_emails()

        self.max_backups = self.get_max_backups()

        if self.argument is not None:
            if self.argument == "--backup" or self.argument == "-b":
                print("Archiving database...")
            elif self.argument == "--add-emails" or self.argument == "-e":
                self.add_emails()
                sys.exit(0)

            elif self.argument == "--show-emails" or self.argument == "-se":
                if self.send_to_mails:
                    for email in self.send_to_mails:
                        print(email)
                sys.exit(0)

            elif self.argument == "--remove-email" or self.argument == "-re":
                self.remove_email()
                sys.exit(0)

            elif self.argument == "--clear-emails" or self.argument == "-ce":
                self.shuttledb.cursor().execute("DELETE FROM Emails")
                self.shuttledb.commit()
                print("Emails cleared!")
                sys.exit(0)

            elif self.argument == "--change-count" or self.argument == "-cc":
                ndays = input("Number of backups: ")
                self.shuttledb.cursor().execute("UPDATE Settings SET count=" +
                                                ndays +
                                                " WHERE count=" +
                                                str(self.max_backups))
                self.shuttledb.commit()
                print("Count changed.")
                sys.exit(0)

            elif self.argument == "--show-count" or self.argument == "-sc":
                print("The number of a backups kept is " + str(self.max_backups) + ".")
                sys.exit(0)

            elif self.argument == "--clear-backups" or self.argument == "-cb":
                self.clear_backups()
                sys.exit(0)

            elif self.argument == "--remove-backup" or self.argument == "-rb":
                self.remove_backup()
                sys.exit(0)

            elif self.argument == "--show-backups" or self.argument == "-sb":
                self.show_backups()
                sys.exit(0)

            else:
                if self.argument == "--help" or self.argument == "-h":
                    print("Available options:\n")
                    self.print_help()
                    sys.exit(0)
                else:
                    print('Unknown argument - "' +
                          self.argument +
                          '"\nAvailable options:\n')
                    self.print_help()
                    sys.exit(1)

        try:
            self.command_output, self.command_error, self.command_status = self.create_backup()
            self.command_output = self.command_output.split('\n')
            backup_dump_name = self.command_output[-2].split('A backup of your data can be found at ')[1]
            backup_log_name = backup_dump_name.replace('rocketchat_', '').replace('tar.gz', 'log')
            shutil.move(backup_dump_name, self.backups_folder)
            shutil.move(backup_log_name, self.backups_log_folder)
        except:
            self.notify_failed_backup()
            sys.exit(1)

        self.clean_backups()

    def print_help(self):
        """Show help information"""
        print("  -h,  --help\t\t\t" +
              "Show this help information." +
              "\n  -b,  --backup\t\t\t" +
              "Create a backup of the current Rocket.Chat database." +
              "\n  -e,  --add-emails\t\t" +
              "Add emails to which a notification will be sent in case of error." +
              "\n  -se, --show-emails\t\t" +
              "Show all notifyable emails." +
              "\n  -re, --remove-email\t\t" +
              "Remove email from the 'send to' list." +
              "\n  -ce, --clear-emails\t\t" +
              "Remove all emails from your 'send to' list." +
              "\n  -sb, --show-backups\t\t" +
              "Show all backups." +
              "\n  -rb, --remove-backup\t\t" +
              "Delete select backups." +
              "\n  -cb, --clear-backups\t\t" +
              "Delete all backups." +
              "\n  -cc, --change-count\t\t" +
              "Change the max. number of backup archives." +
              "\n  -sc, --show-count\t\t" +
              "Show the max. number of backup archives.\n")

    def create_db(self):
        """Creates the tables in the sqlite db file if they do not exist"""
        conn = sqlite3.connect(self.db_file)

        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS `Emails` (
	    `id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	    `email`	TEXT
        );''')

        c.execute('''CREATE TABLE `Settings` (
	    `count`	INTEGER
        );''')

        c.execute('''INSERT INTO Settings VALUES (10);''')

        conn.commit()

        conn.close()

    def init_db_connection(self):
        """Initializes the connection to the sqlite db"""
        try:
            conn = sqlite3.connect(self.db_file)
        except:
            time = datetime.datetime.now()

            with open(self.log_file, "a") as log:
                log.write("Date: " +
                          str(time.year) +
                          "-" + str(time.month) +
                          "-" + str(time.day) +
                          "-" + str(time.hour) +
                          ":" + str(time.minute) +
                          " - Could not connect to sqlite!\n")

            sys.exit("Error connecting to sqlite!")

        return conn

    def requirements_check(self):
        """Checks if the required files and folders exist"""
        if not os.path.exists(self.base_folder):
            os.makedirs(self.base_folder)

        if not os.path.exists(self.backups_folder):
            os.makedirs(self.backups_folder)

        if not os.path.exists(self.backups_log_folder):
            os.makedirs(self.backups_log_folder)

        try:
            os.stat(self.log_file)
        except:
            db_file = open(self.log_file, "w")
            db_file.close()

        try:
            os.stat(self.db_file)
        except:
            self.create_db()

    def get_emails(self):
        """Gets all emails"""
        emails = []

        for mail in self.shuttledb.cursor().execute('SELECT email FROM Emails'):
            emails.append(str(mail[0]))

        return emails

    def add_emails(self):
        """Add emails"""
        while True:
            email = input("Email: ")
            self.shuttledb.cursor().execute("INSERT INTO Emails (email) VALUES ('" + email + "')")
            yes_no = input("Do you want to add another email? (y/n): ")
            if yes_no == "n" or yes_no == "N" or yes_no == "no" or yes_no == "No":
                print("Emails added.")
                self.shuttledb.commit()
                break
            else:
                continue

    def remove_email(self):
        """Removes select emails"""
        for email in self.send_to_mails:
            question = input("Remove email - '" + email + "'? (y/n/quit): ")
            if question == 'y' or question == 'Y' or question == 'Yes' or question == 'yes' or question == 'YES':
                self.shuttledb.cursor().execute("DELETE FROM Emails WHERE email='" + email + "'")
            elif question == 'quit' or question == 'QUIT' or question == 'Quit':
                break
        self.shuttledb.commit()

    def get_max_backups(self):
        count = 10

        for c in self.shuttledb.cursor().execute('SELECT count FROM Settings'):
            count = int(c[0])

        return count

    def notify_failed_backup(self):
        """Write the error to the log file and send email notification if possible"""
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
        if self.send_to_mails:
            try:
                msg = EmailMessage()
                msg.set_content(str("Status: " +
                                    str(self.command_status) +
                                    '\n' +
                                    str(self.command_error) +
                                    '\n' +
                                    str(self.command_output)))
                msg['Subject'] = 'Backup error! - ' + str(backup_time.day) + str(backup_time.month) + str(backup_time.year)
                msg['From'] = "Shuttle" + "@" + socket.gethostname()
                msg['To'] = ', '.join(self.send_to_mails)
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
            return self.output[0].decode(), "Error with no message...", self.status

        elif self.output[0] is None:
            return "No command output...", self.output[1].decode(), self.status

        elif self.output[0] is None and self.output[1] is None:
            return "No command output...", "Error with no message...", self.status

        else:
            return self.output[0].decode(), self.output[1].decode(), self.status

    def clear_backups(self):
        """Deletes all archives form the backup folder"""
        os.system("rm -rf " + str(self.backups_folder) + "/*")
        print("Deleted all archives.")

    def clean_backups(self):
        """Deletes old backups"""
        files = os.listdir(self.backups_folder)
        files.sort(reverse=True)

        for n, file in enumerate(files):
            if (n + 1) > self.max_backups:
                os.remove(self.backups_folder + "/" + file)

    def remove_backup(self):
        """Delete select backups"""
        files = os.listdir(self.backups_folder)
        files.sort(reverse=False)

        for file in files:
            question = input("Delete '" + file + "'? (y/n/quit): ")
            if question == 'y' or question == 'Y' or question == 'Yes' or question == 'yes' or question == 'YES':
                os.remove(self.backups_folder + "/" + file)
                print("Deleted.")

    def show_backups(self):
        """Shows all backups"""
        files = os.listdir(self.backups_folder)
        files.sort(reverse=False)

        for file in files:
            print(file)

def main():
    """Check permissions and load the main class"""
    if os.geteuid() != 0:
        print('You need root permissions to run this program!')
        sys.exit(1)
    ShuttleBackup()

if __name__ == "__main__":
    main()