#!/usr/bin/env python3
from flask import Flask
from flask import render_template
from hdhomerun import main as update_epg
from hdhomerun import txt_m3u, write_m3u
from os import environ

app = Flask(__name__)


@app.route("/")
def welcome():
    message = "Welcome"
    return render_template('index.html', message=message)


@app.route("/xml")
def update_xml():
    message = "Updated EPG"
    update_epg(environ["TUNER_IP"])
    return render_template('index.html', message=message)


@app.route("/m3u")
def update_m3u():
    message = "Updated M3U"
    write_m3u(txt_m3u(environ["TUNER_IP"]))
    return render_template('index.html', message=message)


@app.route("/update")
def update_all():
    update_epg(environ["TUNER_IP"])
    write_m3u(txt_m3u(environ["TUNER_IP"]))
    return render_template('index.html', message="files updated")


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
