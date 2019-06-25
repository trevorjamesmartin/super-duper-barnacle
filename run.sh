#!/bin/bash
if [ -z "$1" ]; then
    echo "USAGE: ./run IP.of.hdhomerun.tuner"
    echo "..."
    echo "Open a web browser to http://my.hdhomerun.com/"
    echo " find your tuner and select 'status' to reveal the IP Address";
    exit 0
fi
docker build -t tuner_xml .;docker run -dit --restart unless-stopped -p 5000:5000 -e TUNER_IP=$1 -v $PWD/www:/www tuner_xml /bin/bash
