# Dog Radio
Personal project for Raspberry Pi to play Internat radio stations via web interface. Built for Raspberry Pi 3 using Python, AngularJS and Bootstrap.

This is a work in progress. This is my first experience with the Raspberry Pi and I had little previous knowledge of Python and Linux before starting. I still have little knowledge of these things and I'm sure it shows. Still, it may prove useful for someone doing a similar project.

When leaving my dogs alone for any length of time I typically physically turn on an old clock radio for noise. This project is to replace that old radio.
## Setup
- Install mpd and for media. PIP to load Python packages
```sh
sudo apt-get install mpd mpc
sudo apt-get install python-pip
```
- Install Flask and flask_restful for HTML and RESTful API.
```sh
sudo pip install flask
sudo pip install flask-restful
```
- Install gevent server and APScheduler
```sh
sudo pip install gevent
sudo pip install apscheduler
```
## Run
- Start server
```sh
python app.py
```
- Open Interface

http://server:5000
