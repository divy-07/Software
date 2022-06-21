import random
import numpy as np

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, mkQApp, QtCore


class PassGenerator(QtWidgets.QMainWindow):

    MIN_VAL = 0
    MAX_VAL = 1
    X_SIZE = 40
    Y_SIZE = 40

    def __init__(self):
        super(PassGenerator, self).__init__()
        gr_wid = pg.GraphicsLayoutWidget(show=True)
        self.setCentralWidget(gr_wid)
        self.show()
        self.count = 0

        self.arr = []

        for i in range(PassGenerator.X_SIZE): # this is how many cols there will be after transpose
            self.arr.append([])

        for i in range(PassGenerator.X_SIZE):
            for j in range(PassGenerator.Y_SIZE):
                self.arr[i].append(0)

        self.data = np.array(self.arr).transpose()

        self.p1 = gr_wid.addPlot()
        self.i1 = pg.ImageItem(image=self.data)
        self.p1.addItem(self.i1)

        self.p1.setMouseEnabled( x=True, y=True)
        self.p1.setRange(xRange=(0,PassGenerator.Y_SIZE), yRange=(0,PassGenerator.X_SIZE), padding=0)
        self.p1.showAxes(True, showValues=(True,False,False,True))

    def refresh(self):

        # update self.data
        for i in range(PassGenerator.X_SIZE):
            for j in range(PassGenerator.Y_SIZE):
                self.arr[i][j] = (random.randint(0,100))/100

        self.data = np.array(self.arr).transpose()
        # self.p1.removeItem(self.i1)
        self.p1.clear()
        self.i1 = pg.ImageItem(image=self.data)
        self.p1.addItem(self.i1)






"""
------------- Sample script ----------------

import time
import random
import numpy as np

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, mkQApp, QtCore

MIN_VAL = 0
MAX_VAL = 1
X_SIZE = 40
Y_SIZE = 40
FPS = 60
time_vals = []

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        gr_wid = pg.GraphicsLayoutWidget(show=True)
        self.setCentralWidget(gr_wid)
        self.setWindowTitle('pyqtgraph example: Interactive color bar')
        self.resize(600,500)
        self.show()
        self.count = 0

        self.arr = []
        
        for i in range(X_SIZE): # this is how many cols there will be after transpose
            self.arr.append([])
        
        for i in range(X_SIZE):
            for j in range(Y_SIZE):
                self.arr[i].append(0)
        
        for i in range(X_SIZE):
            for j in range(Y_SIZE):
                self.arr[i][j] = i*j/1600
        
        self.data = np.array(self.arr).transpose()

        #--- add non-interactive image with integrated color ------------------
        self.p1 = gr_wid.addPlot()
        # Basic steps to create a false color image with color bar:
        self.i1 = pg.ImageItem(image=self.data)
        self.p1.addItem(self.i1)
        self.p1.addColorBar(self.i1, colorMap='magma', values=(MIN_VAL, MAX_VAL), interactive=False)

        self.p1.setMouseEnabled( x=True, y=True)
        self.p1.setRange(xRange=(0,Y_SIZE), yRange=(0,X_SIZE), padding=0)
        self.p1.showAxes(True, showValues=(True,False,False,True) )

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)

        self.timer.timeout.connect(self.updateData)
        self.updateData()
    
    def updateData(self):
        
        ## Display the new self.data set
        t0 = time.perf_counter()
        
        # update self.data
        for i in range(X_SIZE):
            for j in range(Y_SIZE):
                # x = self.arr[i][j]
                # if x > MAX_VAL:
                #     self.arr[i][j] = MIN_VAL
                # else:
                #     self.arr[i][j] += 0.01
                self.arr[i][j] = (random.randint(0,100))/100

        t1 = time.perf_counter()
        
        self.data = np.array(self.arr).transpose()
        # self.p1.removeItem(self.i1)
        self.p1.clear()
        self.i1 = pg.ImageItem(image=self.data)
        self.p1.addItem(self.i1)
        
        t2 = time.perf_counter()
        
        time_vals.append((t2-t0) * 1000)
        self.count += 1
        if self.count % 60 == 0:
            print(np.mean(time_vals))
        
        # print((t2-t0) * 1000)

        # cap update rate at fps
        delay = max(1000/FPS - (t2 - t0), 0)
        self.timer.start(int(delay))
        
        
mkQApp("ColorBarItem Example")
main_window = MainWindow()
main_window.updateData()

## Start Qt event loop
if __name__ == '__main__':
    pg.exec()
"""