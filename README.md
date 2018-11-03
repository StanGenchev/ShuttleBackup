# ShuttleBackup
ShuttleBackup can create and store backup archives of Rocket.Chat's database.
It has the optional feature to send a notification via email in case of error and can be automated using cron.
Note that this works only with the 'snap' version of Rocket.Chat.

## How to install
Clone the repo:
```bash
git clone https://github.com/StanGenchev/ShuttleBackup.git
```

Install dependencies:

If running Debian/Ubuntu:
```bash
sudo apt install python3 python3-pip
sudo pip3 install meson ninja
```

If running RedHat/CentOS/Fedora
```bash
sudo yum install python3 python3-pip postfix mailx
sudo pip3 install meson ninja
```

Build and install:

```bash
cd ShuttleBackup && meson builddir
cd builddir && sudo ninja install
```

## Backup archives and logs location
You can find the archives in:

```bash
/var/shuttlebackup/archives
```

and the mongo dump logs in:

```bash
/var/shuttlebackup/logs
```

## How to add/show/clear emails

You can add multiple emails to which the notifications will be send to.

```bash
sudo shuttlebackup --add-emails
```

To show all emails:

```bash
sudo shuttlebackup --show-emails
```

To remove select email:

```bash
sudo shuttlebackup --remove-email
```

To clear all emails:

```bash
sudo shuttlebackup --clear-emails
```

## How to create/show/delete backups

To create a backup:

```bash
sudo shuttlebackup --backup
```

To show all backups:

```bash
sudo shuttlebackup --show-backups
```

To remove select backups:

```bash
sudo shuttlebackup --remove-backup
```

To delete all backups:

```bash
sudo shuttlebackup --clear-backups
```

## How to show/change the number of backup archives

The default number is ten.
To show the current number:

```bash
sudo shuttlebackup --show-count
```

To change the number:

```bash
sudo shuttlebackup --change-count
```

## How to automate it

Add the following lines to your crontab:
```bash
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
45 23 * * *   /usr/bin/python3 /usr/bin/shuttlebackup
```

'23' is the hour and '45' is the minute.

You can add tasks to cron using the command:
```bash
sudo crontab -e
```
