import os
import subprocess
from flask import request
from flask_restful import Resource, abort
from helpers import Parser

class C(): pass

class Control(Resource):
    def post(self, action, position = ''):
        os.system('sudo mpd')
        if action == 'play':
            os.system('mpc play ' + position)
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
            return {'error', err}, 500
        return {'status': Parser.parsePlayMode(out)}

class Volume(Resource):    
    def get(self):
        proc = subprocess.Popen(["mpc volume"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        if err:
            return {'error', err}, 500
        return {"volume": Parser.parseVolume(out)}

    def put(self, volume):
        proc = subprocess.Popen(["mpc volume " + volume], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        if err:
            return {'error', err}, 500
        return {"volume": Parser.parseVolume(out)}

class Status(Resource):
    def get(self):
        proc = subprocess.Popen(["mpc status"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        if err:
            return {'error', err}, 500
        c = C()
        c.volume = Parser.parseVolume(out)
        c.playMode = Parser.parsePlayMode(out)
        c.title = Parser.parseTitle(out)
        return c.__dict__

class Playlist(Resource):
    def get(self):
        proc = subprocess.Popen(["mpc playlist"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        if err:
            return {'error', err}, 500
        items = out.split('\n')
        return [x for x in items if x]

    def post(self):
        proc = subprocess.Popen(["mpc add " + request.get_json()['url']], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        if err:
            return {'error', err}, 500
        return '', 204

    def delete(self):
        url = request.get_json()['url']
        playlist = self.get()
        try:
            index = playlist.index(url) + 1
            proc = subprocess.Popen(["mpc del " + str(index)], stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            if err:
                return {'error', err}, 500
            return '', 204
        except ValueError:
            abort(404, message='URL not found in playlist')








