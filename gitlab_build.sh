#!/usr/bin/env bash
echo "******** install ********"
apt-get -y update
echo "******** OS dependencies ********"
apt-get -y install python3-pip
apt-get -y install python3-dev python3-setuptools
apt-get -y install git
apt-get -y install supervisor
echo "******** Django dependencies ********"
pip install --upgrade pip
pip install -r requirements.txt
echo "******** zone install step ********"
pip freeze
echo "******** finish ********"