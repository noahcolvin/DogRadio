import subprocess
from flask import request
from flask_restful import Resource, abort
from helpers import Parser
from settings import Settings

import logging
logging.basicConfig()
from apscheduler.schedulers.background import BackgroundScheduler

class C(): pass

scheduler = None

def runCommand(command):
    proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    return proc.communicate()

class Control(Resource):

    def bob(self):
        settings = Settings()
        state = settings.get('radio', 'state')
        #logging.info('initial state = ' + state)
        self.post(state)

    def post(self, action, position = ''):
        global scheduler
        self.checkStartup()

        #logging.debug('posting ' + action + ' position = ' + position)
        
        if action == 'play':
            runCommand('mpc play ' + position)
            Settings.set('radio', 'state', 'play')
            
            if scheduler is None:
                scheduler = BackgroundScheduler()
                scheduler.add_job(self.checkStatus, 'interval', seconds=30, id='checkStatus', replace_existing=True)
                scheduler.start()
        elif action == 'stop':
            runCommand('mpc stop')
            Settings.set('radio', 'state', 'stop')
            
            if scheduler is not None:
                scheduler.remove_job('checkStatus')
                scheduler.shutdown()
                scheduler = None
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
        return {'playMode': Parser.parsePlayMode(out)}
        
    def checkStartup(self):
        s = Status()
        stat = s.get()
        if stat['playMode'] == 'stopped':
            runCommand('mpc clear')
            runCommand('mpc load dogplaylist')
        return
    
    def checkStatus(self):
        s = Status()
        stat = s.get()
        if stat['playMode'] == 'stopped':
            self.post('play')
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
            runCommand('mpc rm dogplaylist')
            runCommand('mpc save dogplaylist')
        finally:
            return








