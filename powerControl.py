import RPi.GPIO as GPIO
import logging

from flask import request
from flask_restful import Resource
from settings import Settings

pins = [3, 5]

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pins, GPIO.OUT, initial=GPIO.HIGH)

class Power(Resource):

    def bob(self):
        settings = Settings()        
        pin3 = settings.get('power', 'pin3')
        pin5 = settings.get('power', 'pin5')
        #logging.info('power initial state pin3 = %s, pin5 = %s', pin3, pin5)
        if pin3 == 'on':
            self.post(3, pin3)
        if pin5 == 'on':
            self.post(5, pin5)

    def post(self, index, state):
        #logging.debug('power state changing for index %s state %s', index, state)
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
