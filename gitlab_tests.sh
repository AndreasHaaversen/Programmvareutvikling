#!/usr/bin/env bash
echo "************************"
echo "******** Update ********"
echo "************************"
apt-get -y update
echo "*********************************"
echo "******** OS dependencies ********"
echo "*********************************"
apt-get install -y ruby-dev
gem install dpl
dpl --provider=heroku --app=tdt4140-51 --api-key=$HEROKU_STAGING_API_KEY
#apt-get -y install apt-utils
#apt-get -y install python3-pip python3-dev python3-setuptools
echo "*************************************"
echo "******** Django dependencies ********"
echo "*************************************"
#pip install --upgrade pip
pip install -r requirements.txt
echo "***********************************"
echo "******** Zone install step ********"
echo "***********************************"
python -V
pip freeze
echo "************************"
echo "******** Finish ********"
echo "************************"