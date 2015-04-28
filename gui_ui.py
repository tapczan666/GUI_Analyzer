# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created: Sat May 10 15:41:26 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui, Qt
import numpy as np

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(847, 480)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        
        #Tworzenie zakładek
        self.tabs = QtGui.QTabWidget(self.centralwidget)        
        
        #Główny wykre
        self.plot = QwtPlot(self.centralwidget)
        self.plot.setObjectName(_fromUtf8("plot"))
        self.plot.setAxisScale(self.plot.yLeft, -20, 80)
        self.plot.setAutoFillBackground(True)
        #self.plot.setPalette(Qt.Qt.black)
        self.plot.setCanvasBackground(Qt.Qt.black)
        
        self.grid = QwtPlotGrid()
        '''self.Yscale = QwtScaleDiv()
        self.Yscale.setInterval(10)
        self.Xscale = QwtScaleDiv()
        self.Xscale.setInterval(10)
        self.grid.setYDiv(self.YScale)
        self.grid.setXDiv(self.Xscale)'''
        self.grid.setMajPen(Qt.Qt.gray)
        self.grid.attach(self.plot)
        
        self.tabs.addTab(self.plot, "Spectrum")
       
        self.curve = QwtPlotCurve('')
        self.curve.setPen(Qt.Qt.yellow)
        self.curve.attach(self.plot)
        
        self.hold_curve = QwtPlotCurve('')
        self.hold_curve.setPen(Qt.Qt.red)
        
        self.peak_marker = QwtPlotMarker()
        self.symbol = QwtSymbol(QwtSymbol.DTriangle, QtGui.QBrush(Qt.Qt.red), QtGui.QPen(Qt.Qt.red), QtCore.QSize(10,10))
        self.peak_marker.setSymbol(self.symbol)
        self.peak_marker.setLabelAlignment(Qt.Qt.AlignTop)
        
        self.sybmol_2 = QwtSymbol(QwtSymbol.DTriangle, QtGui.QBrush(Qt.Qt.red), QtGui.QPen(Qt.Qt.white), QtCore.QSize(10,10))
        self.marker_1 = QwtPlotMarker()
        self.marker_1.setSymbol(self.sybmol_2)
        self.marker_1.setLabelAlignment(Qt.Qt.AlignTop)
        self.marker_2 = QwtPlotMarker()
        self.marker_2.setSymbol(self.sybmol_2)
        self.marker_2.setLabelAlignment(Qt.Qt.AlignTop)
        self.marker_3 = QwtPlotMarker()
        self.marker_3.setSymbol(self.sybmol_2)
        self.marker_3.setLabelAlignment(Qt.Qt.AlignTop)
        self.marker_4 = QwtPlotMarker()
        self.marker_4.setSymbol(self.sybmol_2)
        self.marker_4.setLabelAlignment(Qt.Qt.AlignTop)
        self.delta_marker = QwtPlotMarker()
        self.delta_marker.setSymbol(self.sybmol_2)
        self.delta_marker.setLabelAlignment(Qt.Qt.AlignTop)
        
        self.markers = [self.marker_1, self.marker_2, self.marker_3, self.marker_4]
        
        self.save_curve_1 = QwtPlotCurve('')
        self.save_curve_1.setPen(Qt.Qt.green)
        self.save_curve_2 = QwtPlotCurve('')
        self.save_curve_2.setPen(Qt.Qt.cyan)
        self.save_curve_3 = QwtPlotCurve('')
        self.save_curve_3.setPen(Qt.Qt.magenta)
        self.saved_curves = [self.save_curve_1, self.save_curve_2, self.save_curve_3]
        
        #Wykres waterfall
        '''self.plot_2 = QwtPlot(self.centralwidget)
        self.plot_2.setObjectName(_fromUtf8("plot_2"))
        
        self.waterfall = QwtPlotSpectrogram()
        self.waterfall.attach(self.plot_2)
        
        self.colorMap = QwtLinearColorMap(Qt.Qt.darkCyan, Qt.Qt.red)
        self.scaleColors(80)
        self.waterfall.setColorMap(self.colorMap)
        #self.waterfallData = QwtRasterData()
        #self.tabs.addTab(self.plot_2, "Waterfall")'''
        
        self.verticalLayout.addWidget(self.tabs)
        
        self.picker = QwtPlotPicker(QwtPlot.xBottom, 
                                    QwtPlot.yLeft, 
                                    QwtPicker.PointSelection | QwtPicker.DragSelection,
                                    QwtPlotPicker.CrossRubberBand,
                                    QwtPicker.AlwaysOn,
                                    self.plot.canvas())
        self.picker.setTrackerPen(Qt.Qt.white)
        self.picker.setRubberBandPen(Qt.Qt.gray)
        
        self.freqBox = QtGui.QGroupBox(self.centralwidget)
        self.freqBox.setObjectName(_fromUtf8("freqBox"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.freqBox)
        
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        
        self.formLayout_3 = QtGui.QFormLayout()
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.label = QtGui.QLabel(self.freqBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        
        self.startEdit = QtGui.QDoubleSpinBox(self.freqBox)
        self.startEdit.setObjectName(_fromUtf8("startEdit"))
        self.startEdit.setDecimals(2)
        self.startEdit.setRange(1, 1280)
        self.startEdit.setKeyboardTracking(False)         
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.startEdit)
        self.horizontalLayout.addLayout(self.formLayout_3)
        
        self.formLayout_4 = QtGui.QFormLayout()
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.label_2 = QtGui.QLabel(self.freqBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        
        self.stopEdit = QtGui.QDoubleSpinBox(self.freqBox)
        self.stopEdit.setObjectName(_fromUtf8("stopEdit"))
        self.stopEdit.setDecimals(2)
        self.stopEdit.setRange(1, 1280)
        self.stopEdit.setKeyboardTracking(False)
        
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.FieldRole, self.stopEdit)
        self.horizontalLayout.addLayout(self.formLayout_4)
        self.formLayout_5 = QtGui.QFormLayout()
        self.formLayout_5.setObjectName(_fromUtf8("formLayout_5"))
        self.label_3 = QtGui.QLabel(self.freqBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_5.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        
        self.rbwEdit = QtGui.QComboBox(self.freqBox)
        self.rbwEdit.setObjectName(_fromUtf8("rbwEdit"))
        self.rbwEdit.addItem('0,21 kHz', 16384)
        self.rbwEdit.addItem('0,42 kHz', 8192)
        self.rbwEdit.addItem('0,84 kHz', 4096)
        self.rbwEdit.addItem('1,69 kHz', 2048)
        self.rbwEdit.addItem('3,38 kHz', 1024)
        self.rbwEdit.addItem('6,75 kHz', 512)
        self.rbwEdit.addItem('13,5 kHz', 256)
        self.rbwEdit.addItem('27 kHz', 128)
        self.rbwEdit.addItem('54 kHz', 64)
        self.rbwEdit.addItem('108 kHz', 32)
        self.rbwEdit.addItem('216 kHz', 16)
        self.rbwEdit.addItem('432 kHz', 8)
        self.rbwEdit.setCurrentIndex(4)
        
        
        self.formLayout_5.setWidget(0, QtGui.QFormLayout.FieldRole, self.rbwEdit)
        self.horizontalLayout.addLayout(self.formLayout_5)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.formLayout_7 = QtGui.QFormLayout()
        self.formLayout_7.setObjectName(_fromUtf8("formLayout_7"))
        self.centerLabel = QtGui.QLabel(self.freqBox)
        self.centerLabel.setObjectName(_fromUtf8("centerLabel"))
        self.formLayout_7.setWidget(0, QtGui.QFormLayout.LabelRole, self.centerLabel)
        
        self.centerEdit = QtGui.QDoubleSpinBox(self.freqBox)
        self.centerEdit.setObjectName(_fromUtf8("centerEdit"))
        self.centerEdit.setDecimals(2)
        self.centerEdit.setRange(1, 1280)
        self.centerEdit.setKeyboardTracking(False)         
        self.formLayout_7.setWidget(0, QtGui.QFormLayout.FieldRole, self.centerEdit)
        self.horizontalLayout_3.addLayout(self.formLayout_7)
        
        self.formLayout_8 = QtGui.QFormLayout()
        self.formLayout_8.setObjectName(_fromUtf8("formLayout_8"))
        self.spanLabel = QtGui.QLabel(self.freqBox)
        self.spanLabel.setObjectName(_fromUtf8("spanLabel"))
        self.formLayout_8.setWidget(0, QtGui.QFormLayout.LabelRole, self.spanLabel)
        
        self.spanEdit = QtGui.QDoubleSpinBox(self.freqBox)
        self.spanEdit.setObjectName(_fromUtf8("spanEdit"))
        self.spanEdit.setDecimals(2)
        self.spanEdit.setRange(0.1, 1280)
        self.spanEdit.setKeyboardTracking(False)         
        self.formLayout_8.setWidget(0, QtGui.QFormLayout.FieldRole, self.spanEdit)
        self.horizontalLayout_3.addLayout(self.formLayout_8)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        
        self.verticalLayout.addWidget(self.freqBox)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        
        self.settingsBox = QtGui.QGroupBox(self.centralwidget)
        self.settingsBox.setMaximumSize(QtCore.QSize(250, 16777215))
        self.settingsBox.setObjectName(_fromUtf8("settingsBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.settingsBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.gainLabel = QtGui.QLabel(self.settingsBox)
        self.gainLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.gainLabel.setObjectName(_fromUtf8("gainLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.gainLabel)
        self.gainSlider = QtGui.QSlider(self.settingsBox)
        self.gainSlider.setMaximum(49)
        self.gainSlider.setSingleStep(1)
        self.gainSlider.setProperty("value", 20)
        self.gainSlider.setOrientation(QtCore.Qt.Horizontal)
        self.gainSlider.setObjectName(_fromUtf8("gainSlider"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.gainSlider)
        self.verticalLayout_2.addLayout(self.formLayout)
        
        self.gainDisp = QtGui.QLCDNumber(self.settingsBox)
        self.gainDisp.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.verticalLayout_2.addWidget(self.gainDisp)
        
        '''self.offsetButton = QtGui.QPushButton(self.settingsBox)
        self.offsetButton.setText("Remove DC offset")
        self.verticalLayout_2.addWidget(self.offsetButton)  ''' 
        
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.refLabel = QtGui.QLabel(self.settingsBox)
        self.refLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.refLabel.setObjectName(_fromUtf8("refLabel"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.refLabel)        
        self.refEdit = QtGui.QDoubleSpinBox(self.settingsBox)
        self.refEdit.setObjectName(_fromUtf8("refEdit"))
        self.refEdit.setDecimals(0)
        self.refEdit.setKeyboardTracking(False)
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.refEdit)
        self.verticalLayout_2.addLayout(self.formLayout_2) 
        
        spacerItem1 = QtGui.QSpacerItem(158, 304, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        
        
        #Settings tabs
        self.settings_tabs = QtGui.QTabWidget(self.settingsBox) 
        self.verticalLayout_2.addWidget(self.settings_tabs)
        
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.saveButton = QtGui.QPushButton(self.settingsBox)
        self.saveButton.setText("Save plot")
        self.verticalLayout_4.addWidget(self.saveButton)          
        
        self.formLayout_9 = QtGui.QFormLayout()
        self.formLayout_9.setObjectName(_fromUtf8("formLayout_9"))
        self.avgLabel = QtGui.QLabel(self.settingsBox)
        self.avgLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.avgLabel.setObjectName(_fromUtf8("avgLabel"))
        self.formLayout_9.setWidget(0, QtGui.QFormLayout.LabelRole, self.avgLabel)  
        self.avgCheck = QtGui.QCheckBox(self.settingsBox) 
        self.formLayout_9.setWidget(0, QtGui.QFormLayout.FieldRole, self.avgCheck)
        self.verticalLayout_4.addLayout(self.formLayout_9)
        
        self.formLayout_10 = QtGui.QFormLayout()
        self.avgLabel_2 = QtGui.QLabel(self.settingsBox)
        self.avgLabel_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.avgLabel_2.setObjectName(_fromUtf8("avgLabel_2"))
        self.formLayout_10.setWidget(0, QtGui.QFormLayout.LabelRole, self.avgLabel_2) 
        self.avgEdit = QtGui.QDoubleSpinBox(self.settingsBox)
        self.avgEdit.setDecimals(0)
        self.avgEdit.setRange(1, 100)
        self.avgEdit.setKeyboardTracking(False)
        self.avgEdit.setValue(10)
        self.formLayout_10.setWidget(0, QtGui.QFormLayout.FieldRole, self.avgEdit)
        self.verticalLayout_4.addLayout(self.formLayout_10)
         
        self.formLayout_6 = QtGui.QFormLayout()
        self.formLayout_6.setObjectName(_fromUtf8("formLayout_6"))
        self.holdLabel = QtGui.QLabel(self.settingsBox)
        self.holdLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.holdLabel.setObjectName(_fromUtf8("holdLabel"))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.LabelRole, self.holdLabel)                   
        self.holdCheck = QtGui.QCheckBox(self.settingsBox)  
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.FieldRole, self.holdCheck)
        self.verticalLayout_4.addLayout(self.formLayout_6) 
        
        self.formLayout_11 = QtGui.QFormLayout()
        self.formLayout_11.setObjectName(_fromUtf8("formLayout_11"))
        self.peakLabel = QtGui.QLabel(self.settingsBox)
        self.peakLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.peakLabel.setObjectName(_fromUtf8("peakLabel"))
        self.formLayout_11.setWidget(0, QtGui.QFormLayout.LabelRole, self.peakLabel)                   
        self.peakCheck = QtGui.QCheckBox(self.settingsBox)  
        self.formLayout_11.setWidget(0, QtGui.QFormLayout.FieldRole, self.peakCheck)
        self.verticalLayout_4.addLayout(self.formLayout_11)
        
        self.peakStatus = QtGui.QLabel("Peak: ")        
        
        self.correctButton = QtGui.QPushButton(self.settingsBox)
        self.correctButton.setText("Correction")
        self.verticalLayout_4.addWidget(self.correctButton)
        
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.traceButton = QtGui.QPushButton(self.settingsBox)
        self.traceButton.setText("Save trace 1")
        self.verticalLayout_5.addWidget(self.traceButton)    
        
        self.traceButton_2 = QtGui.QPushButton(self.settingsBox)
        self.traceButton_2.setText("Save trace 2")
        self.verticalLayout_5.addWidget(self.traceButton_2)  
        
        self.traceButton_3 = QtGui.QPushButton(self.settingsBox)
        self.traceButton_3.setText("Save trace 3")
        self.verticalLayout_5.addWidget(self.traceButton_3) 
        
        self.traces = [self.traceButton, self.traceButton_2, self.traceButton_3]        
        
        #MARKERS
        self.gridLayout = QtGui.QGridLayout()
        self.markerLabel = QtGui.QLabel(self.settingsBox)
        self.markerLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.markerLabel, 0,0)        
        self.markerCheck = QtGui.QCheckBox(self.settingsBox)
        self.gridLayout.addWidget(self.markerCheck, 0,1)
        self.markerEdit = QtGui.QDoubleSpinBox(self.settingsBox)
        self.markerEdit.setDecimals(2)
        self.markerEdit.setKeyboardTracking(False)
        self.markerEdit.setDisabled(True)
        self.markerEdit.setSingleStep(0.1)
        self.gridLayout.addWidget(self.markerEdit, 0,2)
        
        self.markerLabel_2 = QtGui.QLabel(self.settingsBox)
        self.markerLabel_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.markerLabel_2, 2,0)        
        self.markerCheck_2 = QtGui.QCheckBox(self.settingsBox)
        self.gridLayout.addWidget(self.markerCheck_2, 2,1)
        self.markerEdit_2 = QtGui.QDoubleSpinBox(self.settingsBox)
        self.markerEdit_2.setDecimals(2)
        self.markerEdit_2.setKeyboardTracking(False)
        self.markerEdit_2.setDisabled(True)
        self.markerEdit_2.setSingleStep(0.1)
        self.gridLayout.addWidget(self.markerEdit_2, 2,2)
        
        self.markerLabel_3 = QtGui.QLabel(self.settingsBox)
        self.markerLabel_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.markerLabel_3, 3,0)        
        self.markerCheck_3 = QtGui.QCheckBox(self.settingsBox)
        self.gridLayout.addWidget(self.markerCheck_3, 3,1)
        self.markerEdit_3 = QtGui.QDoubleSpinBox(self.settingsBox)
        self.markerEdit_3.setDecimals(2)
        self.markerEdit_3.setKeyboardTracking(False)
        self.markerEdit_3.setDisabled(True)
        self.markerEdit_3.setSingleStep(0.1)
        self.gridLayout.addWidget(self.markerEdit_3, 3,2)
        
        self.markerLabel_4 = QtGui.QLabel(self.settingsBox)
        self.markerLabel_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.markerLabel_4, 4,0)        
        self.markerCheck_4 = QtGui.QCheckBox(self.settingsBox)
        self.gridLayout.addWidget(self.markerCheck_4, 4,1)
        self.markerEdit_4 = QtGui.QDoubleSpinBox(self.settingsBox)
        self.markerEdit_4.setDecimals(2)
        self.markerEdit_4.setKeyboardTracking(False)
        self.markerEdit_4.setDisabled(True)
        self.markerEdit_4.setSingleStep(0.1)
        self.gridLayout.addWidget(self.markerEdit_4, 4,2)
        
        self.deltaLabel = QtGui.QLabel(self.settingsBox)
        self.deltaLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.deltaLabel, 1,0)        
        self.deltaCheck = QtGui.QCheckBox(self.settingsBox)
        self.gridLayout.addWidget(self.deltaCheck, 1,1)
        self.deltaEdit = QtGui.QDoubleSpinBox(self.settingsBox)
        self.deltaEdit.setDecimals(2)
        self.deltaEdit.setSingleStep(0.1)
        self.deltaEdit.setKeyboardTracking(False)
        self.deltaEdit.setDisabled(True)
        self.gridLayout.addWidget(self.deltaEdit, 1,2)
        self.deltaCheck.setDisabled(True)
        
        self.tab1 = QtGui.QWidget()
        self.settings_tabs.addTab(self.tab1, "Misc.")
        self.settings_tabs.widget(0).setLayout(self.verticalLayout_4)

        self.tab2 = QtGui.QWidget()
        self.settings_tabs.addTab(self.tab2, "Traces")  
        self.settings_tabs.widget(1).setLayout(self.verticalLayout_5)
        
        self.tab3 = QtGui.QWidget()
        self.settings_tabs.addTab(self.tab3, "Markers")
        self.settings_tabs.widget(2).setLayout(self.gridLayout)
        
        self.horizontalLayout_2.addWidget(self.settingsBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 847, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.addWidget(self.peakStatus)
        self.statusbar.setVisible(False)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.gainSlider.valueChanged.connect(self.gainDisp.display)
        self.saveButton.clicked.connect(self.savePlot)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Analizator 0.4", None))
        self.freqBox.setTitle(_translate("MainWindow", "Częstotliwość", None))
        self.label.setText(_translate("MainWindow", "START [MHz]:", None))
        self.label_2.setText(_translate("MainWindow", "STOP [MHz]:", None))
        self.label_3.setText(_translate("MainWindow", "RBW:", None))
        self.settingsBox.setTitle(_translate("MainWindow", "Ustawienia", None))
        self.gainLabel.setText(_translate("MainWindow", "Gain:", None))
        self.refLabel.setText(_translate("MainWindow", "REF:", None))
        self.holdLabel.setText(_translate("MainWindow", "Max HOLD:", None))
        self.centerLabel.setText(_translate("MainWindow", "Center [MHz]:", None))
        self.spanLabel.setText(_translate("MainWindow", "Span [MHz]:", None))
        self.avgLabel.setText(_translate("MainWindow", "Average:", None))
        self.avgLabel_2.setText(_translate("MainWindow", "Avg traces:", None))
        self.peakLabel.setText(_translate("MainWindow", "Peak search:", None))
        self.markerLabel.setText(_translate("MainWindow", "Marker 1:", None))        
        self.markerLabel_2.setText(_translate("MainWindow", "Marker 2:", None))
        self.markerLabel_3.setText(_translate("MainWindow", "Marker 3:", None))
        self.markerLabel_4.setText(_translate("MainWindow", "Marker 4:", None))
        self.deltaLabel.setText(_translate("MainWindow", "Delta 1:", None))
                    
    def savePlot(self):
        dialog = QtGui.QFileDialog()
        pixmap = QtGui.QPixmap()
        pixmap = pixmap.grabWidget(self.plot)
        fileName = dialog.getSaveFileName()
        print pixmap.save(fileName, format="PNG", quality = -1)
        print pixmap.isNull()
        print "Plot saved"
        
    def scaleColors(self, ref):
        self.colorMap.addColorStop(ref-60, Qt.Qt.cyan)
        self.colorMap.addColorStop(ref-40, Qt.Qt.green)
        self.colorMap.addColorStop(ref-20, Qt.Qt.yellow)
        

        
        

        
from PyQt4.Qwt5 import QwtPlot, QwtScaleDiv, QwtPlotPicker, QwtPicker, QwtPlotSpectrogram, QwtLinearColorMap, QwtPlotGrid, QwtPlotMarker, QwtSymbol, QwtRasterData
from PyQt4.Qwt5 import QwtPlotCurve

'''class WaterfallData(QwtRasterData):
    def __init__(self, length, parent=None):
        super(WaterfallData, self).__init__(parent)
        self.length = length
        self.data = []
        
    def addData(self, newData):
        self.data = newData + self.data[:-1]
                
    def value(self, x, y):
        return self.data[x][y]'''