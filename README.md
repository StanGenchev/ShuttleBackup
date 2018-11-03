# ShuttleBackup
With ShuttleBackup you can easily automate the backup process of Rocket.Chat's database.
It will create backup archives in '/var/shuttlebackup/archives' and in case of error it will send notification via email.
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

## How to add/show/clear emails

You can add multiple emails to which the data will be send to.

```bash
shuttlebackup --add-emails
```

To show all emails:

```bash
shuttlebackup --show-emails
```

To remove select email:

```bash
shuttlebackup --remove-email
```

To clear all emails:

```bash
shuttlebackup --clear-emails
```

## How to create/show/delete backups

To create a backup:

```bash
shuttlebackup --backup
```

To show all backups:

```bash
shuttlebackup --show-backups
```

To remove select backups:

```bash
shuttlebackup --remove-backup
```

To delete all backups:

```bash
shuttlebackup --clear-backups
```

## How to show/change the number of backup archives

The default number is ten.
To show the current number:

```bash
shuttlebackup --show-count
```

To change the number:

```bash
shuttlebackup --change-count
```

## How to automate it

Add the following lines to your crontab:
```bash
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
45 23 * * *   /usr/bin/python3 /usr/local/bin/shuttlebackup
```

'23' is the hour and '45' is the minute.

You can add tasks to cron using the command:
```bash
sudo crontab -e
```