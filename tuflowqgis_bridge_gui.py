# coding=utf-8
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui
from qgis.core import *
from qgis.gui import *
from canvas_event import canvasEvent
import matplotlib
import matplotlib.pyplot as plt
from tuflowqgis_bridge_editor import *
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/forms")
from ui_tuflowqgis_bridge_editor import Ui_tuflowqgis_BridgeEditor

class bridgeGui(QDockWidget, Ui_tuflowqgis_BridgeEditor):

    def __init__(self, iface, **kwargs):
        QDockWidget.__init__(self)
        self.wdg = Ui_tuflowqgis_BridgeEditor.__init__(self)
        self.setupUi(self)
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.bridges = {}  # lyr name,fid: bridgeEditor class object
        self.connected = False
        self.new_bridge = False
        self.initialisePlot()
        self.populateDems()
        #self.newBridge()
        
        self.qgis_connect()

    def qgis_connect(self):
        """
        Set up signal connections.

        :return: void
        """
    
        if not self.connected:
            self.canvas.layersChanged.connect(self.populateDems)
            #self.canvas.layersChanged.connect(self.checkForBridge)
            self.canvas.currentLayerChanged.connect(self.checkForBridge)
            self.canvas.selectionChanged.connect(self.checkForBridge)
            self.pbDrawXsection.clicked.connect(self.startNewBridge)
            self.connected = True

    def qgis_disconnect(self):
        """
        Disconnect signal connections

        :return: void
        """
    
        if self.connected:
            self.canvas.layersChanged.disconnect(self.populateDems)
            #self.canvas.layersChanged.disconnect(self.checkForBridge)
            self.canvas.currentLayerChanged.disconnect(self.checkForBridge)
            self.canvas.selectionChanged.disconnect(self.checkForBridge)
            self.pbDrawXsection.clicked.disconnect(self.startNewBridge)
            self.connected = False

    def initialisePlot(self):
        """
        Initialise matplotlib plotting

        :return: void matplotlib plot widget
        """

        # Initialise ui packing
        self.layout = self.frame_for_plot_2.layout()
        minsize = self.minimumSize()
        maxsize = self.maximumSize()
        self.setMinimumSize(minsize)
        self.setMaximumSize(maxsize)
        self.iface.mapCanvas().setRenderFlag(True)
        # Initialise plotting parameters
        self.artists = []
        self.labels = []
        self.fig, self.subplot = plt.subplots()
        font = {'family': 'arial', 'weight': 'normal', 'size': 12}
        rect = self.fig.patch
        rect.set_facecolor((0.9, 0.9, 0.9))
        self.subplot.set_xbound(0, 1000)
        self.subplot.set_ybound(0, 1000)
        self.manageMatplotlibAxe(self.subplot)
        canvas = FigureCanvasQTAgg(self.fig)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        canvas.setSizePolicy(sizePolicy)
        self.plotWdg = canvas
        self.gridLayout_3.addWidget(self.plotWdg)
        if matplotlib.__version__ < 1.5:
            mpltoolbar = matplotlib.backends.backend_qt4agg.NavigationToolbar2QTAgg(self.plotWdg,
                                                                                    self.frame_for_toolbar)
        else:
            mpltoolbar = matplotlib.backends.backend_qt4agg.NavigationToolbar2QT(self.plotWdg,
                                                                                 self.frame_for_toolbar)
        lstActions = mpltoolbar.actions()
        mpltoolbar.removeAction(lstActions[7])  # remove customise subplot
        # create curve
        label = "test"
        x = numpy.linspace(-numpy.pi, numpy.pi, 201)
        y = numpy.sin(x)
        a, = self.subplot.plot(x, y)
        self.artists.append(a)
        self.labels.append(label)
        self.subplot.hold(True)
        # self.fig.tight_layout()
        self.plotWdg.draw()

    def manageMatplotlibAxe(self, axe1):
        """
        Settings for matplotlib axis

        :param axe1: matplotlib axis object
        :return: void
        """

        axe1.grid()
        axe1.tick_params(axis="both", which="major", direction="out", length=10, width=1, bottom=True, top=False,
                         left=True, right=False)
        axe1.minorticks_on()
        axe1.tick_params(axis="both", which="minor", direction="out", length=5, width=1, bottom=True, top=False,
                         left=True, right=False)

    def populateDems(self):
        """
        Find all QgsRasterLayer in map window and populates dropdown box

        :return: void populated dropdown box
        """
    
        dem = self.demComboBox.currentText()
        self.demComboBox.clear()
        rasterLyrs = findAllRasterLyrs()
        if len(rasterLyrs) > 0:
            demIndex = None
            for i, raster in enumerate(rasterLyrs):
                self.demComboBox.addItem(raster)
                if raster == dem:
                    demIndex = i
            if demIndex is not None:
                self.demComboBox.setCurrentIndex(demIndex)
    
    def startNewBridge(self):
        import pydevd
        pydevd.settrace('localhost', port=53100, stdoutToServer=True, stderrToServer=True)
        self.bridge = bridgeEditor(self, self.iface)
        self.bridge.useTempPolyline()

    def checkForBridge(self):
        import pydevd
        pydevd.settrace('localhost', port=53100, stdoutToServer=True, stderrToServer=True)
        self.saveBridge()
        lyr = self.canvas.currentLayer()
        if lyr.type() == 0:  # QgsVectorLayer
            lyrName = lyr.name()
            feat = lyr.selectedFeatures()
            if len(feat) > 0:
                fid = feat[0].id()
                bridgeKey = '{0},{1}'.format(lyrName, fid)
                if bridgeKey in self.bridges.keys():
                    self.loadBridge(self.bridges[bridgeKey])
                #else:
                #    self.newBridge()
                #    self.new_bridge = True
        #else:
        #    self.newBridge()
        #    self.new_bridge = True
        
    def loadBridge(self, bridge):
        import pydevd
        pydevd.settrace('localhost', port=53100, stdoutToServer=True, stderrToServer=True)
        self.bridge = bridge
        self.bridge.loadEditor(self)
        self.bridge.loadData()
    
    def newBridge(self):
        import pydevd
        pydevd.settrace('localhost', port=53100, stdoutToServer=True, stderrToServer=True)
        self.bridge = bridgeEditor(self, self.iface)
        
    def saveBridge(self):
        if self.bridge.updated:
            lyr = self.bridge.layer
            lyrName = lyr.name()
            feat = self.bridge.feature
            fid = feat.id()
            self.bridge.updated = False
            self.bridges['{0},{1}'.format(lyrName, fid)] = self.bridge
            self.new_bridge = False
        #lyr = self.canvas.currentLayer()
        #if lyr.type() == 0:  # QgsVetorLayer
        #    lyrName = lyr.name()
        #elif lyr.type() == 1:  # QgsRasterLayer
        #    lyr = bridge.layer
        #    if lyr is not None:
        #        lyrName = lyr.name()
        #    else:
        #        return
        #else:
        #    return
        #if self.bridge.updated:
        #    feat = lyr.selectedFeatures()
        #    if len(feat) > 0:
        #        fid = feat[0].id()
        #        self.bridges['{0},{1}'.format(lyrName, fid)] = self.bridge
        #        self.bridge.updated = False

