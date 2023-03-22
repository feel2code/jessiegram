#!/bin/bash
echo 'Starting Django server...'
apt install nginx -y
ufw allow 'Nginx Full'
ufw allow OpenSSH
source venv/bin/activate
cd jessiegram
cat misc/default > /etc/nginx/sites-enabled/default
cat misc/gunicorn.service > /etc/systemd/system/gunicorn.service
cat misc/nginx.conf > /etc/nginx/nginx.conf
systemctl start gunicorn
systemctl enable gunicorn
systemctl restart gunicorn
python jessiegram/manage.py collectstatic --no-input
systemctl start nginx
systemctl reload nginx