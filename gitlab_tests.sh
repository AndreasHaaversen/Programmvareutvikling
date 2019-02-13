#!/usr/bin/env bash
echo "************************"
echo "******** Update ********"
echo "************************"
apt-get -y update
echo "****************************************"
echo "******** OS Docker dependencies ********"
echo "****************************************"
apt-get -y install mysql-client
echo "**********************************"
echo "******** Pip dependencies ********"
echo "**********************************"
#pip install --upgrade pip
pip install -r requirements.
service mysql start
echo "***********************************"
echo "******** Zone install step ********"
echo "***********************************"
python -V
pip freeze
echo "*************************************"
echo "******** Database setup step ********"
echo "*************************************"
mysql -u root -pdev -Bse "CREATE USER 'dev'@'localhost' IDENTIFIED BY 'dev';GRANT ALL PRIVILEGES ON *.* TO 'dev'@'localhost';"
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
