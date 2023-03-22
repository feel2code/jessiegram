#!/bin/bash
echo 'Starting Django server...'
source venv/bin/activate
cd jessiegram
python3 manage.py runserver 0:8000 --insecure &
deactivate
echo 'Closing Django server...'
sleep 10