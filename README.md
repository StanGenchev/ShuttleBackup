# ShuttleBackup
With ShuttleBackup you can easily automate the backup process of Rocket.Chat's database.

# How to install
Place the python and crontab files in the appropriate directory using the following commands:
```bash
git clone https://github.com/StanGenchev/ShuttleBackup.git
cd ShuttleBackup
sudo mkdir /opt/shuttlebackup
sudo mv ./ShuttleBackup/shuttlebackup.py /opt/shuttlebackup/shuttlebackup.py
sudo mv ./ShuttleBackup/shuttletab /opt/shuttlebackup/shuttletab
```

Now add the cron job to the root user:
```bash
sudo crontab /opt/shuttlebackup/shuttletab
```

You can check if it was properly added using the command:
```bash
sudo crontab -l
```

Add email addresses to notify in case of errors:
```bash
sudo /opt/shuttlebackup/shuttlebackup.py --add-mails
```

Clear all emails:
```bash
sudo /opt/shuttlebackup/shuttlebackup.py --clear-mails
```

# Change the time of the backup process

By default the cron job is set to run everyday at 23:45.
If you want to change that you can do it by editing the 'shuttletab' file:
```bash
sudo nano /opt/shuttlebackup/shuttletab
```
The last line will read:
```
45 23 * * *   /usr/bin/python3 /opt/shuttlebackup/shuttlebackup.py
```
The first number is the minute, the second is the hour, and the next three asterisks signify the day of the month, the month and the day of the week.
If you are feeling unsure on how to format them properly you can go to the website "https://crontab.guru/" where you can generate your custom cron job.
