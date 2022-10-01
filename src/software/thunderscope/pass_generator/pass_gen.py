import random
import numpy as np

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, mkQApp, QtCore

# colorbaritem
# isocurves - elevation map - looks very nice
# histogram
# 3d open gl

"""
# -------------ColorBar Item implementation-new dock--------------- works
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

"""
# ------------- ColorBarItem script ----------------

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

""""""
# -------------Isocurves implementation-new dock---------------WORKS
class PassGenerator(QtWidgets.QMainWindow):

    MIN_VAL = 0
    MAX_VAL = 1
    X_SIZE = 40
    Y_SIZE = 40

    def __init__(self):
        super(PassGenerator, self).__init__()

        ## make pretty looping data
        frames = 200
        self.data = np.random.normal(size=(frames,30,30), loc=0, scale=100)
        self.data = np.concatenate([self.data, self.data], axis=0)
        self.data = pg.gaussianFilter(self.data, (10, 10, 10))[frames//2:frames + frames//2]
        self.data[:, 15:16, 15:17] += 1

        win = pg.GraphicsLayoutWidget(show=True)
        self.vb = win.addViewBox()
        self.img = pg.ImageItem(self.data[0])
        self.vb.addItem(self.img)
        self.vb.setAspectLocked()
        self.setCentralWidget(win)

        ## generate empty curves
        self.curves = []
        self.levels = np.linspace(self.data.min(), self.data.max(), 10)
        for i in range(len(self.levels)):
            v = self.levels[i]
            ## generate isocurve with automatic color selection
            c = pg.IsocurveItem(level=v, pen=(i, len(self.levels)*1.5))
            c.setParentItem(self.img)  ## make sure isocurve is always correctly displayed over image
            c.setZValue(10)
            self.curves.append(c)

        ## animate!
        self.ptr = 0
        self.imgLevels = (self.data.min(), self.data.max() * 2)

    def refresh(self):
        self.ptr = (self.ptr + 1) % self.data.shape[0]
        self.img.setImage(self.data[self.ptr])
        for c in self.curves:
            c.setParentItem(self.img)
            c.setData(self.data[self.ptr])
""""""

"""
# ----------------------Isocurve haf working implementation----------------------------
class PassGenerator(QtWidgets.QMainWindow):

    MIN_VAL = 0
    MAX_VAL = 1
    X_SIZE = 40
    Y_SIZE = 40

    def __init__(self):
        super(PassGenerator, self).__init__()
        # win = QtWidgets.QWidget()
        win = pg.GraphicsLayoutWidget(show=True)
        self.setCentralWidget(win)
        self.show()

        layout = QtWidgets.QGridLayout()
        win.setLayout(layout)

        ## make pretty looking data
        frames = 200
        self.data = np.random.normal(size=(frames,30,30), loc=0, scale=100)
        self.data = np.concatenate([self.data, self.data], axis=0)
        self.data = pg.gaussianFilter(self.data, (10, 10, 10))[frames//2:frames + frames//2]
        self.data[:, 15:16, 15:17] += 1

        view = pg.GraphicsView()
        # self.vb = pg.ViewBox()
        self.vb = win.addViewBox()
        self.vb.setAspectLocked()
        view.setCentralItem(self.vb)
        layout.addWidget(view)

        self.img = pg.ImageItem(self.data[0])
        self.vb.addItem(self.img)

        ## generate empty curves
        self.curves = []
        self.levels = np.linspace(self.data.min(), self.data.max(), 10)
        for i in range(len(self.levels)):
            v = self.levels[i]
            ## generate isocurve with automatic color selection
            c = pg.IsocurveItem(level=v, pen=(i, len(self.levels)*1.5))
            c.setParentItem(self.vb)  ## make sure isocurve is always correctly displayed over image
            c.setZValue(10)
            self.curves.append(c)

        ## animate!
        self.ptr = 0
        self.imgLevels = (self.data.min(), self.data.max() * 2)

    def refresh(self):
        self.ptr = (self.ptr + 1) % self.data.shape[0]
        self.vb.clear()
        self.img = pg.ImageItem(self.data[self.ptr])
        self.vb.addItem(self.img)
        for c in self.curves:
            c.setParentItem(self.vb)
            c.setData(self.data[self.ptr])
"""

"""
# ------------- IsoCurve script ----------------
import numpy as np

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore

app = pg.mkQApp("Isocurve Example")

## make pretty looking data
frames = 200
data = np.random.normal(size=(frames,30,30), loc=0, scale=100)
data = np.concatenate([data, data], axis=0)
data = pg.gaussianFilter(data, (10, 10, 10))[frames//2:frames + frames//2]
data[:, 15:16, 15:17] += 1

win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('pyqtgraph example: Isocurve')
vb = win.addViewBox()
img = pg.ImageItem(data[0])
vb.addItem(img)
vb.setAspectLocked()

## generate empty curves
curves = []
levels = np.linspace(data.min(), data.max(), 10)
for i in range(len(levels)):
    v = levels[i]
    ## generate isocurve with automatic color selection
    c = pg.IsocurveItem(level=v, pen=(i, len(levels)*1.5))
    c.setParentItem(img)  ## make sure isocurve is always correctly displayed over image
    c.setZValue(10)
    curves.append(c)

## animate!
ptr = 0
imgLevels = (data.min(), data.max() * 2)
def update():
    global data, curves, img, ptr, imgLevels
    ptr = (ptr + 1) % data.shape[0]
    data[ptr]
    img.setImage(data[ptr], levels=imgLevels)
    for c in curves:
        c.setData(data[ptr])

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

if __name__ == '__main__':
    pg.exec()
"""

"""
# -------------Histogram implementation-new dock--------------- works
class PassGenerator(QtWidgets.QMainWindow):

    MIN_VAL = 0
    MAX_VAL = 1
    X_SIZE = 40
    Y_SIZE = 40

    def __init__(self):
        super(PassGenerator, self).__init__()
        cw = QtWidgets.QWidget()
        self.setCentralWidget(cw)
        self.show()

        layout = QtWidgets.QGridLayout()
        cw.setLayout(layout)
        layout.setSpacing(0)

        view = pg.GraphicsView()
        self.vb = pg.ViewBox()
        self.vb.setAspectLocked()
        view.setCentralItem(self.vb)
        layout.addWidget(view, 0, 1, 3, 1)

        self.hist = pg.HistogramLUTWidget(gradientPosition="left")
        layout.addWidget(self.hist, 0, 2)

        monoRadio = QtWidgets.QRadioButton('mono')
        rgbaRadio = QtWidgets.QRadioButton('rgba')
        layout.addWidget(monoRadio, 1, 2)
        layout.addWidget(rgbaRadio, 2, 2)
        monoRadio.setChecked(True)

        data = pg.gaussianFilter(np.random.normal(size=(256, 256, 3)), (20, 20, 0))
        for i in range(32):
            for j in range(32):
                data[i*8, j*8] += .1
        img = pg.ImageItem(data)
        self.vb.addItem(img)
        self.vb.autoRange()

        self.hist.setImageItem(img)

    def refresh(self):
        data = pg.gaussianFilter(np.random.normal(size=(256, 256, 3)), (20, 20, 0))
        for i in range(32):
            for j in range(32):
                data[i*8, j*8] += .1
        img = pg.ImageItem(data)
        self.vb.clear()
        self.vb.addItem(img)
        self.vb.autoRange()

        self.hist.setImageItem(img)
"""

"""
# ------------- Histogram script ---------------- 
import numpy as np

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets

app = pg.mkQApp("Histogram Lookup Table Example")
win = QtWidgets.QMainWindow()
win.resize(880, 600)
win.show()
win.setWindowTitle('pyqtgraph example: Histogram LUT')

cw = QtWidgets.QWidget()
win.setCentralWidget(cw)

layout = QtWidgets.QGridLayout()
cw.setLayout(layout)
layout.setSpacing(0)

view = pg.GraphicsView()
vb = pg.ViewBox()
vb.setAspectLocked()
view.setCentralItem(vb)
layout.addWidget(view, 0, 1, 3, 1)

hist = pg.HistogramLUTWidget(gradientPosition="left")
layout.addWidget(hist, 0, 2)


monoRadio = QtWidgets.QRadioButton('mono')
rgbaRadio = QtWidgets.QRadioButton('rgba')
layout.addWidget(monoRadio, 1, 2)
layout.addWidget(rgbaRadio, 2, 2)
monoRadio.setChecked(True)


def setLevelMode():
    mode = 'mono' if monoRadio.isChecked() else 'rgba'
    hist.setLevelMode(mode)


monoRadio.toggled.connect(setLevelMode)

data = pg.gaussianFilter(np.random.normal(size=(256, 256, 3)), (20, 20, 0))
for i in range(32):
    for j in range(32):
        data[i*8, j*8] += .1
img = pg.ImageItem(data)
vb.addItem(img)
vb.autoRange()

hist.setImageItem(img)

if __name__ == '__main__':
    pg.exec()
"""

