#!/usr/bin/env bash
echo "************************"
echo "******** Update ********"
echo "************************"
pacman -Syu python3 mariadb-clients --noconfirm
#echo "*********************************"
#echo "******** OS dependencies ********"
#echo "*********************************"
#apt-get install -y mysql-client
echo "**********************************"
echo "******** Pip dependencies ********"
echo "**********************************"
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
pip3 install --upgrade pip
pip3 install -r requirements.txt
echo "***********************************"
echo "******** Zone install step ********"
echo "***********************************"
python -V
pip3 freeze
echo "*************************************"
echo "******** Database setup step ********"
echo "*************************************"
mysql -u root -pdev -h mysql -Bse "CREATE USER 'dev'@'localhost' IDENTIFIED BY 'dev';GRANT ALL PRIVILEGES ON *.* TO 'dev'@'localhost';"
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
