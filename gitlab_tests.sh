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
echo "************************"
echo "******** Finish ********"
echo "************************"