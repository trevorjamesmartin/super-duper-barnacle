#!/usr/bin/env python3
from flask import Flask
from flask import render_template
from hdhomerun import main as update_epg
from sys import argv
from os import environ

app = Flask(__name__)


@app.route("/")
def welcome():
    message = "Welcome"
    return render_template('index.html', message=message)


@app.route("/update")
def updater():
    message = "Updated EPG"
    update_epg(environ["TUNER_IP"])
    return render_template('index.html', message=message)


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
