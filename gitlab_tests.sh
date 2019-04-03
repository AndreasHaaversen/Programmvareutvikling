#!/usr/bin/env bash
# Testing script
echo "Hostname: " $(cat /etc/hostname)
echo "**********************************"
echo "******** Pip dependencies ********"
echo "**********************************"
#pip install --upgrade pip
pip install -r ./nigirifalls/requirements.txt
pip install coverage
echo "***********************************"
echo "******** Zone install step ********"
echo "***********************************"
python -V
pip freeze
echo "*************************************"
echo "******** Database setup step ********"
echo "*************************************"
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
echo "*************************************"
echo "******** Collect static step ********"
echo "*************************************"
if python3 ./nigirifalls/manage.py collectstatic; then
    printf 'OK - Static files collected\n'
else
    printf 'Failed - Could not collect static files\n'
	exit 1
fi
echo "*****************************"
echo "******** Django test ********"
echo "*****************************"
cd nigirifalls
if coverage run --source='.' manage.py test -k; then
    coverage report -m
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