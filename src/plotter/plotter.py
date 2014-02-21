from PySide.QtCore import QPoint, QTimer, SIGNAL, Qt
from PySide.QtGui import (QTreeWidgetItem, QFrame, QPainter, 
                          QMenu, QInputDialog, QGridLayout, 
                          QWidget, QComboBox, QMainWindow,
                          QPushButton, QSplitter, QMessageBox,
                          QFileDialog, QProgressDialog, QApplication,
                          QVBoxLayout) 
 
import pyqtgraph as pq

import matplotlib
from utils.extendedPyHPF import extendedPyHPF
from interactor import Interactor
from utils.updateTriggers import save
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar2#Agg as NavigationToolbar
from matplotlib.figure import Figure

from mainWindow_ui import Ui_MainWindow
from utils import plattform
from utils import pyHPF
from utils.server import DelsysStation
import numpy as np
from signalAnalysis import feature

import cPickle as pickle
import sys
import os

sys.modules['pyHPF'] = pyHPF
colors = ['#69A1C9', '#365691', '#CE8BE0', '#983BA1', '#AFDB84', '#43872D']#['b', 'g', 'r', 'c', 'm', 'y', 'k']
class DataItem(QTreeWidgetItem):
    '''
    QTreeWidgetItem and additionally 
    containing triggers, emg data and
    current frame of video
    '''
    
    def __init__(self, parent=None):
        self.emg = None
        super(DataItem, self).__init__(parent)
        self.triggers = []
        self.picture = None
        
        
    def setNumData(self, data):
        self.emg = np.asarray(data)
        
class DragWindow(QFrame):
    '''Widget to visualize and stream emg data
    
    - right click on points adds plots to stream data
    - right click otherwise opens context menu to start and set server
    - plots can be dragged by user
    '''
    def __init__(self, parent=None):
        super(DragWindow, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setStyleSheet("QFrame {background-image: url(../plotter/arm.jpg);background-repeat: no-repeat;}")
        
        self.server = DelsysStation(buffered=True)
        
        self.plots = {}
        self.points = [QPoint(538,705), QPoint(559,532), QPoint(588,730), 
                       QPoint(651,579), QPoint(645,394), QPoint(664,298)]
        
        timer = QTimer(self)
        self.connect(timer, SIGNAL("timeout()"), self.updatePlots)
        timer.start() #timed out as soon as all process finished
        
    def paintEvent(self, e):
        ''' overwrite paintEvent in order to also redraw points (indicating
        electrode positions) and their link to added plots
        
        this is necessary to get smooth animation if plots are dragged around
        '''
        super(DragWindow, self).paintEvent(e)
        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()
        
    def drawPoints(self, qp):
        ''' draw points for electrode positions and
        their connection lines to the plots
        '''
        qp.setPen(Qt.white)
        qp.setBrush(Qt.white)
        for key, item in self.plots.iteritems():
            pos = item.pos()
            pos = QPoint(pos.x()+item.size().width(), pos.y()+item.size().height())
            qp.drawLine(pos, self.points[int(key)-1])
            qp.drawEllipse(pos, 4,4)
        for pp in self.points:
            qp.drawEllipse(pp, 4,4)
        
    def addPlot(self, key):
        ''' adds a plot and link it to the clicked point '''
        if key in self.plots:
            return
        self.plots[key] = DragPlotWidget(self)
        self.plots[key].move(600,600)
        self.plots[key].show()
        self.update()  # updates widget leading to call of paintEvent
    
    def updatePlots(self):
        ''' plots are updated by reading server's buffer '''
        for item in self.plots.itervalues():
            data = self.server.buffer[0][:]
            item.updatePlot(data)
        
    def contextMenuEvent(self, e):
        ''' calls context menu if right click:
         - set server
         - trigger server (storts or stops the server)
        in case of righ click on point, a plot is added
        '''
        i = 0
        for pp in self.points:
            i += 1
            if (e.pos()-pp).manhattanLength() > 5:
                continue
            else:
                self.addPlot(str(i))
                return
        menu = QMenu()
        menu.addAction("Set Server", self.setServer)
        menu.addAction("Trigger Server", self.stream)
        menu.exec_(e.globalPos())
        
    def setServer(self):
        ''' dialog is opened to enter server address:
         e.g. localhost, 192.168.1.5
        '''
        text, ok = QInputDialog.getText(self, 'Input Dialog', 
            'Enter your server-address:')
        
        if ok:
            self.server.host = text

    def stream(self):
        ''' triggers server:
         - if already started -> stopped
         - if not started -> started
        '''
        if self.server.exitFlag:
            self.server.exitFlag = False
            self.server.start()
        else:
            self.server.exitFlag = True
            self.server.stop()
                
class DragPlotWidget(QFrame):
    ''' draggable widget plotting data and
    a combo box to choose channel
    '''
    
    def __init__(self, parent=None):
        super(DragPlotWidget, self).__init__(parent)
        
        # transparent fill color and a frame with size 400x250 
        self.setStyleSheet("QFrame {  border: 2px solid black; background-image: url(); }")
        self.setGeometry(1,1,400,250)
        
        # arrange elements in a gridLayout
        l = QGridLayout()
        self.setLayout(l)
        
        self.p = pq.PlotWidget(self)
        self.p.setYRange(-0.0002, 0.0002)
        self.pl1 = self.p.plot(np.linspace(0,3.4, 1000))  # initial plot
        
        self.box = QComboBox(self)
        self.box.addItems(["EMG " + str(x+1) for x in range(16)])
        self.box.currentIndexChanged.connect(self.changeChannel)
        
        l.addWidget(self.p)
        l.addWidget(self.box)
        
        self.dragPos = QPoint(0,0)
        
    def mousePressEvent(self, e):
        ''' enter drag mode by left click and save position '''
        if e.buttons() != Qt.LeftButton:
            return
        self.dragPos = e.pos()
        
    def mouseMoveEvent(self, e):
        ''' move by holding left mouse button and update position
        - removing offset by subtracting saved dragPos
        '''
        if e.buttons() != Qt.LeftButton:
            return
        position = e.pos() + self.pos() - self.dragPos
        self.move(position)
        self.update()
        self.parent().update()
    
    def mouseReleaseEvent(self, e):
        ''' release left mouse button and exit drag mode '''
        if e.buttons() != Qt.LeftButton:
            return
        position = e.pos() + self.pos() - self.dragPos
        self.move(position)
    
    def changeChannel(self, index):
        ''' change channel to index and clear plot '''
        self.p.plot([0], clear=True)
    
    def updatePlot(self, data):
        ''' plot new data '''
        self.p.plot(data[self.box.currentIndex()], clear=True)

class DataWrapper(object):
    def __init__(self, data):
        if len(data) == 3:
            print "oni -file"
            
        l = data[0][0].shape
        self.data = [None]*l[0]*4
        self.name = []
        for i in range(l[1]):
            name = str(i+1).zfill(2)
            for k in ('emg ', 'accX ', 'accY ', 'accZ '):
                self.name.append(k + name)
        
        self.data[::4] = data[0][0].tolist()
        for i in range(l[0]):
            for k in range(1,4):
                self.data[i*4+k] = data[0][1][i+k-1].tolist()
        self.triggers = data[1]

class Plotter(QMainWindow):
    ''' MainWindow consisting of menu bar, tab widget, tree list
    menu bar: load data
    tab widget: - dragWindow
                - widget consisting of picture viewer and two plots (raw and rms)
    tree list: to show loaded data, expand to see their channels and click to plot
    '''
    
    
    def __init__(self, parent=None):
        super(Plotter, self).__init__(parent)
        self.ui =  Ui_MainWindow()
        self.ui.setupUi(self)
        self.setCanvas()
        
        w = DragWindow()
        grid = QGridLayout()
        grid.addWidget(w)
        
        self.ui.tab_2.acceptDrops()
        self.ui.tab_2.setLayout(grid)
        
        self.moveConnection = None
        self.currentParent = None
        
        self.datas = []        
        self.offsetRecording = 0
        self.lines = [{}, {}]
    
    def setCanvas(self):
        ''' set widgets for a tab page
         - left side show image of current frame
         - right side show two plots: raw and rms
         - bot: button to edit triggers and slider to adjust 
                video-emg offset
        '''
        
        ########################
        # set matplotlib plots #
        ########################
        self.fig = Figure(dpi=70)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.ui.mainFrame)
        self.axes = self.fig.add_subplot(211)
        self.axesRMS = self.fig.add_subplot(212)
        self.mpl_toolbar = NavigationToolbar2(self.canvas, self.ui.mainFrame)
        self.canvas.mpl_connect('draw_event', self.onDraw)
        
        ####################################
        # add button to matplotlib toolbar #
        #################################### 
        redb = QPushButton('Edit Triggers')
        redb.setCheckable(True)
        self.mpl_toolbar.addWidget(redb)
        redb.clicked[bool].connect(self.toggleEditMode)
        
        # container for current frame of video 
        layout = pq.GraphicsLayoutWidget()
        vb = layout.addViewBox()
        vb.setAspectLocked(True)
        
        self.ri = pq.ImageItem()
        vb.addItem(self.ri)
        
        # layout to organize elements
        grid = QGridLayout()
        wrapper = QWidget()        
        vbox = QVBoxLayout(wrapper)
        splitter = QSplitter()
        
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.mpl_toolbar)
        wrapper.setLayout(vbox)
        
        splitter.addWidget(layout)
        splitter.addWidget(wrapper)
        
        grid.addWidget(splitter)
        
        self.ri.show()
        layout.show()
        self.ui.mainFrame.setLayout(grid)
        
    def loadData(self):
        ''' open dialog for choosing files to load '''
        fileNames, ok1= QFileDialog.getOpenFileNames(
                     self, self.tr("Open data"),
                     plattform.fixpath("D:\Master\emg\Benedictus"), self.tr("Pickle Files (*.pk)"))
        if ok1:
            self.load(fileNames)
    
    def load(self, fileNames):
        ''' unpickles data and add elements to tree view
        in case loading takes a while, a progress bar shows current status 
        '''
        progress = QProgressDialog("Loading files...", "Abort Copy", 0, len(fileNames), self)
        progress.setWindowModality(Qt.WindowModal)
        i = 0
        for fileName in fileNames:
            with open(fileName, 'rb') as ifile:
                tmp = pickle.load(ifile)
                if os.path.isfile(fileName[:-2] + "oni"):
                    tmp = tmp + (fileName[:-2]+"oni",)
                if isinstance(tmp, pyHPF.pyHPF):
                    self.datas.append(tmp)
                else:
                    self.datas.append(extendedPyHPF(tmp))
                self.updateTree(fileName[-5:])
                
                i+=1
                progress.setValue(i)

    def updateTree(self, name):
        ''' adds DataItem to tree view '''
        dataItem = QTreeWidgetItem(self.ui.dataView)
        dataItem.setText(0, name)
        dataItem.setFlags(Qt.ItemIsEnabled|Qt.ItemIsEditable)
        for i in range(len(self.datas[-1].data)/4):
            x = DataItem(dataItem)
            x.setText(0, self.datas[-1].name[i*4])
            x.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
            x.setNumData(self.datas[-1].data[i*4])
            if hasattr(self.datas[-1], 'triggers'):
                x.triggers = self.datas[-1].triggers
            if hasattr(self.datas[-1], 'frames'):
                x.depth = self.datas[-1].seekFrame
                
    def toggleEditMode(self, toggle):
        ''' button pressed to toggle edit mode for triggers
         - if pressed in edit mode again, dialog to save changes to
           a existing file
        '''
        if toggle:
            item = self.ui.dataView.selectedItems()[-1]
            self.interactionMode = Interactor(self.canvas,
                                              [self.axes, self.axesRMS], 
                                              item.triggers, self.lines, item.emg.shape[0])
        else:
            self.interactionMode = None
            reply = QMessageBox.question(self, 'QMessageBox.question()',
                             'Update triggers?',
                             QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                fileName, ok= QFileDialog.getOpenFileName(
                                    self, self.tr("Choose which file to overwrite data"),
                
                plattform.fixpath("D:\Master\emg\Benedictus"), self.tr("Pickle Files (*.pk)"))
                if ok:
                    save(self.ui.dataView.selectedItems()[-1].triggers, fileName)
        
    def plotData(self):
        ''' clicking a DataItem will plot the raw data and rms of
        emg data
        - if oni files are present, it will connect the mouse position inside
          plots to frame number of video 
        '''
        
        #################
        #   clearing    #
        #################
        self.axes.clear()
        self.axesRMS.clear()
        if self.moveConnection is not None:
            self.canvas.mpl_disconnect(self.moveConnection)
        
        ########################
        #  get selected item   #
        ########################
        if len(self.ui.dataView.selectedItems()) > 0:
            item = self.ui.dataView.selectedItems()[-1]
            if hasattr(item, 'depth'):
                self.ui.offsetSlider.setEnabled(True)
                ''' if selected channel is from other dataset
                 - slider is available
                 - current frame of video is set
                 - and new parent is saved
                '''
                if item.parent() is not self.currentParent:
                    self.offsetRecording = 0
                    self.ui.offsetSlider.setValue(150)
                    if self.currentParent:
                        self.currentParent.child(0).depth(-1)
                    self.ri.setImage(item.depth(0))
                    self.currentParent = item.parent()
        ########################
        # if deselected, reset #
        ########################
        else:
            self.ui.offsetSlider.setEnabled(False)
            self.ri.setImage(np.zeros((1,1,1)))
        
        ##########################
        # plot selected data     #
        ##########################
        for item in self.ui.dataView.selectedItems():
            c = int(item.text(0)[-1])-1
            if c >= len(colors):
                c = c % len(colors)
            self.axes.plot(item.emg, label=item.text(0), c=colors[c])
            self.axesRMS.plot(feature.rootMeanSquare(np.abs(item.emg), 200), c=colors[c])
            
            self.lines = [{}, {}]
            for p in item.triggers:
                self.lines[0][p], = self.axes.plot([p]*2, [np.min(item.emg), np.max(item.emg)], c='k', animated = True)
                self.lines[1][p], = self.axesRMS.plot([p]*2, [np.min(item.emg), np.max(item.emg)], c='k', animated = True)
            c+=1
        
        # connect mouse position inside plots to frame index of video
        self.moveConnection = self.canvas.mpl_connect("motion_notify_event", self.updateVideo)

        self.axes.legend()
        self.canvas.draw()
        
    def onDraw(self, event):
        ''' partially updating plots
        see: http://wiki.scipy.org/Cookbook/Matplotlib/Animations#head-3d51654b8306b1585664e7fe060a60fc76e5aa08
        '''
        items = self.ui.dataView.selectedItems()
        if len(items)== 0: return
        
        for i in range(2):
            ax = [self.axes, self.axesRMS]
            for t in items[-1].triggers:
                ax[i].draw_artist(self.lines[i][t])

        self.canvas.blit()
            
    def correctOffset(self, offs):
        self.offsetRecording = offs-150
        
    def updateVideo(self, event):
        ''' set frame index according to mouse position '''
        if event.xdata is not None:
            frameIdx = int(event.xdata/2000.0*30 + self.offsetRecording)
            if frameIdx < 0:
                frameIdx = 0
            if len(self.ui.dataView.selectedItems()) > 0:
                if hasattr(self.ui.dataView.selectedItems()[-1], 'depth'):
                    self.ri.setImage(self.ui.dataView.selectedItems()[-1].depth(frameIdx)) 
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mySW = Plotter()
    mySW.show()
    sys.exit(app.exec_())