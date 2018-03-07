# ShuttleBackup
With ShuttleBackup you can easily automate the backup process of Rocket.Chat's database.

# How to install
Place the compiled and crontab files in the appropriate directory using the following commands:
```bash
sudo mkdir /opt/shuttlebackup
sudo mv ~/ShuttleBackup/ShuttleBackup/shuttlebackup.py /opt/shuttlebackup/shuttlebackup.py
sudo mv ~/ShuttleBackup/ShuttleBackup/shuttletab /opt/shuttlebackup/shuttletab
```

Now add the cron job to the root user:
```bash
sudo crontab /opt/shuttlebackup/shuttletab
```

You can check if it was properly added using the command:
```bash
sudo crontab -l
```

# Add emails to notify in case off backup error
For now the only way to add emails is manual.
Open the file "/root/.shuttle.mails" and add each email on a new line.
```bash
sudo nano /root/.shuttle.mails
```
Example file content:
```
example@example.com
shuttle@shuttle.com
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
