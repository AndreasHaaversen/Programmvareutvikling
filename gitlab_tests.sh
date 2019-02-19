#!/usr/bin/env bash
echo "************************"
echo "******** Update ********"
echo "************************"
apt-get -y update
echo "*********************************"
echo "******** OS dependencies ********"
echo "*********************************"
apt-get install -y mariadb-client mariadb-server
echo "**********************************"
echo "******** Pip dependencies ********"
echo "**********************************"
#pip install --upgrade pip
pip install -r requirements.txt
echo "***********************************"
echo "******** Zone install step ********"
echo "***********************************"
python -V
pip freeze
service mariadb start
service mysql start
echo "*************************************"
echo "******** Database setup step ********"
echo "*************************************"

mysql -u root -h localhost -Bse "create database nigirifalls_db default character set utf8 default collate utf8_bin;GRANT ALL PRIVILEGES ON nigirifalls_db.* to dev@'localhost' IDENTIFIED BY 'dev';"
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
