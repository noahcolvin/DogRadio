import os
import subprocess
from flask_restful import Resource
from helpers import Parser

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
