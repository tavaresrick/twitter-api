#!/bin/bash
pip install -r requirements.txt

python tweets_collector/manage.py migrate
python tweets_collector/manage.py runserver 0:8000