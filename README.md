Fullstack Nanodegree - Project 5 - Linux Server Configuration
=============================================================

Table of Contents
-----------------

*	Project Background
*	Prerequisites
*	Overall Process
*	Step-by-step
*	Resources


### Project Background

The purpose of this project is to gain an understanding of how to configure
an Ubuntu server "out of the box" in such a way that it is at least reasonably
secure at the outset. Once properly configured, a Python-based application that
serves a simple catalog of items is then configured along with the supporting
tools such as Apache2 and Postgres.

### Prerequisites

Perhaps the most important prerequisite of this project is patience and
determination. Creating a set of steps that one can follow precisely is
nearly impossible given the literally limitless variations of hardware,
software, and knowledge level of the reader. For that reason, you should
be prepared to do quite a bit of additional reading to supplement your
understanding, though I'll do my best to thoroughly explain things here to
try to limit how many other resources you need to go to.

Here are some basic prerequisites:

1.	 These instructions are written specifically to align with the Project 5
requirements and resources from the Udacity Fullstack Nanodegree. As such,
the entire process assumes that you are starting out with the development
environment that Udacity provides for the project, which is a pre-built
Ubuntu 14.04 Server build running on an Amazon EC2 instance. The root account
*is* enabled for login, which is not typically the case when you install
Ubuntu server on your own. There's an entire set of additional steps you'd need
to take if you are installing Ubuntu Server on your own from scratch that I
have not covered here.
2.	The catalog project that is supplied requires a Google developer's account
in order to enable sign-in with a Google Plus ID. You will have to create a
project in the developer's console mainly to be able to generate a client
secrets file for the catalog project. If you choose not to install the catalog
project (which is entirely optional), you are off the hook for this pre-req
entirely.
3.	It should be obvious, but just to be thorough, I'll mention the fact that
for any of this to work, you're going to need an Internet connection :-).

That's about it for requirements.

### Overall Process

The overall process that you are about to follow has a logical sequence to it
(well, it's logical to me at least) that should be done in the order listed.
You *can* do things in a different order, but be sure to read the steps in
order first as some of them assume that you are in a particular directory at
the start of the step (because that's where you were at the end of the last
step).

In general, here's what we're going to do:
1.	Get Ubuntu updated with the latest software
2.	Set up automatic unattended upgrading
3.	Add a user and give the user the ability to SSH to the machine as
well as give them sudo privileges
4.	Configure SSH to work on port 2200 instead of 22
5.	Configure the Uncomplicated Firewall (UFW) to allow traffic only on ports
80 (HTTP), 123 (NTP), and 2200 (which we will use for SSH)
6.	Install Apache
7.	Configure the user created in the steps above, which includes generating
SSH keys.
8.	Lock down the root account
9.	Install several supporting packages like Git, Flask, SQLAlchemy and Postgres.
10. Clone and set up the provided catalog project (optional)
11. Configure Apache to serve the catalog
12.	Configure Postgres for the project


### Step By Step

#### 0 - Set up Ubuntu (for non-Udacity students)
The first thing to do is to get your base Ubuntu Server setup operational.
This step is only required for those of you starting from scratch. Udacity
students will start with Step 1.
The download for Ubuntu Server is here:
http://www.ubuntu.com/download/server
And the installation instructions are here:
http://www.ubuntu.com/download/server/install-ubuntu-server
Finally, the admin manual for Ubuntu Server is here:
https://help.ubuntu.com/lts/serverguide/index.html

At some point in the steps below, we are going to disable the ability to
log in using a username and password and instead require the use of SSH
keys. The environment that Udacity provides comes with the key already created,
but if you are building from scratch, you will need to generate a set of SSH
keys **ON YOUR PC, NOT ON THE SERVER.** You will copy the public key to the
server (the file that ends with .pub) but keep the private key on your personal
workstation. Apologies in advance, but I have not detailed the steps for this
here. However, further below you will see that a set of keys is generated for
the user that will be created. You can follow those steps to create a set
of keys, and you need to do that NOW because shortly we'll be shutting off
access via username/password.

*NOTE:* For Udacity students, the development environment is provided for you,
so you will skip the above step and instead, log into the environment and
continue from here.

1.	Update the server to the latest software.
sudo apt-get update
sudo apt-get upgrade
"install package maintainer's version" when asked about grub file
apt-get dist-upgrade
dpkg-reconfigure -plow unattended-upgrades
'yes' to allowing the unattended upgrades
dpkg-reconfigure tzdata
	none of the above
	select UTC

### add grader user ###
adduser grader
	set Full Name to "Udacity Grader"
	set passwod to "grader"

cd /etc/sudoers.d
vi grader
	grader ALL=(ALL) NOPASSWD:ALL
chmod 440 grader

confirm sudo worked:
su grader
cd /etc
sudo less sudoers
(should work)

exit (gets you back to root user login)

### Set up ssh over 2200 ###
vi /etc/ssh/sshd_config

near top, find line that says Port 22
change to:
Port 2200
:wq!

service ssh restart

exit (completely log off)

Now log back on as root, but use this (notice the -p 2200 on the end):
ssh -i ~/.ssh/udacity_key.rsa root@52.25.121.39 -p 2200


### set up firewall ###

ufw allow http
ufw allow ntp
ufw allow 2200
ufw default deny incoming
ufw default allow outgoing
ufw reload

### Install Apache ###
apt-get install apache2
sudo reboot
wait 60 seconds

while waiting, open terminal on your local machine
ssh-keygen -t rsa
	name the file linuxCourse_rsa
	no passphrase

cat linuxCourse_rsa.pub
highlight and copy
connect to server again as root

su grader
cd ~
mkdir .ssh
cd .ssh
vi authorized_keys
	press 'i' to insert
	paste (the contents of the linuxCourse_rsa.pub file you catted earlier)
	:wq! to save 
chmod 400 authorized_keys


### color mods ###

cd ~
mv .profile .bash_profile
vi .bash_profile
go to end of file
A (append)
type this:

alias ls='ls -la --color'

LS_COLORS='di=1:fi=0:ln=31:pi=5:so=5:bd=5:cd=5:or=31:mi=0:ex=35:*.rpm=90'
export LS_COLORS

then :wq! to save it

now:
vi .vimrc

i (to insert) then type:

highlight comment ctermfg=cyan

then type :wq! to save



exit
exit
from terminal on your local machine, now try to connect this way:
ssh -i ~/.ssh/linuxCourse_rsa grader@52.25.121.39 -p 2200

cd /etc
sudo visudo
	find the line like this:
	root   ALL=(ALL:ALL) ALL

	and comment it out. It should look like this when you are done:
	#root   ALL=(ALL:ALL) ALL

	then press ctrl-x
	press y to save the file
	press return to accept the default

type:
sudo less sudoers
and make sure that the line you changed above is properly commented out.

sudo vi /etc/ssh/sshd_config
go to the end of the file and type:
AllowUsers grader


sudo apt-get install -y ntp
sudo apt-get install python-setuptools libapache2-mod-wsgi
sudo apt-get install python-pip
sudo apt-get install -y postgresql
sudo apt-get install -y python-dev
sudo apt-get install git
sudo apt-get install -y python-flask
sudo apt-get install -y python-sqlalchemy
sudo apt-get install -y python-psycopg2
sudo apt-get install libpq-dev python-dev
sudo pip install Flask
sudo pip install sqlalchemy
sudo pip install oauth2client
sudo pip install -U psycopg2

### clone project ###

open web browser and go to your project repo
click the button to show the HTTPS clone link
copy it

go back to the server
cd /var/www
git clone <paste HTTPS link>
this will clone your project to the web directory.

do an ls to see what the directory name is (should be same as your project repo name)
cd into that directory
sudo chmod 400 .git

### Configure Apache ###
https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps

sudo vi /etc/apache2/sites-available/catalog.conf
	make changes
	<VirtualHost *:80>
                ServerName ec2-52-25-121-39.us-west-2.compute.amazonaws.com
                ServerAdmin codingvirtual@gmail.com
                WSGIScriptAlias / /var/www/p5-linux-server-config/flaskapp.wsgi
                <Directory /var/www/p5-linux-server-config/>
                        Order allow,deny
                        Allow from all
                </Directory>
                Alias /catalog/static /var/www/p5-linux-server-config/catalog_main/static
                <Directory /var/www/p5-linux-server-config/catalog/static/>
                        Order allow,deny
                        Allow from all
                </Directory>
                ErrorLog ${APACHE_LOG_DIR}/error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

sudo vi /var/www/<project-root>/flaskapp.wsgi
	import sys
	import logging
	logging.basicConfig(stream=sys.stderr)
	sys.path.insert(0,"/var/www/p5-linux-server-config/")

	from catalog import app as application


sudo a2ensite catalog
sudo a2dissite 000-default



### set up Postgres user ###
https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps

sudo -i -u postgres
psql
CREATE ROLE catalog WITH LOGIN password 'catalog';
CREATE DATABASE catalog WITH OWNER catalog;
\c catalog
REVOKE ALL ON SCHEMA public FROM public;
GRANT ALL ON SCHEMA public TO catalog;

sudo service apache2 restart 
sudo apt-get update
sudo apt-get upgrade

### Resources
Ubuntu Server Download
	http://www.ubuntu.com/download/server
Ubuntu Installation Instructions
	http://www.ubuntu.com/download/server/install-ubuntu-server
Ubuntu Server Guide (manual):
	https://help.ubuntu.com/lts/serverguide/index.html

https://discussions.udacity.com/t/p5-how-i-got-through-it/15342
https://github.com/robertavram/Linux-Server-Configuration
https://docs.google.com/document/d/1J0gpbuSlcFa2IQScrTIqI6o3dice-9T7v8EDNjJDfUI/pub?embedded=true
https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps