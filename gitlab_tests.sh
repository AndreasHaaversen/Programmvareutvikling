#!/usr/bin/env bash
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
echo "*************************************"
echo "******** Django default test ********"
echo "*************************************"
python3 ./nigirifalls/manage.py test -k
echo "************************"
echo "******** Finish ********"
echo "************************"
