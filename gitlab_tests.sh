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
pip install --upgrade pip
pip install -r requirements.txt
echo "***********************************"
echo "******** Zone install step ********"
echo "***********************************"
python -V
pip freeze
#echo "*************************************"
#echo "******** Database setup step ********"
#echo "*************************************"
#echo "CREATE USER 'dev'@'mariadb' IDENTIFIED BY 'dev';GRANT ALL PRIVILEGES ON *.* TO 'dev'@'mariadb' WITH GRANT OPTION;" | mysql --user=root --password=rootpassword --host=mariadb nigirifalls_db
if python3 ./nigirifalls/manage.py makemigrations; then
    printf 'OK - Migrations have been made or were already made\n'
else
    printf 'Failed - Could not make necessary migration\n'
	exit 1
fi
if python3 ./nigirifalls/manage.py migrate; then
    printf 'OK - Database migrations succeeded\n'
else
    printf 'Failed - Database migrations failed\n'
	exit 1
fi
echo "*****************************"
echo "******** Django test ********"
echo "*****************************"
cd nigirifalls
if python3 manage.py test -k; then
    printf 'OK - Django tests passed\n'
else
    printf 'Failed - Django tests failed\n'
	exit 1
fi
cd ..
echo "***********************************************"
echo "******** Pycodestyle Style Guide check ********"
echo "***********************************************"
if pycodestyle . --ignore=E501; then
    printf 'OK - All code adheres to PEP8\n'
else
    printf 'Failed - Some code does not adhere to PEP8\n'
	exit 1
fi
echo "************************"
echo "******** Finish ********"
echo "************************"