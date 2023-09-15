import numpy as np
import segyio
import sys

import pyvista as pv

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLCDNumber
from pyvistaqt import QtInteractor, MainWindow

#segy_data = segyio.cube('SEG_C3NA_Velocity.sgy')[:350]
#print(segy_data.shape)



class MyMainWindow(MainWindow):

    segy_data = None

    def __init__(self, parent=None, show=True):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.setFixedSize(1000, 800)

        # create the frame
        self.frame = QtWidgets.QFrame()        
        vlayout = QtWidgets.QVBoxLayout()
        glayout = QtWidgets.QGridLayout() 

        self.filename_label = QtWidgets.QLabel()
        vlayout.addWidget(self.filename_label)

        # add the pyvista interactor object
        self.plotter = QtInteractor(self.frame)               
        vlayout.addWidget(self.plotter.interactor)
        self.signal_close.connect(self.plotter.close)
        
        glayout.addWidget(QtWidgets.QLabel('1st index:'), 0, 0)
        self.first_index_start_spinbox = QtWidgets.QSpinBox()
        self.first_index_end_spinbox = QtWidgets.QSpinBox()    
        glayout.addWidget(self.first_index_start_spinbox, 0, 1)
        glayout.addWidget(self.first_index_end_spinbox, 0, 2)

        glayout.addWidget(QtWidgets.QLabel('2nd index:'), 1, 0)
        self.second_index_start_spinbox = QtWidgets.QSpinBox()
        self.second_index_end_spinbox = QtWidgets.QSpinBox()        
        glayout.addWidget(self.second_index_start_spinbox, 1, 1)
        glayout.addWidget(self.second_index_end_spinbox, 1, 2)
        
        glayout.addWidget(QtWidgets.QLabel('3rd index:'), 2, 0)
        self.third_index_start_spinbox = QtWidgets.QSpinBox()
        self.third_index_end_spinbox = QtWidgets.QSpinBox()      
        glayout.addWidget(self.third_index_start_spinbox, 2, 1)
        glayout.addWidget(self.third_index_end_spinbox, 2, 2)

        self.cut_button = QtWidgets.QPushButton('Cut')
        glayout.addWidget(self.cut_button, 0, 3)
        self.cut_button.clicked.connect(self.cut_data)
        self.reset_button = QtWidgets.QPushButton('Reset')
        self.reset_button.clicked.connect(self.reset_data)
        glayout.addWidget(self.reset_button, 1, 3)
        

        vlayout.addLayout(glayout)

        self.frame.setLayout(vlayout)        
        self.setCentralWidget(self.frame)

        # simple menu to demo functions
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        openButton = QtWidgets.QAction('Open', self)
        openButton.setShortcut('Ctrl+O')
        openButton.triggered.connect(self.open_sgy)
        fileMenu.addAction(openButton)
        exitButton = QtWidgets.QAction('Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)
    

        if show:
            self.show()

    def open_sgy(self):
        file , check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                               "", "All Files (*);;SEG-Y Files (*.sgy)")
        if check:

            self.filename_label.setText(file)
            
            self.segy_data = segyio.cube(file)
            print(self.segy_data.shape)
                       
            self.first_index_start_spinbox.setRange(1, self.segy_data.shape[0])     
            self.first_index_end_spinbox.setRange(1, self.segy_data.shape[0])         
            self.first_index_start_spinbox.setValue(1)
            self.first_index_end_spinbox.setValue(self.segy_data.shape[0])
            

            self.second_index_start_spinbox.setRange(1, self.segy_data.shape[1]) 
            self.second_index_end_spinbox.setRange(1, self.segy_data.shape[1]) 
            self.second_index_start_spinbox.setValue(1)
            self.second_index_end_spinbox.setValue(self.segy_data.shape[1])

            self.third_index_start_spinbox.setRange(1, self.segy_data.shape[2]) 
            self.third_index_end_spinbox.setRange(1, self.segy_data.shape[2])
            self.third_index_start_spinbox.setValue(1)
            self.third_index_end_spinbox.setValue(self.segy_data.shape[2])

            data = pv.wrap(np.flip(self.segy_data, axis=2))
            self.plotter.clear()
            self.plotter.add_volume(data)
            self.plotter.reset_camera()
            self.plotter.add_bounding_box()
            self.plotter.show_axes_all()

          #  data.plot(volume=True) # Volume render

    def cut_data(self):
        first_start = self.first_index_start_spinbox.value()-1  
        first_end = self.first_index_end_spinbox.value()-1
        second_start = self.second_index_start_spinbox.value()-1
        second_end = self.second_index_end_spinbox.value()-1
        third_start = self.third_index_start_spinbox.value()-1
        third_end = self.third_index_end_spinbox.value()-1
        if first_start>first_end or second_start>second_end or third_start>third_end:
            return
        max_z = self.segy_data.shape[2]
        data = pv.wrap(np.flip(self.segy_data[first_start:first_end+1, 
                                              second_start:second_end+1, 
                                              third_start: third_end+1], axis=2))
        self.plotter.clear()
        self.plotter.add_volume(data)
        self.plotter.reset_camera()

    def reset_data(self):           
                
        self.first_index_start_spinbox.setValue(1)
        self.first_index_end_spinbox.setValue(self.segy_data.shape[0])   

    
        self.second_index_start_spinbox.setValue(1)
        self.second_index_end_spinbox.setValue(self.segy_data.shape[1])
        
        self.third_index_start_spinbox.setValue(1)
        self.third_index_end_spinbox.setValue(self.segy_data.shape[2])

        data = pv.wrap(np.flip(self.segy_data, axis=2))
        self.plotter.clear()
        self.plotter.add_volume(data)
        self.plotter.reset_camera()




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("CubeView version 0.1")
    window = MyMainWindow()
    sys.exit(app.exec_())
