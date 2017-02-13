#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive

# Set provisioning variables
PROJECT_NAME=photosite

DB_USER=dev
DB_PASS=default123

MQ_USER='admin'
MQ_PASS=$DB_PASS
MQ_VHOST='local'

VIRTUALENV_DIR=/home/vagrant/.virtualenvs/$PROJECT_NAME
BASH_RC='/home/vagrant/.bashrc'

echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.6" >> $BASH_RC
source $BASH_RC


# create downloads directory for Python
mkdir -p "/home/vagrant/downloads"
chown vagrant:vagrant /home/vagrant/downloads

# Add RabbitMQ repository signing key and add project repository to aptitude
wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -
echo 'deb http://www.rabbitmq.com/debian/ testing main' | sudo tee /etc/apt/sources.list.d/rabbitmq.list

# Ensure root db user has password set when bypassing console input install
echo "Setting MySQL root password"
debconf-set-selections <<< "mysql-server mysql-server/root_password password $DB_PASS"
debconf-set-selections <<< "mysql-server mysql-server/root_password_again password $DB_PASS"

# Add Redis and python 3.6 PPA
add-apt-repository ppa:chris-lea/redis-server -y
add-apt-repository ppa:jonathonf/python-3.6

# add node and npm
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -

echo "Updating Ubuntu repositories and installed packages"

apt-get update -y
apt-get upgrade -y

echo "Installing required dependencies for project"
apt-get install -y python3-dev autotools-dev blt-dev bzip2 dpkg-dev g++-multilib gcc-multilib libbluetooth-dev libbz2-dev libffi-dev \
    libffi6 libffi6-dbg libgdbm-dev libgpm2 libncursesw5-dev libreadline-dev libsqlite3-dev libssl-dev libtinfo-dev \
    mime-support net-tools python3-crypto python3-mox3 python-ply quilt tk-dev zlib1g zlib1g-dev build-essential libxml2 \
    libxml2-dev libxslt1.1 libxslt1-dev mysql-server-5.6 libmysqlclient-dev rabbitmq-server redis-server python3.6 python3-pip \
    nodejs
apt-get autoremove -y


echo "Setting up mysql with the following:"
echo "  USERNAME: $DB_USER"
echo "  PASSWORD: $DB_PASS"
echo "  DATABASE: $PROJECT_NAME"
echo ""

# Create mysql db with username/password and all privileges
mysql -u root -p$DB_PASS -e "create user '$DB_USER'@'localhost' identified by '$DB_PASS'"
mysql -u root -p$DB_PASS -e "create database $PROJECT_NAME"
mysql -u root -p$DB_PASS -e "grant all privileges on $PROJECT_NAME.* to '$DB_USER'@'localhost'"
mysql -u root -p$DB_PASS -e "flush privileges"

#Configure RabbitMQ
echo "Configuring RabbitMQ"
rabbitmq-plugins enable rabbitmq_management
rabbitmqctl add_user $MQ_USER $MQ_PASS
rabbitmqctl add_vhost $MQ_VHOST
rabbitmqctl set_user_tags $MQ_USER administrator
rabbitmqctl set_permissions -p $MQ_VHOST $MQ_USER ".*" ".*" ".*"
rabbitmqctl delete_user guest

echo "Configuring Virtualenv"

if [[ ! -f /usr/local/bin/virtualenvwrapper.sh ]]; then
    pip3 install -U pip
    pip3 install -U virtualenvwrapper
fi

if ! grep -Fq "WORKON_HOME" $BASH_RC; then
    echo "Exporting virtualenv variables"
    echo "export WORKON_HOME=/home/vagrant/.virtualenvs"  >> $BASH_RC
    echo "export PROJECT_HOME=/home/vagrant/$PROJECT_NAME" >> $BASH_RC
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> $BASH_RC
fi

WORKON_HOME=/home/vagrant/.virtualenvs
PROJECT_HOME=/home/vagrant/$PROJECT_NAME
source /usr/local/bin/virtualenvwrapper.sh

# mkvirtualenv -p "/usr/bin/python3.6" --clear -a "/home/vagrant/project" $PROJECT_NAME
mkvirtualenv -p "/usr/bin/python3.6" -r "/home/vagrant/project/requirements.txt" -a "/home/vagrant/project" $PROJECT_NAME

chown -R vagrant:vagrant $WORKON_HOME