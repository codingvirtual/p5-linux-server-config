Fullstack Nanodegree - Project 5 - Linux Server Configuration
=============================================================

Table of Contents
-----------------

*	Project Background
*	Prerequisites
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

1.	You will need somewhere to run all of this. In the Udacity project, an
Amazon EC2 instance was provided for us that contained the base build of
Ubuntu 14.04 Server Edition along with a private SSH key file that allowed
us to log into the instance. If you are starting from bare metal, you will
have to take care of getting Ubuntu 14.04 Server installed first. You will
also need to generate a set of SSH keys to log into it with. Steps for this
will be lightly discussed below.
2.	The catalog project that is supplied requires a Google developer's account
in order to enable sign-in with a Google Plus ID. You will have to create a
project in the developer's console mainly to be able to generate a client
secrets file for the catalog project. If you choose not to install the catalog
project (which is entirely optional), you are off the hook for this pre-req
entirely.


Create development environment
Connect to environment
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
https://discussions.udacity.com/t/p5-how-i-got-through-it/15342
https://github.com/robertavram/Linux-Server-Configuration
https://docs.google.com/document/d/1J0gpbuSlcFa2IQScrTIqI6o3dice-9T7v8EDNjJDfUI/pub?embedded=true
https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps