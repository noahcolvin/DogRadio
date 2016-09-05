import RPi.GPIO as GPIO

from flask import request
from flask_restful import Resource
#from settings import Settings

pins = [3, 5]

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pins, GPIO.OUT, initial=GPIO.HIGH)

class Power(Resource):

    def post(self, index, state):
        pin = pins[index]
        enabled = state != 'on'
        GPIO.output(pin, enabled)
        return enabled

    def get(self, index):
        pin = pins[index]
        return GPIO.input(pin) == 0

    @staticmethod
    def cleanup():
        GPIO.cleanup()
        return
