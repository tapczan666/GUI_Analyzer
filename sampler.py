# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 21:06:13 2014

@author: maciek
"""
from PyQt4 import QtCore
from rtlsdr import RtlSdr
import Queue
import time
import numpy as np

class Sampler(QtCore.QObject):
    abortStart = QtCore.pyqtSignal()
    
    def __init__(self, gain, samp_rate, freqs, num_samples, q_in, parent=None):
        super(Sampler, self).__init__(parent)
        self.gain = gain
        self.samp_rate = samp_rate
        self.freqs = freqs
        self.num_samples = num_samples
        self.queue = q_in
        self.offset = 0
        
        self.WORKING = True
        self.BREAK = False  
        self.MEASURE = False
        
        try:
            self.sdr = RtlSdr()
            self.sdr.set_manual_gain_enabled(1)
            self.sdr.gain = self.gain
            self.sdr.sample_rate = self.samp_rate
        except IOError:            
            self.WORKING = False
            print "Failed to initiate device. Please reconnect."
        
        
        
    def sampling(self):
        print 'Starting sampler...'
        while self.WORKING:
            prev = 0
            counter = 0
            gain = self.gain
            num_samples = self.num_samples
            self.BREAK = False
            self.sdr.gain = gain
            start = time.time()
            #print self.sdr.get_gain()
            for i in range(len(self.freqs)):
                if self.BREAK:
                    break
                else:
                    center_freq = self.freqs[i]
                    #print "frequency: " + str(center_freq/1e6) + "MHz"
                    if center_freq != prev:  
                        try:
                            self.sdr.set_center_freq(center_freq)
                        except:
                            self.WORKING = False
                            print "Device failure while setting center frequency"
                            break
                        prev = center_freq
                    else:
                        pass
                    
                    #time.sleep(0.01)
                    try:
                        x = self.sdr.read_samples(2048)
                        data = self.sdr.read_samples(num_samples)
                    except:
                        self.WORKING = False
                        print "Device failure while getting samples"
                        break
                    if self.MEASURE:
                        self.offset = np.mean(data)
                    #print data
                    #self.sdr.close()
                    counter += 1
                    self.queue.put([i, center_freq, data])            
            print str(counter) + " samples in " + str(time.time()-start) + " seconds"           
        self.abortStart.emit()
        
        
    @QtCore.pyqtSlot(int)
    def changeGain(self, gain):
        self.gain = gain