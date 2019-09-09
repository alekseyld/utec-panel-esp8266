import control
from machine import Pin
import network
import os

import esp
esp.osdebug(None)

import gc
gc.collect()

#For PC
#class Pin:
#    def __init__(self):
#        self.ons = 0
#    
#    def on(self):
#        self.ons = 1
#
#    def off(self):
#        self.ons = 0
#        
#    def value(self):
#        return self.ons


class NamedPin:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
    
    def value(self):
        return self.pin.value()

    def name(self):
        return self.name

    def on(self):
        self.pin.on()

    def off(self):
        self.pin.off()

def setupSTA(settings):
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        #print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(settings['wifi-name'], settings['wifi-pass'])
        import time
        i = time.time()
        while not sta_if.isconnected():
            #print('.', end='')
            if time.time() - i > 40:
                setupAp(settings)
                break

def setupAp(settings):
     sta_if = network.WLAN(network.STA_IF)
     sta_if.active(False)
     ap_if = network.WLAN(network.AP_IF)
     ap_if.active(True)
     ap_if.config(essid=settings['ap-name'], password=settings['ap-pass'])

def setupNetwork():     
    if not "settings.json" in os.listdir():
        open("settings.json", 'w+').close()

    settings = control.getSettings()

    if settings['mode'] == 'sta' and not settings['wifi-name'] == '' and not settings['wifi-pass'] == '':
        setupSTA(settings)
    else:
        setupAp(settings)

print('setupNetwork')
        
setupNetwork()

print('setup pins')

#Set up pins (max 9 pins)
control.namedPinsList.append(NamedPin('Компрессор', Pin(0, Pin.OUT)))
control.namedPinsList.append(NamedPin('Насос', Pin(4, Pin.OUT)))
control.namedPinsList.append(NamedPin('Вентилятор', Pin(5, Pin.OUT)))
control.namedPinsList.append(NamedPin('Пар', Pin(2, Pin.OUT)))

control.start_web()
