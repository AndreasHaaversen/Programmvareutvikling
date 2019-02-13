#!/usr/bin/env bash
echo "**************************************"
echo "******** Pip dependencies get ********"
echo "**************************************"
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
echo "***********************************************"
echo "******** Pycodestyle Style Guide check ********"
echo "***********************************************"
pycodestyle .
echo "************************"
echo "******** Finish ********"
echo "************************"
