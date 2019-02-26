#!/usr/bin/env bash
echo "Deploying..."
cd nigirifalls
ls -l
gem install dpl
dpl --provider=heroku --app=nigirifallsdev --api-key=$HEROKU_DEPLOY_API_KEY
#apt-get -y install apt-utils
#apt-get -y install python3-pip python3-dev python3-setuptools