from flask import Flask, render_template
from flask_restful import Resource, Api
from radioApi import Control, Volume, Status, Playlist

app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():    
    return render_template('index.html')

api.add_resource(Control, '/control/<string:action>', '/control/<string:action>/<string:position>')
api.add_resource(Volume, '/volume', '/volume/<string:volume>')
api.add_resource(Status, '/status')
api.add_resource(Playlist, '/playlist')

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
