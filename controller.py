# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 16:49:33 2014

@author: maciek
"""
from pylibftdi import BitBangDevice

class USBController():
    def __init__(self):
        try:
            self.bb = BitBangDevice()
            self.bb.port = 0xFF
            self.state = self.bb.read_pins()
            self.attenuation = 0
            self.switch_1 = 1
            self.switch_2 = 1
            print self.state
        except:
            raise Exception("Failed to initialize USB controller")
            print "Failed to initialize USB controller. Please reconnect."
            
        
    def set_att(self, att):
        if att >=0 and att <=31:
            self.attenuation = att
            value = self.switch_1*32 + self.switch_2*64 + self.attenuation^0b11111
            self.bb.port = value
            self.state = self.bb.read_pins()
        else:
            print "Attenuation value out of range"
        
        
    def set_switches(self, a, b):
        if a in [0,1] and b in [0,1]:
            self.switch_1 = a
            self.switch_2 = b
            
            value = self.switch_1*32 + self.switch_2*64 + self.attenuation^0b11111
            self.bb.port = value
            self.state = self.bb.read_pins()
        else:
            print "Incorrent switch setting. Enter 0 or 1."