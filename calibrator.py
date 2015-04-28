# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 17:10:31 2014

@author: maciek
"""
import xlrd as xl
import numpy as np

class Calibrator():
    def __init__(self):
        self.loadData()
        
    def loadData(self):
        book = xl.open_workbook('kalibracja.xls')
        
        #Skalowanie w zaleznosci od czestotliwosci
        sheet1 = book.sheet_by_index(0)
        a=np.empty(0)
        b=np.empty(0)
        for i in range(1,sheet1.nrows):
            a = np.append(a,sheet1.cell_value(i,0))
            b = np.append(b,sheet1.cell_value(i,1))
        self.scaling = [a,b]
        
        #Zysk FFT
        sheet2 = book.sheet_by_index(1)
        self.fft_gain = np.empty(0)
        for i in range(sheet2.nrows):
            self.fft_gain = np.append(self.fft_gain, sheet2.cell_value(i,1))
            
        #Charakterystyka segmentu
        sheet3 = book.sheet_by_index(2)
        self.segment_x = np.array(0)
        self.segment_y = []
        for j in range(1,sheet3.nrows):
            self.segment_x = np.append(self.segment_x,sheet3.cell_value(j,0))
        
        for i in range(1,sheet3.ncols):
            temp=np.empty(0)
            for j in range(1,sheet3.nrows):
                temp = np.append(b,sheet3.cell_value(j,i))
            self.segment_y.append(temp)
    
        
    def getCalibration(self, start, stop, rbw_index, size):
        pass