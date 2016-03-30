from flask import Flask, render_template
from flask_restful import Resource, Api
from helpers import Parser
import os
import subprocess
import re

app = Flask(__name__)
api = Api(app)

class C(): pass

class Control(Resource):
    def post(self, action):
        os.system('sudo mpd')
        if action == 'play':
            os.system('mpc play')
        elif action == 'stop':
            os.system('mpc stop')
            return {'playMode': 'stopped'}
        elif action =='pause':
            os.system('mpc pause')
        elif action =='next':
            os.system('mpc next')
        elif action =='previous':
            os.system('mpc prev')
        else:
            return {'playMode': 'invalid'}
            
        proc = subprocess.Popen(['mpc status'], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        if err:
            return {'error', err}
        return {'status': Parser.parsePlayMode(out)}

class Volume(Resource):    
    def get(self):
        proc = subprocess.Popen(["mpc volume"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        if err:
            return {'error', err}
        return {"volume": Parser.parseVolume(out)}

    def put(self, volume):
        proc = subprocess.Popen(["mpc volume " + volume], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        if err:
            return {'error', err}
        return {"volume": Parser.parseVolume(out)}

class Status(Resource):
    def get(self):
        proc = subprocess.Popen(["mpc status"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        c = C()
        c.volume = Parser.parseVolume(out)
        c.playMode = Parser.parsePlayMode(out)
        c.title = Parser.parseTitle(out)
        return c.__dict__

@app.route('/')
def index():    
    return render_template('index.html')

@app.route('/cakes')
def cakes():
    return 'Yummy cakes!'


api.add_resource(Control, '/control/<string:action>')
api.add_resource(Volume, '/volume', '/volume/<string:volume>')
api.add_resource(Status, '/status')

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
