Fullstack Nanodegree - Project 5 - Linux Server Configuration
=============================================================

Table of Contents
-----------------

*	Project Background
*	Prerequisites
*	Overall Process
*	Step-by-step
*	Appendix - Resources


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
4.	Configure SSH to work on port 2200 instead of 22 and lock down 'root'
5.	Configure the Uncomplicated Firewall (UFW) to allow traffic only on ports
80 (HTTP), 123 (NTP), and 2200 (which we will use for SSH)
6.	Install Apache
7.	Configure the user created in the steps above, which includes generating
SSH keys.
8.	Install several supporting packages like Git, Flask, SQLAlchemy and Postgres.
9.  Clone and set up the provided catalog project (optional)
10. Configure Apache to serve the catalog
11.	Configure Postgres for the project


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

#### 1 - Update the server to the latest software.

Log in to the server using the root login and issue the following commands:

	apt-get update
	apt-get upgrade

The first of these tells the system to go out and fetch the latest list of
versions for all of the official packages on your machine.

The second command tells the system to compare the currently installed versions
with what is in the list that was just updated with the 'update' command and
if any newer versions are available, install them. You will typically be asked
to confirm this if the system finds updates to install.

Also, you may encounter a message that comes up on its own colored screen and
asks you about which version of a "grub"-related file you want to keep. You
should choose to install the package maintainer's version.

When this is all done, you may notice that the output shows that some number
of packages were "held back" (on my machine, it was 4). To get these to
properly install, you need to issue this command:

	apt-get dist-upgrade

While it's not strictly required, it would probably be a good idea to reboot
at this point. You can do that by typing either "reboot" or
"shutdown -r now" (the first one is just a shorthand to the 2nd one; they
both do the same thing).

#### 2 - Set up Unattended Updates

Next, we will set the machine up to automatically pull down and install upgrades
in an unattended fashion. This will help ensure that the latest security patches
(among other things) are installed at all times. Type the following:

	dpkg-reconfigure -plow unattended-upgrades

It will ask for confirmation. Make sure that <yes> is highlighted (or press the
'y' key) and press return.

Now, we'll configure the timezone to UTC. Type:

First, we will install ntp, the network time protocol:

	apt-get install -y ntp

Now, we'll configure the time zone on the server to UTC.

	dpkg-reconfigure tzdata

This will bring up a new screen offering you a number of time zone choices,
but none of them include UTC. As a result, arrow down to None of the Above and
then press return.

Then another screen will come up and you will find UTC down the list. Arrow
down to it and select it then press return.

#### 3 - Add a User and prepare for key-based authentication

Now we need to add the "grader" user to the system. To do that, type:

	adduser grader

This will bring up a series of questions. The first one will ask you for the
user's full name. Type "Udacity Grader" or whatever else you'd like.

You can accept the other defaults. When it gets to the password, just enter
'grader' as it won't matter when we're all done (we'll be setting the user up
to connect using an RSA key and disabling password-based authentication).

Next, we need to give this new user the ability to issue "sudo" commands. To
do this, we need to add the to the "sudoers" file. The best way to do this
is to create a file for the user inside the /etc/sudoers.d directory. Type:

	cd /etc/sudoers.d

Now create new file by typing:
	vi grader

When vi opens up, type the letter 'i' (to insert new text) and then type the
text below EXACTLY as it appears:

	grader ALL=(ALL) NOPASSWD:ALL

When you are done, type this:

	:wq

to write the changes. That's a colon and then wq.

Next, we need to set the proper privileges on this new file so that the owner
(root) and the group (root) can read the file but nobody else can. To do that,
type:

	chmod 440 grader

Now, we need to confirm that this sequence of commands worked (we have a user
'grader' that has 'sudo' permission). Here's how:

Type:

	su grader
	cd /etc
	sudo less sudoers

The first command basically "logs you in" as the user grader. Then you change
to /etc directory and try to examine the sudoers file using the 'less' command.
If you don't get an error (and you should not if you followed the steps
correctly), then everything is set up correctly.

Now, let's back out of being logged in as 'grader' by typing:

	exit

Now we'll generate the needed ssh keys to enable key-based authentication 
instead of using the username/password login prompt.

ON YOUR LOCAL LINUX or MAC MACHINE (NOT THE SERVER), create a key pair using
these commands:

	ssh-keygen -t rsa

This will then prompt you for the name of the key file to generate. Name the
file linuxCourse_rsa. You will be asked as well for a passphrase, which you
would normally want to do (if you set a passphrase, you will be required
to enter it each time you go to use the key in the future, so it adds a
measure of security should the key be compromised). For this project, you do
not need a passphrase (just hit enter to leave it blank).

This will create two files in whatever directory you are in when you issue
the ssh-keygen command. The file that ends with .pub is the public key
and 'linuxCourse_rsa' is the private key. You should NEVER give out the private
key and should take care to protect it.

Now we need to get the contents of the public key and put it on the server.
On your local machine, type:

	cat linuxCourse_rsa.pub

highlight the output and copy it, then switch back over to your server terminal
window and type the following:

	su grader
	cd ~
	mkdir .ssh
	cd .ssh
	vi authorized_keys

Now, press 'i' to insert new text and then paste the contents of the
linuxCourse_rsa.pub file you catted earlier. Finally, to save this file type:

	:wq!
	
Now set the privileges so that only the 'grader' user has write access to this
file.

	chmod 644 authorized_keys

and set the privileges on the .ssh folder such that only the 'grader' user
can do anything inside that folder:

	cd ..
	chmod 700 .ssh

Exit out of the grader login again by typing:

	exit

You should now be back at the root prompt.

#### 4 - Configuring SSH for a different port

Now with the user stuff out of the way, let's move on to configuring ssh to
work on port 2200 (instead of the default 22), set up logging in using an
ssh key file, and disable password-based login.


First, we need to change ssh to work on port 2200. To do that, type:

	vi /etc/ssh/sshd_config

This will open the config file in vi. Now, find line that says Port 22 and
navigate down to it. Change the line to read as follows:

	Port 2200

Remember to save the changes. You can type :wq! to save changes.

To get this change to take effect, you need to restart the ssh service. To do
that, type:

	service ssh restart

And finally, log off and then reconnect on port 2200. Type:

	exit

Now log back on as root, but use this (notice the -p 2200 on the end):

	ssh -i ~/.ssh/udacity_key.rsa root@xx.xx.xx.xx -p 2200

Now that we have ssh reconfigured to port 2200, we're going to add some
restrictions so that the 'grader' user is the only user that can ssh into
the machine. Specifically, this will DISALLOW logging in via ssh as root,
which will help secure the box.

	cd /etc
	visudo

Now find the line that looks like this:

	root   ALL=(ALL:ALL) ALL

and comment it out by putting a pound sign (#) in front of it. It should look
like this when you are done:

	#root   ALL=(ALL:ALL) ALL

then press ctrl-x (this assumes that visudo opened using the nano text editor).
Press y to save the file and then press return to accept the default file name
that is offered (it will look like you're creating a .tmp file but visudo
takes care of making it the real sudoers file for you).

Now let's confirm the change worked by checking the contents of the sudoers
configuration (note: this is different than the sudoers.d directory; you
should never directly alter the sudoers file - that's what 'visudo' is for;
however, it *IS* ok to create files in sudoers.d as we did earlier).

Now type:

	less sudoers

and make sure that the line you changed above is properly commented out.


#### 5 - Set up Uncomplicated Firewall (UFW)

Next, we need to set up the Uncomplicated Firewall with a few basic config
steps. The following commands will do the work for you. Note that if you
configured ssh on a port other than 2200, you should use that value below
instead of 2200.

	ufw allow http
	ufw allow ntp
	ufw allow 2200
	ufw default deny incoming
	ufw default allow outgoing
	ufw enable

#### 6 - Install Apache, Postgres, and Python tools

Now we need to install the Apache web server, Python tools related to both
development and integration with Apache, and Postgres. Later we'll install
some additional utilities that will allow you to run the P3 project on this
server.

	apt-get install apache2
	apt-get install -y postgresql
	apt-get install python-setuptools libapache2-mod-wsgi
	apt-get install python-pip
	apt-get install -y python-dev
	apt-get install -y python-psycopg2
	apt-get install libpq-dev

#### 7 - Additional 'grader' User Configuration

These first few steps will modify the default profiles that get used when
you log into the box. By default, some of colors that both the console and
the vi text editor use are very difficult to see in some circumstances. To
make that easier to see, the following edits will make changes to the color
scheme. Note that you can pick different colors if you choose to.

Assuming you are at a root prompt, "login" to the grader account again by
typing:

	su grader

Now, issue the following commands:

	cd ~
	mv .profile .bash_profile
	vi .bash_profile

go to the end of the .bash_profile file and append this to the end of the file:

	alias ls='ls -la --color'
	
	LS_COLORS='di=1:fi=0:ln=31:pi=5:so=5:bd=5:cd=5:or=31:mi=0:ex=35:*.rpm=90'
	export LS_COLORS

then to save it, type:

	:wq!

The alias command sets things up so that every time you type just "ls" you
actually get 'ls -la --color' via the alias substitution method. It's basically
like a macro.

Optionally, you can now set the color scheme for the vi editor (if you don't
use vi, you can skip this part):

You should still be in your home directory. Type:

	vi .vimrc

press the 'i' key (to insert) then type:

	highlight comment ctermfg=cyan

then to save changes, type:

	:wq!

Finally, exit out of the grader login by typing:

	exit


#### 8 - Install additional utilities for P3 Project

If you intend to run your Udacity P3 project, you will need to follow the
remaining steps below to get everything set up. These commands will install
git, Flask, SQLAlchemy, OAuth2, and tools to access the Postgres database
via Python & Flask. NOTE: You will need to modify your P3 project to work
with Postgres. Instructions for that are mostly beyond the scope of this
document, though some details are provided further below that should help
you modify your project.

	apt-get install git
	apt-get install -y python-flask
	apt-get install -y python-sqlalchemy
	pip install Flask
	pip install sqlalchemy
	pip install oauth2client
	pip install -U psycopg2

#### 9 - Clone your "P3" Project

Next, you will clone your P3 Project to the server using the HTTPS link (not
the SSH link). Open your web browser on your local machine and go to your
project repo. Click the button to show the HTTPS clone link and copy it.

Go back to the terminal window for the server and type this:

	cd /var/www
	sudo git clone <paste HTTPS link>

This will clone your project to the web directory. Git will create a new
directory inside /var/www/ with the name of your project. Do an 'ls'' to confirm
what the directory name is (should be same as your project repo name). Next,
cd into that directory and set the .git subdirectory to be accessible only
by you:

	sudo chmod 400 .git

#### 10 - Configure Apache ###

The following instructions are adapated from detailed information at the
following website:

https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps

The steps below are an example based on my project that is included in the
repo you are reading this README file in. I included it as a reference so
you can get an idea of how to modify your project.

First, we need to configure Apache to serve the project as a virtual host. To
do that, we need to create a configuration file for the project. In this
example, I am naming the file "catalog.conf" but you can name yours as you
like. Just make sure you use that name anywhere else in the instructions
below where I reference catalog.conf

	sudo vi /etc/apache2/sites-available/catalog.conf

You should now be at a blank screen in vi. Type 'i' to insert text, and then
type the following, substituting your info where you see info within pairs of
pound signs (##). You should remove the ## that both leads and trails that
info and put your relevant info there instead. NOTE: you will see less-than and
greater-than characters below - you *DO* type those - they are part of the
config file.

	<VirtualHost *:80>
                ServerName ##your_environment##.us-west-2.compute.amazonaws.com
                ServerAdmin ##your_email_address##
                WSGIScriptAlias / /var/www/##your_project_directory##/flaskapp.wsgi
                <Directory /var/www/##your_project_directory##/>
                        Order allow,deny
                        Allow from all
                </Directory>
                Alias /catalog/static /var/www/##your_project_directory##/catalog_main/static
                <Directory /var/www/##your_project_directory##/catalog/static/>
                        Order allow,deny
                        Allow from all
                </Directory>
                ErrorLog ${APACHE_LOG_DIR}/error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/access.log combined
	</VirtualHost>

After typing in the above, save it by typing:

	:wq!

Now, you need to create a simple .wsgi file that will "point" to your project's
actual run file (the .py file that starts your application). To do that, type:

	sudo vi /var/www/##your_project_directory##/flaskapp.wsgi

You will be at a blank vi screen. Next, type this:

	import sys
	import logging
	logging.basicConfig(stream=sys.stderr)
	sys.path.insert(0,"/var/www/##your_project_directory##/")

	from catalog_main import app as application

KEY NOTE: The last line above is specific to my P3 project. Within my project,
there is a directory called "catalog_main" that is a Python package (note the
presence of the __init__.py file - that makes it a package). My main app is defined
in that directory. Adapt this line to match your project. It's that line that
Apache will use to start up your app.

Now, you need to enable the new virtual host in Apache. Earlier, you created
a config file for Apache. In my example, it was named catalog.conf. If you
gave it a different name, you need to change the next line below and put
whatever you used in front of the .conf in the line below instead of catalog.

	sudo a2ensite catalog

Now, for a little additional security, we'll disable the default site that is
usually at Port 80 by issuing the following command:

	sudo a2dissite 000-default

To make these changes active, you now need to restart Apache, but we'll save
that step for a bit further down after we get Postgres set up.


#### 11 - Configure Postgres ###

The following instructions are adapted from a tutorial on securing Postgres
at Digital Ocean at the link below:

https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps

When you install Postgres, it creates an account with the name postgres. We
need to use that account to configure the Postgres server. To do that, type:

	sudo -i -u postgres

You will now be at a postgres prompt. From there, enter the psql command line
tool to set up the database and user. Type the following commands:

	psql

Now you will be in the Postgres command line interface where you can define
the tables for your project database. You'll need to adapt all of the following
to your project. See the P3 subdirectory of this repo to understand how the
commands below relate to the database my project uses so you an determine
how to modify them to suit your project.

	CREATE ROLE catalog WITH LOGIN password 'catalog';
	CREATE DATABASE catalog WITH OWNER catalog;
	\c catalog
	REVOKE ALL ON SCHEMA public FROM public;
	GRANT ALL ON SCHEMA public TO catalog;

Exit out of psql by typing:

	\q

Then exit out of the postgres user account by typing:

	exit

Now, the last steps are to restart the Apache server and make one last check
for any needed software updates. To do that, type:

	sudo service apache2 restart
	sudo apt-get update
	sudo apt-get upgrade

#### Appendix - Resources

The following resources were all instrumental in helping me configure and
document all of the above.

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