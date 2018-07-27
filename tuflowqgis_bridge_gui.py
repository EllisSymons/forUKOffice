# coding=utf-8
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui
from qgis.core import *
from qgis.gui import *
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
        self.populateDems()
        self.newBridge()
        
        self.qgis_connect()

    def qgis_connect(self):
        """
        Set up signal connections.

        :return: void
        """
    
        if not self.connected:
            self.canvas.layersChanged.connect(self.populateDems)
            self.canvas.selectionChanged.connect(self.checkForBridge)
            self.connected = True

    def qgis_disconnect(self):
        """
        Disconnect signal connections

        :return: void
        """
    
        if self.connected:
            self.canvas.layersChanged.disconnect(self.populateDems)
            self.canvas.selectionChanged.disconnect(self.checkForBridge)
            self.connected = False

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
    
    def checkForBridge(self):
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
                else:
                    self.newBridge()
        else:
            self.newBridge()
        
    def loadBridge(self, bridge):
        self.bridge = bridge
        self.bridge.loadEditor(self)
        self.bridge.loadData()
        self.bridge.updatePlot()
    
    def newBridge(self):
        self.bridge = bridgeEditor(self, self.iface)
        
    def saveBridge(self):
        lyr = self.canvas.currentLayer()
        if lyr.type() == 0:  # QgsVetorLayer
            lyrName = lyr.name()
        #elif lyr.type() == 1:  # QgsRasterLayer
        #    lyr = bridge.layer
        #    if lyr is not None:
        #        lyrName = lyr.name()
        #    else:
        #        return
        else:
            return
        if self.bridge.updated:
            feat = lyr.selectedFeatures()
            if len(feat) > 0:
                fid = feat[0].id()
                self.bridges['{0},{1}'.format(lyrName, fid)] = self.bridge
                self.bridge.updated = False