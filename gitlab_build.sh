#!/usr/bin/env bash
echo "*************************"
echo "******** Install ********"
echo "*************************"
apt-get -y update
echo "*********************************"
echo "******** OS dependencies ********"
echo "*********************************"
#apt-get -y install apt-utils
#apt-get -y install python3-pip python3-dev python3-setuptools
echo "*************************************"
echo "******** Django dependencies ********"
echo "*************************************"
pip install --upgrade pip
pip install -r requirements.txt
echo "***********************************"
echo "******** Zone install step ********"
echo "***********************************"
pip freeze
echo "************************"
echo "******** Finish ********"
echo "************************"