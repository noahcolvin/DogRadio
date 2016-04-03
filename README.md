# Dog Radio
Personal project for Raspberry Pi to play Internat radio stations via web interface. Built for Raspberry Pi 3 using Python, AngularJS and Bootstrap.

This is a work in progress. This is my first experience with the Raspberry Pi and I had little previous knowledge of Python and Linux before starting. I still have little knowledge of these things and I'm sure it shows. Still, it may prove useful for someone doing a similar project.

When leaving my dogs alone for any length of time I typically physically turn on an old clock radio for noise. This project is to replace that old radio.
## Setup
- Install mpd and mpc
```sh
sudo apt-get install mpd mpc
```
- Install pip
```sh
sudo apt-get install python-pip
```
- Install Flask
```sh
sudo pip install flask
```
- install flask_restful
```sh
sudo pip install flask-restful
```
## Run
- Start server
```sh
python app.py
```
- Open Interface

http://server:5000
