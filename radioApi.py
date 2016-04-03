import subprocess
from flask import request
from flask_restful import Resource, abort
from helpers import Parser

class C(): pass

def runCommand(command):
    proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    return proc.communicate()

class Control(Resource):
    def post(self, action, position = ''):
        self.checkStartup()
        #runCommand('sudo mpd')
        if action == 'play':
            runCommand('mpc play ' + position)
        elif action == 'stop':
            runCommand('mpc stop')
            return {'playMode': 'stopped'}
        elif action =='pause':
            runCommand('mpc pause')
        elif action =='next':
            runCommand('mpc next')
        elif action =='previous':
            runCommand('mpc prev')
        else:
            return {'playMode': 'invalid'}

        (out, err) = runCommand('mpc status')
        if err:
            return {'error', err}, 500
        return {'status': Parser.parsePlayMode(out)}
        
    def checkStartup(self):
        s = Status()
        stat = s.get()
        if stat['playMode'] == 'stopped':
            runCommand('mpc clear')
            runCommand('mpc load dogplaylist')
        return

class Volume(Resource):    
    def get(self):        
        (out, err) = runCommand('mpc volume')
        if err:
            return {'error', err}, 500
        return {'volume': Parser.parseVolume(out)}

    def put(self, volume):
        (out, err) = runCommand('mpc volume ' + volume)
        if err:
            return {'error', err}, 500
        return {'volume': Parser.parseVolume(out)}

class Status(Resource):
    def get(self):
        (out, err) = runCommand('mpc status')
        if err:
            return {'error', err}, 500
        c = C()
        c.volume = Parser.parseVolume(out)
        c.playMode = Parser.parsePlayMode(out)
        c.title = Parser.parseTitle(out)
        return c.__dict__

class Playlist(Resource):
    def get(self):
        (out, err) = runCommand('mpc playlist')
        if err:
            return {'error', err}, 500
        items = out.split('\n')
        return [x for x in items if x]

    def post(self):        
        (out, err) = runCommand('mpc add ' + request.get_json()['url'])
        if err:
            return {'error', err}, 500
        self.savePlaylist()
        return '', 204

    def delete(self):
        url = request.get_json()['url']
        playlist = self.get()
        try:
            index = playlist.index(url) + 1            
            (out, err) = runCommand('mpc del ' + str(index))
            if err:
                return {'error', err}, 500
            self.savePlaylist()
            return '', 204
        except ValueError:
            abort(404, message='URL not found in playlist')
        
    def savePlaylist(self):
        try:
            runCommand('mpc save dogplaylist')
        finally:
            return








