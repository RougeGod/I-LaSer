#!/usr/bin/env bash
set -e

#This script installs required software for hosting a LaSer research server

apt-get update
apt-get --assume-yes upgrade

#Set local time to Halifax
timedatectl set-timezone America/Halifax

#Make sure loopback device has IP
ip addr add 127.0.0.1 dev lo

#Install basic tools
apt-get --assume-yes install vim git zip unzip python-pip
pip install FAdo

#Install Apache2 and Django if they do not exist
if [ ! -f /etc/apache2/apache2.conf ];
then
  #Install Apache2 and modules
  apt-get --assume-yes --quiet install \
    apache2 apache2-utils \
    python-django libapache2-mod-python libapache2-mod-wsgi
  service apache2 restart

  #Enable necessary Apache2 mods
  a2enmod wsgi
  #a2enmod python
fi

#Enable LaSer site in Apache2
if [ -h /etc/apache2/site-enabled/LaSer.conf ];
then
  echo "LaSer site already enabled in Apache2"
else
  cp /var/www/project/LaSer.conf /etc/apache2/sites-available/LaSer.conf
  chown root:www-data /var/www/project/laser/transducer/code_gen
  chmod 775 /var/www/project/laser/transducer/code_gen
  a2ensite LaSer
  service apache2 reload
fi

#Ensure MySQL is installed
if command -v mysql 1>/dev/null;
then
  echo "MySQL is already installed."
else
  #Load debconf with password to avoid interaction during install
  MYSQL_ROOT_PASS="mySecretPassword"
  echo "mysql-server mysql-server/root_password password $MYSQL_ROOT_PASS" | debconf-set-selections
  echo "mysql-server mysql-server/root_password_again password $MYSQL_ROOT_PASS" | debconf-set-selections
  
  #Install MySQL
  apt-get --assume-yes --quiet install mysql-server python-mysqldb
fi