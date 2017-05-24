#!/bin/bash
echo 'Starte Server'
source ~/venvs/flaskproj/bin/activate 
python3 /root/flaskproj/manage.py runserver
