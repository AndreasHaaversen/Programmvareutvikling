#!/usr/bin/env bash
# Testing script
echo "Hostname: " $(cat /etc/hostname)
echo "************************"
echo "******** Update ********"
echo "************************"
apt-get -y update
echo "*********************************"
echo "******** OS dependencies ********"
echo "*********************************"
# NB: For when I get a GNU/Linux install or Hyper-V, it is wise to combine Python image with mariadb-client baked-in to then
# Docker image in order to avoid having to install it every time the pipeline runs.
apt-get install -y mariadb-client
echo "**********************************"
echo "******** Pip dependencies ********"
echo "**********************************"
#pip install --upgrade pip
pip install -r gitlabrequirements.txt
echo "***********************************"
echo "******** Zone install step ********"
echo "***********************************"
python -V
pip freeze
echo "*************************************"
echo "******** Database setup step ********"
echo "*************************************"
echo "SELECT 'OK';CREATE USER 'dev'@'mariadb' IDENTIFIED BY 'dev';GRANT ALL PRIVILEGES ON *.* TO 'dev'@'mariadb' WITH GRANT OPTION;" | mysql --user=root --password=rootpassword --host=mariadb nigirifalls_db
python3 ./nigirifalls/manage.py makemigrations
python3 ./nigirifalls/manage.py migrate
echo "*************************************"
echo "******** Django default test ********"
echo "*************************************"
python3 ./nigirifalls/manage.py test -k
echo "***********************************************"
echo "******** Pycodestyle Style Guide check ********"
echo "***********************************************"
if pycodestyle . --ignore=E501; then
    printf 'OK\n'
else
    printf 'Failed\n'
fi
echo "************************"
echo "******** Finish ********"
echo "************************"