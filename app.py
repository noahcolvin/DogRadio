from flask import Flask, render_template
from flask_restful import Resource, Api
from radioApi import Control, Volume, Status, Playlist
from powerControl import Power
from settings import Settings
from gevent.wsgi import WSGIServer

#import logging
#logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():    
    return render_template('index.html')

api.add_resource(Control, '/control/<string:action>', '/control/<string:action>/<string:position>')
api.add_resource(Volume, '/volume', '/volume/<string:volume>')
api.add_resource(Status, '/status')
api.add_resource(Playlist, '/playlist')
api.add_resource(Power, '/power/<int:index>', '/power/<int:index>/<string:state>')
api.add_resource(Settings, '/setting/<string:section>/<string:name>')

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

#if __name__ == '__main__':
#    app.run(debug=True, host='0.0.0.0', port=5000)

http_server = WSGIServer(('', 5000), app)

try:
  http_server.serve_forever()
except:
  Power.cleanup()