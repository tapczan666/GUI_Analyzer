# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 18:45:43 2014

@author: maciek
"""
import sys
from PyQt4 import QtCore, QtGui
from PyQt4.Qwt5 import QwtText, QwtScaleDiv
import Queue
from gui_ui import Ui_MainWindow#, WaterfallData
from sampler import Sampler
from worker import Worker
from printer import Printer
from controller import USBController
import numpy as np  
from scipy import signal
import time

app = QtGui.QApplication(sys.argv)

class Analyzer(QtGui.QMainWindow):
    num_threads = 10   
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        #QtCore.QThread.currentThread().setPriority(QtCore.QThread.HighPriority)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.q_in = Queue.Queue(maxsize=1000)
        self.q_out = Queue.Queue(maxsize=1000)
        
        self.startFreq = 130e6
        self.stopFreq = 140e6
        self.span = self.stopFreq - self.startFreq
        self.center = self.startFreq + self.span/2
        
        self.gain = 0
        self.samp_rate = 2.4e6
        self.nfft = self.ui.rbwEdit.itemData(self.ui.rbwEdit.currentIndex()).toInt()
        self.num_samples = self.nfft*2
        self.step = 1.8e6
        self.FFT = True
        self.HOLD = False
        self.PEAK = False
        self.CORRECT = False
        self.AVERAGE = False
        self.SAVE = [False, False, False]
        self.saved = [False, False, False]
        self.MARKERS = [False, False, False, False]
        self.DELTA = False
        self.delta_index = None
        self.delta_value = 0
        self.marker_index = [None, None, None, None]
        self.marker_value = [0, 0, 0, 0]
        self.DIF_MARKER = False
        self.correction = 0
        self.max_hold = []
        self.peak_search = ()
        self.avg = []
        self.avg_counter = 0
        self.num_avg = 1
        self.ref = 80
        self.length = 2048
        self.slice_length = int(np.floor(self.length*(self.step/self.samp_rate)))
        print "Slice: " + str(self.slice_length)
        
        
        
        self.getFreqs()    
        
        #self.waterfallData = WaterfallData(100)        
        
        self.setupSampler()
        self.setupWorkers()
        self.setupPrinter()
        
        self.ui.refEdit.setValue(self.ref)
        self.ui.gainDisp.display(20)
        
        self.ui.startEdit.valueChanged.connect(self.onStart)
        self.ui.stopEdit.valueChanged.connect(self.onStop)
        self.ui.rbwEdit.activated[int].connect(self.onRbw)
        self.ui.centerEdit.valueChanged.connect(self.onCenter)
        self.ui.spanEdit.valueChanged.connect(self.onSpan)
        self.ui.refEdit.valueChanged.connect(self.onRef)
        #self.ui.offsetButton.clicked.connect(self.onOffset)
        self.ui.correctButton.clicked.connect(self.onCorrect)
        self.ui.holdCheck.stateChanged.connect(self.onHold)
        self.ui.peakCheck.stateChanged.connect(self.onPeak)
        self.ui.avgCheck.stateChanged.connect(self.onAvg)
        self.ui.traceButton.clicked.connect(self.onSave_1)
        self.ui.traceButton_2.clicked.connect(self.onSave_2)
        self.ui.traceButton_3.clicked.connect(self.onSave_3)
        self.ui.markerCheck.stateChanged.connect(self.onMarker_1)
        self.ui.markerCheck_2.stateChanged.connect(self.onMarker_2)
        self.ui.markerCheck_3.stateChanged.connect(self.onMarker_3)
        self.ui.markerCheck_4.stateChanged.connect(self.onMarker_4)
        self.ui.markerEdit.valueChanged.connect(self.onMarkerEdit_1)
        self.ui.markerEdit_2.valueChanged.connect(self.onMarkerEdit_2)
        self.ui.markerEdit_3.valueChanged.connect(self.onMarkerEdit_3)
        self.ui.markerEdit_4.valueChanged.connect(self.onMarkerEdit_4)
        self.ui.deltaCheck.stateChanged.connect(self.onDelta)
        self.ui.deltaEdit.valueChanged.connect(self.onDeltaEdit)
        '''
        try:
            self.usb = USBController()     
        except:
            print "Failed to initialize USB controller. Please reconnect."
            self.close()
        '''
        self.getOffset()        
        
    def setupSampler(self):
        self.samplerThread = QtCore.QThread(self)
        self.sampler = Sampler(self.gain, self.samp_rate, self.freqs, self.num_samples, self.q_in)
        self.sampler.moveToThread(self.samplerThread)
        self.samplerThread.started.connect(self.sampler.sampling)
        self.sampler.abortStart.connect(self.onAbort)
        self.ui.gainSlider.valueChanged[int].connect(self.setGain)
        #self.ui.gainSlider.valueChanged[int].connect(self.sampler.changeGain, QtCore.Qt.QueuedConnection)
        self.samplerThread.start(QtCore.QThread.NormalPriority)
        
    def setupPrinter(self):
        self.printerThread = QtCore.QThread(self)
        self.printer = Printer(self.q_out, self.slice_length)
        self.printer.moveToThread(self.printerThread)
        self.printerThread.started.connect(self.printer.printing)
        self.printer.dataReady.connect(self.plotUpdate)
        self.printerThread.start(QtCore.QThread.NormalPriority)
        
    def setupWorkers(self):
        self.threads = []
        self.workers = []
        for i in range(self.num_threads):
            print 'Starting worker #' + str(i+1) + '...'
            self.threads.append(QtCore.QThread(self))
            self.workers.append(Worker(self.q_in, self.q_out, self.nfft, self.length, self.slice_length, self.samp_rate, i))
            self.workers[i].moveToThread(self.threads[i])
            self.threads[i].started.connect(self.workers[i].working)
            self.workers[i].abort.connect(self.onAbort)
            self.threads[i].start(QtCore.QThread.NormalPriority)
            
    def getFreqs(self):
        self.freqs = np.arange(self.startFreq+self.step/2, self.stopFreq+self.step/2, self.step)
        self.ui.plot.setAxisScale(self.ui.plot.xBottom, self.startFreq/1e6, self.stopFreq/1e6)        
        self.ui.startEdit.setValue(self.startFreq/1e6)
        self.ui.stopEdit.setValue(self.stopFreq/1e6)
        self.ui.centerEdit.setValue(self.center/1e6)
        self.ui.spanEdit.setValue(self.span/1e6)    
        self.ui.centerEdit.setSingleStep(self.span/1e6)
        
    def updateFreqs(self):
        self.getFreqs()
        self.sampler.freqs = self.freqs
        self.printer.xdata = []
        self.printer.ydata = []
        self.sampler.BREAK = True
        self.max_hold = []
        self.avg = []
        self.marker_index = [None, None, None, None]
        self.delta_index = None
        
        with self.q_in.mutex:
            self.q_in.queue.clear()
        with self.q_out.mutex:
            self.q_out.queue.clear()
        
        self.ui.plot.setAxisScale(self.ui.plot.xBottom, self.startFreq/1e6, self.stopFreq/1e6)
        self.ui.centerEdit.setSingleStep(self.span/1e6)
        
    def updateRbw(self):
        self.marker_index = [None, None, None, None]
        self.delta_index = None
        if self.nfft < 200:
            self.num_samples = 256
        else:
            self.num_samples = self.nfft*2
            
        if self.span >=50e6:
            threshold = 200
        elif self.span >= 20e6: 
            threshold = 500
        else:
            threshold = 1000
            
        if self.nfft < threshold:
            self.length = 1024
            self.slice_length = int(np.floor(self.length*(self.step/self.samp_rate)))        
        else:
            self.length = self.nfft
            self.slice_length = int(np.floor(self.length*(self.step/self.samp_rate)))
        

    @QtCore.pyqtSlot(object)
    def plotUpdate(self, data):
        ydata = data[0].tolist()
        xdata = data[1].tolist()
        
        if self.HOLD:
            if len(ydata) != self.slice_length*len(self.freqs):
                pass
            else:
                if len(self.max_hold) < len(data[0]):
                    self.max_hold = data[0]
                else:
                    dif = data[0] - self.max_hold
                    dif = dif.clip(0)
                    self.max_hold += dif
                self.ui.hold_curve.setData(xdata, self.max_hold.tolist())
            
        if self.AVERAGE:
            if len(ydata) != self.slice_length*len(self.freqs):
                pass
            else:
                if self.avg_counter == 0:
                    if len(self.avg)<self.num_avg:
                        self.avg.append(data[0])
                    else:
                        self.avg = self.avg[1:]
                        self.avg.append(data[0])
                    self.avg_counter = len(self.freqs)
                else:
                    self.avg_counter -= 1
                temp = np.sum(self.avg, 0)
                temp = temp/len(self.avg)
                ydata = temp
                
        if self.PEAK:
            index = np.argmax(data[0])
            self.peak_search = (xdata[index], ydata[index])
            self.ui.peak_marker.setValue(self.peak_search[0], self.peak_search[1])
            self.ui.peak_marker.setLabel(QwtText("Peak:\n%.2f MHz, %.2f dBm" % self.peak_search))
            
        for i in range(len(self.SAVE)):
            if self.SAVE[i]:
                if self.saved[i]:
                    self.ui.saved_curves[i].detach()
                    self.saved[i] = False
                    self.ui.traces[i].setDown(False)
                else:
                    self.ui.saved_curves[i].setData(xdata, ydata)
                    self.ui.saved_curves[i].attach(self.ui.plot)
                    self.saved[i] = True
                self.SAVE[i] = False
            
        for i in range(len(self.MARKERS)):
            if self.MARKERS[i]:
                if len(ydata) != self.slice_length*len(self.freqs):
                    pass
                else:
                    self.ui.markers[i].attach(self.ui.plot)
                    if self.marker_index[i] == None:
                        value = self.marker_value[i]
                        index = np.argmin(np.abs(data[1]-value))
                        self.marker_index[i] = index
                    self.ui.markers[i].setValue(xdata[self.marker_index[i]], ydata[self.marker_index[i]])
                    self.ui.markers[i].setLabel(QwtText("Mk%i\n%.2fdBm" % (i+1, ydata[self.marker_index[i]])))                
                    
        if self.DELTA:
            if len(ydata) != self.slice_length*len(self.freqs):
                pass
            else:
                self.ui.delta_marker.attach(self.ui.plot)
                if self.delta_index == None:
                    value = self.delta_value
                    index = np.argmin(np.abs(data[1]-value))
                    self.delta_index = index
                self.ui.delta_marker.setValue(xdata[self.delta_index], ydata[self.delta_index])
                temp_x = xdata[self.delta_index] - xdata[self.marker_index[0]]
                temp_y = ydata[self.delta_index] - ydata[self.marker_index[0]]
                self.ui.delta_marker.setLabel(QwtText("Delta\n%.2fMHz, %.2fdB" % (temp_x, temp_y)))
                    
        while self.CORRECT > 0:
            
            correction = np.reshape(data[0], (-1,self.slice_length))
            correction = np.sum(correction, 0)/len(correction)
            self.correction += correction
            self.CORRECT -= 1
            if self.CORRECT == 0:
                self.correction = self.correction/10000
                self.correction -= max(self.correction)
                print max(self.correction)
                #self.correction = self.correction[:100]+np.zeros(self.slice_length-200)+self.correction[-100:]
                self.correction -= np.mean(self.correction)                
                for i in range(self.num_threads):
                    self.workers[i].correction = self.correction
                print "New correction vector applied"
                
        #print len(ydata)
        self.ui.curve.setData(xdata, ydata)
        self.ui.plot.replot() 
        
    @QtCore.pyqtSlot(float)
    def setGain(self,gain):
        self.gain = gain
        self.sampler.gain = gain
       
    @QtCore.pyqtSlot(float)
    def onStart(self,start):
        if start*1e6 < self.stopFreq:
            self.startFreq = start*1e6
            self.span = self.stopFreq - self.startFreq
            self.center = self.startFreq + self.span/2
            self.updateFreqs()
        else:
            self.startFreq = start*1e6
            self.stopFreq = self.startFreq + self.step
            self.span = self.stopFreq - self.startFreq
            self.center = self.startFreq + self.span/2
            self.updateFreqs()
    
    @QtCore.pyqtSlot(float)   
    def onStop(self,stop):
        if stop*1e6 > self.startFreq:
            self.stopFreq = stop*1e6
            self.span = self.stopFreq - self.startFreq
            self.center = self.startFreq + self.span/2
            self.updateFreqs()
        else:
            self.stopFreq = stop*1e6
            self.startFreq = self.stopFreq - self.step
            self.span = self.stopFreq - self.startFreq
            self.center = self.startFreq + self.span/2
            self.updateFreqs()
            
    @QtCore.pyqtSlot(int)
    def onRbw(self,index):
        self.nfft = self.ui.rbwEdit.itemData(index).toInt()[0]
        self.updateRbw()
        self.sampler.num_samples = self.num_samples
        self.printer.length = self.slice_length
        self.updateFreqs()
        
        for i in range(self.num_threads):
            self.workers[i].nfft = self.nfft   
            self.workers[i].length = self.length
            self.workers[i].slice_length = self.slice_length
            self.workers[i].correction = 0
            
    @QtCore.pyqtSlot(float)   
    def onCenter(self,center):
        self.center = center*1e6
        self.startFreq = self.center - self.span/2
        self.stopFreq = self.center + self.span/2
        self.updateFreqs()
        
    @QtCore.pyqtSlot(float)   
    def onSpan(self,span):
        self.span = span*1e6
        self.startFreq = self.center - self.span/2
        self.stopFreq = self.center + self.span/2
        self.updateFreqs()
        
        
    @QtCore.pyqtSlot(int)
    def onRef(self, ref):
        self.ref = ref
        self.ui.plot.setAxisScale(self.ui.plot.yLeft, ref-100, ref)
        self.ui.scaleColors(self.ref)
                
    def getOffset(self):
        self.sampler.MEASURE = True
        time.sleep(0.5)
        self.sampler.MEASURE = False
        self.offset = self.sampler.offset
        print "New offset: " + str(self.offset)
        for i in range(self.num_threads):
                self.workers[i].offset = self.offset  
                
    @QtCore.pyqtSlot()          
    def onSave_1(self):
        self.SAVE[0] = True
        self.ui.traceButton.setDown(True)
        
    @QtCore.pyqtSlot()          
    def onSave_2(self):
        self.SAVE[1] = True
        self.ui.traceButton_2.setDown(True)
        
    @QtCore.pyqtSlot()          
    def onSave_3(self):
        self.SAVE[2] = True
        self.ui.traceButton_3.setDown(True)
        
    @QtCore.pyqtSlot(int)          
    def onMarker_1(self, state):
        if state == 2:
            self.MARKERS[0] = True
            self.ui.deltaCheck.setEnabled(True)
            self.ui.markerEdit.setEnabled(True)
            self.ui.markerEdit.setRange(self.startFreq/1e6, self.stopFreq/1e6)
            self.ui.markerEdit.setValue(self.center/1e6)
        elif state == 0:
            self.MARKERS[0] = False
            self.ui.markerEdit.setDisabled(True)
            self.ui.marker_1.detach()
            self.ui.delta_marker.detach()
            self.ui.deltaCheck.setDisabled(True)
            
    @QtCore.pyqtSlot(float)
    def onMarkerEdit_1(self, freq):
        self.marker_index[0] = None
        self.marker_value[0] = freq
        
    @QtCore.pyqtSlot(int)          
    def onMarker_2(self, state):
        if state == 2:
            self.MARKERS[1] = True
            self.ui.markerEdit_2.setEnabled(True)
            self.ui.markerEdit_2.setRange(self.startFreq/1e6, self.stopFreq/1e6)
            self.ui.markerEdit_2.setValue(self.center/1e6)
        elif state == 0:
            self.MARKERS[1] = False
            self.ui.markerEdit_2.setDisabled(True)
            self.ui.marker_2.detach()
        
    @QtCore.pyqtSlot(float)
    def onMarkerEdit_2(self, freq):
        self.marker_index[1] = None
        self.marker_value[1] = freq
        
    @QtCore.pyqtSlot(int)          
    def onMarker_3(self, state):
        if state == 2:
            self.MARKERS[2] = True
            self.ui.markerEdit_3.setEnabled(True)
            self.ui.markerEdit_3.setRange(self.startFreq/1e6, self.stopFreq/1e6)
            self.ui.markerEdit_3.setValue(self.center/1e6)
        elif state == 0:
            self.MARKERS[2] = False
            self.ui.markerEdit_3.setDisabled(True)
            self.ui.marker_3.detach()
        
    @QtCore.pyqtSlot(float)
    def onMarkerEdit_3(self, freq):
        self.marker_index[2] = None
        self.marker_value[2] = freq
        
    @QtCore.pyqtSlot(int)          
    def onMarker_4(self, state):
        if state == 2:
            self.MARKERS[3] = True
            self.ui.markerEdit_4.setEnabled(True)
            self.ui.markerEdit_4.setRange(self.startFreq/1e6, self.stopFreq/1e6)
            self.ui.markerEdit_4.setValue(self.center/1e6)
        elif state == 0:
            self.MARKERS[3] = False
            self.ui.markerEdit_4.setDisabled(True)
            self.ui.marker_4.detach()
        
    @QtCore.pyqtSlot(float)
    def onMarkerEdit_4(self, freq):
        self.marker_index[3] = None
        self.marker_value[3] = freq
        
    @QtCore.pyqtSlot(int)          
    def onDelta(self, state):
        if state == 2:
            self.DELTA = True
            self.ui.deltaEdit.setEnabled(True)
            self.ui.deltaEdit.setRange(self.startFreq/1e6, self.stopFreq/1e6)
            self.ui.deltaEdit.setValue(self.center/1e6)
        elif state == 0:
            self.DELTA = False
            self.ui.deltaEdit.setDisabled(True)
            self.ui.delta_marker.detach()
        
    @QtCore.pyqtSlot(float)
    def onDeltaEdit(self, freq):
        self.delta_index = None
        self.delta_value = freq
    
    @QtCore.pyqtSlot(int)            
    def onHold(self, state):
        if state == 2:
            self.HOLD = True
            self.ui.hold_curve.attach(self.ui.plot)
        elif state == 0:
            self.HOLD = False
            self.ui.hold_curve.detach()
            self.max_hold = []
            
    @QtCore.pyqtSlot(int)            
    def onAvg(self, state):
        if state == 2:
            self.AVERAGE = True
            self.num_avg = self.ui.avgEdit.value()
        elif state == 0:
            self.AVERAGE = False
            self.num_avg = 1
            self.avg = []
            
    @QtCore.pyqtSlot(int)            
    def onPeak(self, state):
        if state == 2:
            self.PEAK = True
            self.ui.peak_marker.attach(self.ui.plot)
        elif state == 0:
            self.PEAK = False
            self.ui.peak_marker.detach()
            self.peak_search = ()
            
    def onCorrect(self):
        self.correction = 0
        self.CORRECT = 10000
        
    @QtCore.pyqtSlot()
    def onAbort(self):
        print "Aborting..."
        self.close()
    
    def closeEvent(self, event):
        print "Closing..."  
        
        while self.samplerThread.isRunning():
            self.sampler.BREAK = True
            time.sleep(0.1)
            self.sampler.WORKING = False  
            time.sleep(0.1)
            #self.sampler.sdr.close()
            self.q_in.join()
            self.samplerThread.quit()
            
        
        #self.q_out.join()    
        print "dupa2"
        if self.printerThread.isRunning():
            self.printer.WORKING = False
            self.printerThread.quit()
            
        print 'dupa'
        for i in range(self.num_threads):
            if self.threads[i].isRunning():
                self.threads[i].quit()
        
        
            
        #self.q_out.join()    
        with self.q_out.mutex:
            self.q_out.queue.clear()
        print "dupa3"
        
            
        '''with self.q_in.mutex:
            self.q_in.queue.clear()
            
        with self.q_out.mutex:
            self.q_out.queue.clear() '''           
        
        #app.quit()
     
if __name__ == "__main__":
    analyzer = Analyzer()
    analyzer.show()
    sys.exit(app.exec_())