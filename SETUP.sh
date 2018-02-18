#!/bin/bash

echo "Built for Ubuntu 16.x"


apt-get install git -y
apt-get install supervisor
apt-get install gunicorn
apt-get install nginx
pip install Flask
pip install statistics
pip install pygal
pip install werkzeug

# Clone Repo
git clone https://github.com/Monkeybut/Fairpool-simple-logger.git


# Add crontab for logger.py ever 15 minutes.
crontab -l > newcron
echo "*/15 * * * * /usr/bin/python3 /home/ubuntu/Fairpool-simple-logger/logger.py" >> newcron
crontab newcron
rm newcron

echo "[program:flaskdeploy]
command = /usr/bin/gunicorn web_ui:app -w 4
directory = /home/ubuntu/Fairpool-simple-logger/
user = ubuntu
stdout_logfile = /var/log/flaskdeploy.err.log
stderr_logfile = /var/log/flaskdeploy.out.log
redirect_stderr = True
environment = PRODUCTION=1" > /etc/supervisor/conf.d/flaskdeploy.conf 

echo "Please setup nginx config yourself as a proxy. This should start app on port 8000.
Nginx should be used as a front end proxy. Especially if public facing in which case also 
use letsencrypt

I should also recommend using a virtual environment to run this."
wait