#!/bin/bash
echo "testing ... " + $TUNER_IP
echo "installing flask"
pip3 install Flask
cd /www
echo "pulling xml"
python3 hdhomerun.py $TUNER_IP
sleep 2
echo "starting web server"
python3 serve.py
exec "$@"
