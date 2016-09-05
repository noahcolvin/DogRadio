from flask import request
from flask_restful import Resource
from configobj import ConfigObj

config = ConfigObj('settings.ini')

class Settings(Resource):
    def get(self, section, name):
        settingSection = config[section]
        value = settingSection[name]
        return value

    @staticmethod
    def set(section, name, value):
        settingSection = config[section]
        settingSection[name] = value
        config.write()