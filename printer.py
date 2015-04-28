# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 14:41:40 2014

@author: maciek
"""
from PyQt4 import QtCore
import numpy as np

class Printer(QtCore.QObject):
    dataReady = QtCore.pyqtSignal(object)
    
    def __init__(self, q_out, length, parent=None):
        super(Printer, self).__init__(parent)
        self.queue = q_out
        self.WORKING = True
        self.length = length
        self.xdata = np.empty(0)
        self.ydata = np.empty(0)
        
    
    def printing(self):
        while self.WORKING:
            try:
                item = self.queue.get()
            except:
                print "Printer error"
                self.WORKING = False
                break
            
            length = self.length
            index = int(item[0])
            power = item[1]
            freqs = item[2]
            
            if len(power) == length:
                if len(self.xdata) == 0:
                    self.xdata = freqs
                    self.ydata = power
                else:
                    self.xdata = np.concatenate((self.xdata[:index*length], freqs, self.xdata[(index+1)*length:]))
                    self.ydata = np.concatenate((self.ydata[:index*length], power, self.ydata[(index+1)*length:]))
                #print self.xdata    
                #self.ydata = np.convolve(self.ydata, np.ones(100), mode='same')
                self.queue.task_done()
                #print "Replot"
                self.dataReady.emit([self.ydata, self.xdata])
            else:
                pass