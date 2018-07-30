from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui
from qgis.core import *
from qgis.gui import *
import sys
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.patches import Patch
from matplotlib.patches import Polygon
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from tuflowqgis_settings import TF_Settings
from tuflowqgis_library import lineToPoints, getRasterValue
from tuflowqgis_bridge_context_menus import *
from tuflowqgis_bridge_rubberband import *
from tuflowqgis_bridge_layer_edit import *
from canvas_event import canvasEvent
from Pier_Losses import lookupPierLoss
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/forms")
# Debug using PyCharm
sys.path.append(r'C:\Program Files\JetBrains\PyCharm 2018.1\debug-eggs')
sys.path.append(r'C:\Program Files\JetBrains\PyCharm 2018.1\helpers\pydev')

#class bridgeEditor(QDockWidget, Ui_tuflowqgis_BridgeEditor):
class bridgeEditor():

    def __init__(self, bridge, iface, **kwargs):
        self.updated = False
        self.bridge = bridge  # bridge gui class
        self.iface = iface  # QgsInterface
        self.canvas = self.iface.mapCanvas()  # QgsMapCanvas
        self.connected = False  # signal connections
        self.cursorTrackingConnected = False  # temp polyline signals
        self.xSectionOffset = []  # XSection offset values
        self.pierOffset = []  # list of pier offsets [[pier 1 offset], [pier 2 offset]]
        self.pierRowHeaders = []  # list of pier row names
        self.pierPatches = []  # patches used for plotting piers
        self.deckPatch = []  # patch used for plotting deck
        self.rubberBand = QgsRubberBand(self.iface.mapCanvas(), False)  # temporary polyline
        self.points = []  # QgsPoints used for temporary created layer
        self.obverts = []  # list of obvert values aligning with xSectionOffset list
        self.area = 0  # area under bridge deck
        self.pierArea = 0  # area of piers in waterway
        self.layer = None  # QgsVectorLayer - layer created by tool
        self.feat = None  # QgsFeature layer
        self.variableGeom = False  # True means a point layer will have to be used
        self.qgis_connect()
        self.populateAttributes()
        
        # Save data
        # save tables
        self.saved_xSectionTable = None
        self.saved_deckTable = None
        self.saved_pierTable = None
        # save spinboxes
        self.saved_xSectionRowCount = None
        self.saved_deckRowCount = None
        self.saved_pierRowCount = None
        # save input boxes
        self.saved_bridgeName = None
        self.saved_deckElevationBottom = None
        self.saved_deckThickness = None
        self.saved_handRailDepth = None
        self.saved_handRailFls = None
        self.saved_handRailBlockage = None
        self.saved_rbDrowned = None
        self.saved_pierNo = None
        self.saved_pierWidth = None
        self.saved_pierWidthLeft = None
        self.saved_pierGap = None
        self.saved_pierShape = None
        self.saved_zLineWidth = None
        self.saved_enforceInTerrain = None
        
        # Get empty TUFLOW folder
        self.tfsettings = TF_Settings()
        error, message = self.tfsettings.Load()
        if error:
            QMessageBox.information(self.iface.mainWindow(), "Error", "Error Loading Settings: " + message)
        basepath = self.tfsettings.combined.base_dir
        if basepath:
            path_split = basepath.split('\\')
            if path_split[-1].lower() == 'tuflow':
                basepath = '\\'.join(path_split[:-1])
            self.bridge.emptydir.setText(os.path.join(basepath, "TUFLOW", "model", "gis", "empty"))
        else:
            self.bridge.emptydir.setText("ERROR - Project not loaded")
		    
    def __del__(self):
        self.qgis_disconnect()

    def qgis_connect(self):
        """
        Set up signal connections.
        
        :return: void
        """
        
        if not self.connected:
            # canvas interactions
            # None
            # push buttons
            self.bridge.pbUpdate.clicked.connect(self.updatePlot)
            self.bridge.pbUpdatePierData.clicked.connect(self.updatePierTable)
            self.bridge.pbUpdateDeckData.clicked.connect(self.updateDeckTable)
            self.bridge.pbUseMapWindowSel.clicked.connect(self.getCurrSel)
            #self.bridge.pbDrawXsection.clicked.connect(self.useTempPolyline)
            self.bridge.pbClearXsection.clicked.connect(self.clearXsection)
            self.bridge.pbUpdateAttributes.clicked.connect(self.updateAttributes)
            self.bridge.pbCreateLayer.clicked.connect(lambda: createLayer(self))
            self.bridge.pbUpdateLayer.clicked.connect(lambda: updateLayer(self))
            self.bridge.pbIncrementLayer.clicked.connect(lambda: incrementLayer(self))
            # Spin boxes
            self.bridge.xSectionRowCount.valueChanged.connect(lambda: tableRowCountChanged(self, self.bridge.xSectionRowCount, self.bridge.xSectionTable))
            self.bridge.deckRowCount.valueChanged.connect(lambda: tableRowCountChanged(self, self.bridge.deckRowCount, self.bridge.deckTable))
            self.bridge.pierRowCount.valueChanged.connect(lambda: tableRowCountChanged(self, self.bridge.pierRowCount, self.bridge.pierTable))
            # Right Click (Context) Menus
            self.xSectionTableRowHeaders = self.bridge.xSectionTable.verticalHeader()
            self.pierTableRowHeaders = self.bridge.pierTable.verticalHeader()
            self.deckTableRowHeaders = self.bridge.deckTable.verticalHeader()
            self.bridge.plotWdg.setContextMenuPolicy(Qt.CustomContextMenu)
            self.xSectionTableRowHeaders.setContextMenuPolicy(Qt.CustomContextMenu)
            self.deckTableRowHeaders.setContextMenuPolicy(Qt.CustomContextMenu)
            self.pierTableRowHeaders.setContextMenuPolicy(Qt.CustomContextMenu)
            self.bridge.plotWdg.customContextMenuRequested.connect(lambda pos: plotterMenu(self, pos))
            self.xSectionTableRowHeaders.customContextMenuRequested.connect(lambda pos: xSectionTableMenu(self, pos))
            self.deckTableRowHeaders.customContextMenuRequested.connect(lambda pos: deckTableMenu(self, pos))
            self.pierTableRowHeaders.customContextMenuRequested.connect(lambda pos: pierTableMenu(self, pos))
            self.connected = True

    def qgis_disconnect(self):
        """
        Disconnect signal connections
        
        :return: void
        """

        if self.connected:
            # canvas interactions
            # None
            # push buttons
            self.bridge.pbUpdate.clicked.disconnect(self.updatePlot)
            self.bridge.pbUpdatePierData.clicked.disconnect(self.updatePierTable)
            self.bridge.pbUpdateDeckData.clicked.disconnect(self.updateDeckTable)
            self.bridge.pbUseMapWindowSel.clicked.disconnect(self.getCurrSel)
            #self.bridge.pbDrawXsection.clicked.disconnect(self.useTempPolyline)
            self.bridge.pbClearXsection.clicked.disconnect(self.clearXsection)
            self.bridge.pbUpdateAttributes.clicked.disconnect(self.updateAttributes)
            self.bridge.pbCreateLayer.clicked.disconnect()
            self.bridge.pbUpdateLayer.clicked.disconnect()
            self.bridge.pbIncrementLayer.clicked.disconnect()
            # Spin boxes
            self.bridge.xSectionRowCount.valueChanged.disconnect()
            self.bridge.deckRowCount.valueChanged.disconnect()
            self.bridge.pierRowCount.valueChanged.disconnect()
            # Right Click (Context) Menus
            self.bridge.plotWdg.customContextMenuRequested.disconnect()
            self.xSectionTableRowHeaders.customContextMenuRequested.disconnect()
            self.deckTableRowHeaders.customContextMenuRequested.disconnect()
            self.pierTableRowHeaders.customContextMenuRequested.disconnect()
            self.connected = False

    def populateAttributes(self):
        """
        Populate the attributes in the bridge editor from  feature
        
        :return:
        """

        if self.feat is None:
            lyr = self.canvas.currentLayer()
            if lyr is not None:
                if lyr.type() == 0:  # QgsVectorLayer
                    feat = lyr.selectedFeatures()
                    if len(feat) > 0:
                        self.bridge.invert.setText('{0}'.format(feat[0].attributes()[0]))
                        self.bridge.dz.setText('{0}'.format(feat[0].attributes()[1]))
                        self.bridge.shapeWidth.setText('{0}'.format(feat[0].attributes()[2]))
                        self.bridge.shapeOptions.setText('{0}'.format(feat[0].attributes()[3]) if feat[0].attributes()[3] != NULL else '')
                        self.bridge.layer1Block.setText('{0}'.format(feat[0].attributes()[4]))
                        self.bridge.layer1Obv.setText('{0}'.format(feat[0].attributes()[5]))
                        self.bridge.layer1Flc.setText('{0}'.format(feat[0].attributes()[6]))
                        self.bridge.layer2Depth.setText('{0}'.format(feat[0].attributes()[7]))
                        self.bridge.layer2Block.setText('{0}'.format(feat[0].attributes()[8]))
                        self.bridge.layer2Flc.setText('{0}'.format(feat[0].attributes()[9]))
                        self.bridge.layer3Depth.setText('{0}'.format(feat[0].attributes()[10]))
                        self.bridge.layer3Block.setText('{0}'.format(feat[0].attributes()[11]))
                        self.bridge.layer3Flc.setText('{0}'.format(feat[0].attributes()[12]))
                        self.bridge.comment.setText('{0}'.format(feat[0].attributes()[13]))

    def loadGui(self, gui):
        """
        Loads the GUI class
        
        :param gui: tuflowqgis_bridge_gui class object
        :return:
        """
        
        self.bridge = gui
    
    def saveData(self):
        """
        Save the GUI data into the editor object
        
        :return:
        """
        
        # save tables
        x = []
        y = []
        for i in range(self.bridge.xSectionTable.rowCount()):
            x.append(self.bridge.xSectionTable.item(i, 0).text())
            y.append(self.bridge.xSectionTable.item(i, 1).text())
        self.saved_xSectionTable = [x, y]
        x = []
        y = []
        for i in range(self.bridge.deckTable.rowCount()):
            x.append(self.bridge.deckTable.item(i, 0).text())
            y.append(self.bridge.deckTable.item(i, 1).text())
        self.saved_deckTable = [x, y]
        x = []
        for i in range(self.bridge.pierTable.rowCount()):
            x.append(self.bridge.pierTable.item(i, 0).text())
        self.saved_pierTable = x[:]
        # save spinboxes
        self.saved_xSectionRowCount = self.bridge.xSectionRowCount.value()
        self.saved_deckRowCount = self.bridge.deckRowCount.value()
        self.saved_pierRowCount = self.bridge.pierRowCount.value()
        # save input boxes
        self.saved_bridgeName = self.bridge.bridgeName.text()
        self.saved_deckElevationBottom = self.bridge.deckElevationBottom.value()
        self.saved_deckThickness = self.bridge.deckThickness.value()
        self.saved_handRailDepth = self.bridge.handRailDepth.value()
        self.saved_handRailFlc = self.bridge.handRailFlc.value()
        self.saved_handRailBlockage = self.bridge.handRailBlockage.value()
        self.saved_rbDrowned = self.bridge.rbDrowned.isChecked()
        self.saved_pierNo = self.bridge.pierNo.value()
        self.saved_pierWidth = self.bridge.pierWidth.value()
        self.saved_pierWidthLeft = self.bridge.pierWidthLeft.value()
        self.saved_pierGap = self.bridge.pierGap.value()
        self.saved_pierShape = self.bridge.pierShape.currentIndex()
        self.saved_zLineWidth = self.bridge.zLineWidth.value()
        self.saved_enforceInTerrain = self.bridge.enforceInTerrain.isChecked()
        
    def loadData(self):
        """
        loads the plot from a previous bridge editor class

        :return:
        """

        # save tables
        self.bridge.xSectionTable.setRowCount(len(self.saved_xSectionTable[0]))
        for i in range(self.bridge.xSectionTable.rowCount()):
            self.bridge.xSectionTable.setItem(i, 0, QTableWidgetItem(self.saved_xSectionTable[0][i]))
            self.bridge.xSectionTable.setItem(i, 1, QTableWidgetItem(self.saved_xSectionTable[1][i]))
        self.bridge.deckTable.setRowCount(len(self.saved_deckTable[0]))
        for i in range(self.bridge.deckTable.rowCount()):
            self.bridge.deckTable.setItem(i, 0, QTableWidgetItem(self.saved_deckTable[0][i]))
            self.bridge.deckTable.setItem(i, 1, QTableWidgetItem(self.saved_deckTable[1][i]))
        self.bridge.pierTable.setRowCount(len(self.saved_pierTable))
        for i in range(self.bridge.pierTable.rowCount()):
            self.bridge.pierTable.setItem(i, 0, QTableWidgetItem(self.saved_pierTable[i]))
        # save spinboxes
        self.bridge.xSectionRowCount.setValue(self.saved_xSectionRowCount)
        self.bridge.deckRowCount.setValue(self.saved_deckRowCount)
        self.bridge.pierRowCount.setValue(self.saved_pierRowCount)
        # save input boxes
        self.bridge.bridgeName.setText(self.saved_bridgeName)
        self.bridge.deckElevationBottom.setValue(self.saved_deckElevationBottom)
        self.bridge.deckThickness.setValue(self.saved_deckThickness)
        self.bridge.handRailDepth.setValue(self.saved_handRailDepth)
        self.bridge.handRailFlc.setValue(self.saved_handRailFlc)
        self.bridge.handRailBlockage.setValue(self.saved_handRailBlockage)
        self.bridge.rbDrowned.setChecked(self.saved_rbDrowned)
        self.bridge.pierNo.setValue(self.saved_pierNo)
        self.bridge.pierWidth.setValue(self.saved_pierWidth)
        self.bridge.pierWidthLeft.setValue(self.saved_pierWidthLeft)
        self.bridge.pierGap.setValue(self.saved_pierGap)
        self.bridge.pierShape.setCurrentIndex(self.saved_pierShape)
        self.bridge.zLineWidth.setValue(self.saved_zLineWidth)
        self.bridge.enforceInTerrain.setChecked(self.saved_enforceInTerrain)
        
        self.qgis_connect()
        self.updatePlot()
    
    def getCurrSel(self):
        """
        Get Current Selection
        
        :return:
        """
        
        # Get current selection
        lyr = self.iface.mapCanvas().currentLayer()  # QgsVectorLayer
        feat = lyr.selectedFeatures()  # list [QgsFeature]
        self.extractXSection(lyr, feat)
        
    
    def extractXSection(self, lyr, feat):
        """
        Extracts chainage and elevation data from selected DEM and Feature
        
        :return: list self.xSectionOffset
        :return: list self.xSectionElev
        """
        
        # Check that selected layer is a polyline
        if lyr is not None:
            if lyr.geometryType() != 1:
                self.bridge.statusLog.insertItem(0, 'Error: Layer is not a polyline type')
                self.bridge.statusLabel.setText('Status: Error')
                return
            else:
                self.bridge.statusLabel.setText('Status: Successful')
        # Check number of features selected
        if len(feat) == 0:
            self.bridge.statusLog.insertItem(0, 'Error: No Features Selected')
            self.bridge.statusLabel.setText('Status: Error')
            return
        if len(feat) > 1:
            self.bridge.statusLog.insertItem(0, 'Warning: More than one feature selected - using first selection in {0}'.format(lyr.name()))
            self.bridge.statusLabel.setText('Status: Warning')
        else:
            #self.statusLog.insertItem(0, 'Message: Draping line in {0}'.format(lyr.name()))
            self.bridge.statusLabel.setText('Status: Successful')
        feat = feat[0]  # QgsFeature
        # Get DEM for draping
        dem = tuflowqgis_find_layer(self.bridge.demComboBox.currentText())  # QgsRasterLayer
        if dem is None:
            self.bridge.statusLog.insertItem(0, 'Error: No DEM selected')
            self.bridge.statusLabel.setText('Status: Error')
            return
        else:
            demCellSize = max(dem.rasterUnitsPerPixelX(), dem.rasterUnitsPerPixelY())
        # create points for dem value extraction and get DEM value
        point, chainage = lineToPoints(feat, demCellSize)
        self.xSectionOffset = []
        self.xSectionElev = []
        for i, p in enumerate(point):
            self.xSectionOffset.append(chainage[i])
            self.xSectionElev.append(getRasterValue(p, dem))
        # Update X Section table and plot with values
        self.updateXsectionTable()
        self.updatePlot()
    
    def clearXsection(self):
        """
        resets the plot back to start
        
        :return:
        """
        
        self.canvas.scene().removeItem(self.rubberBand)  # Remove previous temp layer
        self.bridge.labels = []
        self.xSectionElev = []
        self.xSectionOffset = []
        self.deckPatch = []
        self.pierPatches = []
        self.bridge.subplot.cla()  # clear axis
        self.feat = None
        # create curve
        self.bridge.manageMatplotlibAxe(self.bridge.subplot)
        label = "test"
        x = numpy.linspace(-numpy.pi, numpy.pi, 201)
        y = numpy.sin(x)
        a, = self.bridge.subplot.plot(x, y)
        self.bridge.artists.append(a)
        self.bridge.labels.append(label)
        self.bridge.subplot.hold(True)
        #self.fig.tight_layout()
        self.bridge.plotWdg.draw()
        # clear tables
        self.bridge.xSectionTable.setRowCount(0)
        self.bridge.deckTable.setRowCount(0)
        self.bridge.pierTable.setRowCount(0)
        # clear spinboxes
        self.bridge.xSectionRowCount.setValue(0)
        self.bridge.deckRowCount.setValue(0)
        self.bridge.pierRowCount.setValue(0)
        # clear input boxes
        self.bridge.bridgeName.setText('')
        self.bridge.deckElevationBottom.setValue(0)
        self.bridge.deckThickness.setValue(0)
        self.bridge.handRailDepth.setValue(0)
        self.bridge.handRailFlc.setValue(0)
        self.bridge.handRailBlockage.setValue(0)
        self.bridge.rbDrowned.setChecked(True)
        self.bridge.pierNo.setValue(0)
        self.bridge.pierWidth.setValue(0)
        self.bridge.pierWidthLeft.setValue(0)
        self.bridge.pierGap.setValue(0)
        self.bridge.pierShape.setCurrentIndex(0)
        self.bridge.zLineWidth.setValue(0)
        self.bridge.enforceInTerrain.setChecked(False)
        # clear attributes
        self.bridge.invert.setText('')
        self.bridge.dz.setText('')
        self.bridge.shapeWidth.setText('')
        self.bridge.shapeOptions.setText('')
        self.bridge.layer1Obv.setText('')
        self.bridge.layer1Block.setText('')
        self.bridge.layer1Flc.setText('')
        self.bridge.layer2Depth.setText('')
        self.bridge.layer2Block.setText('')
        self.bridge.layer2Flc.setText('')
        self.bridge.layer3Depth.setText('')
        self.bridge.layer3Block.setText('')
        self.bridge.layer3Flc.setText('')
        self.bridge.comment.setText('')
        self.bridge.label_44.setText('')
        self.bridge.label_35.setText('')
        self.bridge.label_36.setText('')
        self.bridge.label_37.setText('')

    def createMemoryLayerFromTempLayer(self):
        """
        Creates a QgsFeature from the QgsPoint vertices in the temp layer
        
        :return:
        """
        
        self.feat = QgsFeature()
        self.feat.setGeometry(QgsGeometry.fromPolyline(self.points))
        self.extractXSection(None, [self.feat])
    
    def useTempPolyline(self):
        """
        Creates a graphic polyline that can be drawn on the map canvas
        
        :return: void
        """
        
        self.clearXsection()
        self.canvas.scene().removeItem(self.rubberBand)  # Remove previous temp layer
        self.rubberBand = QgsRubberBand(self.iface.mapCanvas(), False)  # setup rubberband class for drawing
        self.rubberBand.setWidth(2)
        self.rubberBand.setColor(QtGui.QColor(Qt.red))
        self.tempPolyline = canvasEvent(self.iface, self.canvas)  # setup maptool for custom canvas signals
        self.canvas.setMapTool(self.tempPolyline)
        self.points = []
        self.rubberBand.setToGeometry(QgsGeometry.fromPolyline(self.points), None)
        mouseTrackConnect(self)  # start the tuflowqgis_bridge_rubberband
    
    def updateXsectionTable(self):
        """
        Update table widget
        
        :param tableWidget: QTableWidget to be updated
        :return: void updated table widget with data
        """

        self.bridge.xSectionTable.setRowCount(len(self.xSectionOffset))
        self.bridge.xSectionTable.setItem(0, 0, QTableWidgetItem('test'))
        for i, value in enumerate(self.xSectionOffset):
            self.bridge.xSectionTable.setItem(i, 0, QTableWidgetItem(str(value)))
            self.bridge.xSectionTable.setItem(i, 1, QTableWidgetItem(str(self.xSectionElev[i])))
        # update spinbox
        self.bridge.xSectionRowCount.setValue(self.bridge.xSectionTable.rowCount())

    def updateXsectionData(self):
        """
        Update data based on the data in the table
        
        :return: list self.xSectionOffset
        :return: list self.xSectionElev
        """
        
        self.xSectionOffset = []
        self.xSectionElev = []
        for i in range(self.bridge.xSectionTable.rowCount()):
            self.xSectionOffset.append(float(self.bridge.xSectionTable.item(i, 0).text()))
            self.xSectionElev.append(float(self.bridge.xSectionTable.item(i, 1).text()))
            
    def updatePierTable(self):
        """
        Updates the pier table widget based on the input parameters
        
        :return: void updated table widget with data
        """

        # Check if cross section data is present
        if not self.xSectionOffset:
            return
        self.pierOffset = []
        # Set up QTableWidget
        self.bridge.pierTable.setRowCount(self.bridge.pierNo.value())
        # Populate values and column headers
        self.pierRowHeaders = []
        for i in range(1, self.bridge.pierNo.value() + 1):
            self.pierRowHeaders.append('Pier {0}'.format(i))
            if i == 1:
                offset = self.bridge.pierWidthLeft.value() + self.bridge.pierWidth.value() / 2
            else:
                offset += self.bridge.pierWidth.value() + self.bridge.pierGap.value()
            self.pierOffset.append(offset)
        self.bridge.pierTable.setVerticalHeaderLabels(self.pierRowHeaders)
        for i, pier in enumerate(self.pierOffset):
            self.bridge.pierTable.setItem(i, 0, QTableWidgetItem(str(pier)))
        # update spinbox
        self.bridge.pierRowCount.setValue(self.bridge.pierTable.rowCount())
        
        self.updatePlot()

    def createPierPatches(self):
        """
        Creates a list of patches to be used to create matplotlib patches

        :return: void updates self.pierPatches
        """
        
        if self.bridge.pierTable.item(0, 0) is None:
            self.bridge.statusLog.insertItem(0, 'Warning: No Piers Defined in Table')
            self.bridge.statusLabel.setText('Status: Warning')
            return
        self.pierPatches = []
        for i in range(self.bridge.pierTable.rowCount()):
            x = []
            y = []
            x1 = float(self.bridge.pierTable.item(i, 0).text()) - self.bridge.pierWidth.value() / 2
            x2 = float(self.bridge.pierTable.item(i, 0).text()) + self.bridge.pierWidth.value() / 2
            y1a = self.getGroundAtX(x1)
            y1b = self.getGroundAtX(x2)
            y2a = self.interpolateVLookupObvert(x1)
            y2b = self.interpolateVLookupObvert(x2)
            if y2a <= y1a or y2b <= y1b:
                self.bridge.statusLog.insertItem(0, 'Error: Bridge deck level is lower than ground')
                self.bridge.statusLabel.setText('Status: Error')
                return
            else:
                self.bridge.statusLabel.setText('Status: Successful')
            x.append(x1)
            y.append(y1a)
            iStart = None
            iEnd = None
            for i, offset in enumerate(self.xSectionOffset):
                if i == 0:
                    offsetPrev = offset
                    iPrev = i
                else:
                    if x1 < offset and x1 >= offsetPrev:
                        offsetStart = offsetPrev
                        iStart = iPrev
                    if x2 <= offset and x2 > offsetPrev:
                        offsetEnd = offset
                        iEnd = i
                    if iStart is not None and iEnd is not None:
                        if iEnd - iStart > 1:
                            for j in range(iStart + 1, iEnd):
                                x.append(self.xSectionOffset[j])
                                y.append(self.xSectionElev[j])
                        break
                    offsetPrev = offset
                    iPrev = i
            x.append(x2)
            x.append(x2)
            x.append(x1)
            y.append(y1b)
            y.append(y2b)
            y.append(y2a)
            patch = list(zip(x, y))
            self.pierPatches.append(patch)
        self.bridge.statusLabel.setText('Status: Successful')
            
    def updateDeckTable(self):
        """
        Updates the deck table widget based on the input parameters
        
        :return:
        """

        # Set up table
        self.bridge.deckTable.setRowCount(2)
        # Update parameters
        if self.xSectionElev[0] <= self.bridge.deckElevationBottom.value():
            xmin = self.xSectionOffset[0]
        else:
            xmin = self.getXatElevation(self.bridge.deckElevationBottom.value(), 1)
        if self.xSectionElev[-1] <= self.bridge.deckElevationBottom.value():
            xmax = self.xSectionOffset[-1]
        else:
            xmax = self.getXatElevation(self.bridge.deckElevationBottom.value(), -1)
        self.bridge.deckTable.setItem(0, 0, QTableWidgetItem(str(xmin)))
        self.bridge.deckTable.setItem(1, 0, QTableWidgetItem(str(xmax)))
        self.bridge.deckTable.setItem(0, 1, QTableWidgetItem(str(self.bridge.deckElevationBottom.value())))
        self.bridge.deckTable.setItem(1, 1, QTableWidgetItem(str(self.bridge.deckElevationBottom.value())))
        
        self.updatePlot()
        
    def updateDeckOffset(self):
        """
        Updates the first and last offset value in the deck table to be where the deck meets the Xsection
        
        :return:
        """
        
        if self.bridge.deckTable.item(0, 0) is not None:
            # first value
            elevation = float(self.bridge.deckTable.item(0, 1).text())
            if elevation >= self.xSectionElev[0]:
                offset = self.xSectionOffset[0]
            else:
                offset = self.getXatElevation(elevation, 1)
            self.bridge.deckTable.setItem(0, 0, QTableWidgetItem(str(offset)))
            # last value
            lastRow = self.bridge.deckTable.rowCount() - 1
            elevation = float(self.bridge.deckTable.item(lastRow, 1).text())
            if elevation >= self.xSectionElev[-1]:
                offset = self.xSectionOffset[-1]
            else:
                offset = self.getXatElevation(elevation, -1)
            self.bridge.deckTable.setItem(lastRow, 0, QTableWidgetItem(str(offset)))
            self.updateObverts()
        # Update spinbox
        self.bridge.deckRowCount.setValue(self.bridge.deckTable.rowCount())
            
    def interpolateVLookupObvert(self, x):
        """
        A vertical lookup from the deck table. Will interpolate between values
        
        :param x: float- offset for lookup
        :return: float- elevation value
        """
        
        
        for i in range(self.bridge.deckTable.rowCount()):
            offset = float(self.bridge.deckTable.item(i, 0).text())
            y = float(self.bridge.deckTable.item(i, 1).text())
            if i == 0:
                if offset == x:
                    return y
                offsetPrev = offset
                yPrev = y
            else:
                if offset == x:
                    return y
                if offsetPrev < x and offset > x:
                    return self.interpolate(x, offsetPrev, offset, yPrev, y)
                offsetPrev = offset
                yPrev = y
        return None
    
    def updateObverts(self):
        """
        Updates the obverts list to align with the xSectionOffset list. Will interpolate if bridge deck is not flat
        
        :return:
        """

        self.obverts = []
        lastRow = self.bridge.deckTable.rowCount() - 1
        for offset in self.xSectionOffset:
            if offset == float(self.bridge.deckTable.item(0, 0).text()):  # equal to the first entry in the deck table
                self.obverts.append(float(self.bridge.deckTable.item(0, 1).text()))
            elif offset == float(self.bridge.deckTable.item(lastRow, 0).text()):  # equal to the last entry in the deck table
                self.obverts.append(float(self.bridge.deckTable.item(lastRow, 1).text()))
            elif offset > float(self.bridge.deckTable.item(0, 0).text()) and offset < float(self.bridge.deckTable.item(lastRow, 0).text()):  # in between first and last entry- interpolate
                self.obverts.append(self.interpolateVLookupObvert(offset))
            elif offset > float(self.bridge.deckTable.item(lastRow, 0).text()):  # after last entry
                self.obverts.append(float(self.bridge.deckTable.item(lastRow, 1).text()))
            else:  # before first entry
                self.obverts.append(float(self.bridge.deckTable.item(0, 1).text()))
        
    def createDeckPatch(self):
        """
        Creates a matplotlib patch for plotting the bridge deck
        
        :return: void updates self.deckPatch
        """

        if self.bridge.deckTable.item(0, 0) is None:
            self.bridge.statusLog.insertItem(0, 'Warning: No Piers Defined in Table')
            self.bridge.statusLabel.setText('Status: Warning')
            return
        x = []
        y = []
        # Get patch values between upper and lower deck cords on left hand side
        y1 = float(self.bridge.deckTable.item(0, 1).text())  # lower cord on left hand deck limit
        y2 = y1 + self.bridge.deckThickness.value()  # upper cord on left hand deck limit
        x1 = float(self.bridge.deckTable.item(0, 0).text())  # x value of lower cord on left hand deck limit
        x2 = self.getXatElevation(y2, 1)  # x value of upper cord on left hand deck limit
        x2 = x1 if x2 > x1 else x2  # x2 cannot be greater than x1
        x.append(x2)
        y.append(y2)
        iStart = None
        iEnd = None
        # Follow xsection for path between upper and lower cords
        for i, offset in enumerate(self.xSectionOffset):
            if i == 0:
                offsetPrev = offset
                iPrev = i
            else:
                if x2 < offset and x2 >= offsetPrev:
                    offsetStart = offsetPrev
                    iStart = iPrev
                if x1 <= offset and x1 > offsetPrev:
                    offsetEnd = offset
                    iEnd = i
                if iStart is not None and iEnd is not None:
                    if iEnd - iStart > 1:
                        for j in range(iStart + 1, iEnd):
                            x.append(self.xSectionOffset[j])
                            y.append(self.xSectionElev[j])
                    break
                offsetPrev = offset
                iPrev = i
        x.append(x1)
        y.append(y1)
        # get patch values along deck bottom
        iMax = self.bridge.deckTable.rowCount() - 1
        underDeck = False
        start = False
        for i, xsElev in enumerate(self.xSectionElev):
            obvert = self.obverts[i]
            offset = self.xSectionOffset[i]
            if i == 0:
                xsElevPrev = xsElev
                iPrev = i
                obvertPrev = obvert
                offsetPrev = offset
                if xsElev < obvert:
                    underDeck = True
                    start = True
                    continue
            elif offset >= float(self.bridge.deckTable.item(iMax, 0).text()):
                start = False
            elif xsElev < obvert and xsElevPrev > obvertPrev:
                underDeck = True
                start = True
                x.append(self.interpolate(obvert, xsElevPrev, xsElev, offsetPrev, offset))
                y.append(obvert)
            elif xsElev > obvert and xsElevPrev < obvertPrev:
                underDeck = False
                x.append(self.interpolate(obvert, xsElevPrev, xsElev, offsetPrev, offset))
                y.append(obvert)
            elif xsElev == obvert and xsElevPrev > obvertPrev:
                underDeck = True
                start = True
                x.append(offset)
                y.append(obvert)
                xsElevPrev = xsElev
                iPrev = i
                obvertPrev = obvert
                offsetPrev = offset
                continue
            if underDeck and start:
                x.append(offset)
                y.append(obvert)
            elif start:
                x.append(offset)
                y.append(xsElev)
            xsElevPrev = xsElev
            iPrev = i
            obvertPrev = obvert
            offsetPrev = offset
        # Get patch values between upper and lower deck cords on right hand side
        y3 = float(self.bridge.deckTable.item(iMax, 1).text())  # lower cord on right hand deck limit
        y4 = y3 + self.bridge.deckThickness.value()  # upper cord on right hand deck limit
        x3 = float(self.bridge.deckTable.item(iMax, 0).text())  # x value of lower cord on right hand deck limit
        x4 = self.getXatElevation(y4, -1)  # x value of upper cord on right hand deck limit
        x4 = x3 if x4 < x3 else x4  # x4 cannot be less than x3
        x.append(x3)
        y.append(y3)
        iStart = None
        iEnd = None
        for i, offset in enumerate(self.xSectionOffset):
            if i == 0:
                offsetPrev = offset
                iPrev = i
            else:
                if x3 < offset and x3 >= offsetPrev:
                    offsetStart = offsetPrev
                    iStart = iPrev
                if x4 <= offset and x4 > offsetPrev:
                    offsetEnd = offset
                    iEnd = i + 1
                if iStart is not None and iEnd is not None:
                    if iEnd - iStart > 1:
                        for j in range(iStart + 1, iEnd):
                            x.append(self.xSectionOffset[j])
                            y.append(self.xSectionElev[j])
                    break
                offsetPrev = offset
                iPrev = i
        x.append(x4)
        y.append(y4)
        # get patch values along deck top
        underDeck = False
        start = False
        for i in range(len(self.xSectionElev) - 1, 0, -1):
            xsElev = self.xSectionElev[i]
            obvert = self.obverts[i] + self.bridge.deckThickness.value()
            offset = self.xSectionOffset[i]
            if i == len(self.xSectionElev) - 1:
                xsElevPrev = xsElev
                iPrev = i
                obvertPrev = obvert
                offsetPrev = offset
                if xsElev < obvert:
                    underDeck = True
                    start = True
                    continue
            elif offset <= float(self.bridge.deckTable.item(0, 0).text()):
                start = False
            elif xsElev < obvert and xsElevPrev > obvertPrev:
                underDeck = True
                start = True
                x.append(self.interpolate(obvert, xsElevPrev, xsElev, offsetPrev, offset))
                y.append(obvert)
            elif xsElev > obvert and xsElevPrev < obvertPrev:
                underDeck = False
                x.append(self.interpolate(obvert, xsElevPrev, xsElev, offsetPrev, offset))
                y.append(obvert)
            elif xsElev == obvert and xsElevPrev > obvertPrev:
                underDeck = True
                start = True
                x.append(offset)
                y.append(obvert)
                xsElevPrev = xsElev
                iPrev = i
                obvertPrev = obvert
                offsetPrev = offset
                continue
            if underDeck and start:
                x.append(offset)
                y.append(obvert)
            elif start:
                x.append(offset)
                y.append(xsElev)
            xsElevPrev = xsElev
            iPrev = i
            obvertPrev = obvert
            offsetPrev = offset
        self.deckPatch = list(zip(x, y))
    
    def getGroundAtX(self, x):
        """
        Get the ground elevation at a given offset
        
        :param x: offset value
        :return: float elevation value
        """
        
        # Check if cross section data is present
        if not self.xSectionOffset:
            return
        # Get values on either side
        for i, offset in enumerate(self.xSectionOffset):
            if i == 0:
                if x == offset:
                    self.bridge.statusLabel.setText('Status: Successful')
                    return self.xSectionElev[i]
                xPrev = offset
                iPrev = i
            else:
                if x == offset:
                    self.bridge.statusLabel.setText('Status: Successful')
                    return self.xSectionElev[i]
                elif x > xPrev and x < offset:
                    self.bridge.statusLabel.setText('Status: Successful')
                    return self.interpolate(x, xPrev, offset, self.xSectionElev[iPrev], self.xSectionElev[i])
                else:
                    xPrev = offset
                    iPrev = i
        self.bridge.statusLog.insertItem(0, 'Error: Unable to find ground level at pier offset')
        self.bridge.statusLabel.setText('Status: Error')
        return min(self.xSectionElev)
    
    def getXatElevation(self, z, direction):
        """
        Get the X value at a given elevation. Will return the first value it finds.
        
        :param z: elevation value
        :param direction: 1 or -1 (1 will start the search from the start, -1 will start the search from the end)
        :return: float offset value
        """
        
        if not self.xSectionOffset:
            return
        if direction > 0:
            for i, elev in enumerate(self.xSectionElev):
                if i == 0:
                    if z == elev:
                        return self.xSectionOffset[i]
                    elevPrev = elev
                    iPrev = i
                else:
                    if z == elev:
                        return self.xSectionOffset[i]
                    elif z > elev and z < elevPrev:
                        return self.interpolate(z, elev, elevPrev, self.xSectionOffset[i], self.xSectionOffset[iPrev])
                    else:
                        elevPrev = elev
                        iPrev = i
            return min(self.xSectionOffset)
        else:
            for i, elev in enumerate(reversed(self.xSectionElev)):
               l = len(self.xSectionElev) - 1
               if i == 0:
                   if z == elev:
                       return self.xSectionOffset[l - i]
                   elevPrev = elev
                   iPrev = i
               else:
                   if z == elev:
                       return self.xSectionOffset[l - i]
                   elif z > elev and z < elevPrev:
                       return self.interpolate(z, elev, elevPrev, self.xSectionOffset[l - i], self.xSectionOffset[l - iPrev])
                   else:
                       elevPrev = elev
                       iPrev = i
            return max(self.xSectionOffset)
                    
    def interpolate(self, a, b, c, d, e):
        """
        Linear interpolation
        
        :param a: known mid point
        :param b: known lower value
        :param c: known upper value
        :param d: unknown lower value
        :param e: unknown upper value
        :return: float
        """
        
        a = float(a)
        b = float(b)
        c = float(c)
        d = float(d)
        e = float(e)
        
        return (e - d) / (c - b) * (a - b) + d
    
    def calculateFlowArea(self):
        """
        Calculates the flow area underneath the deck
        
        :return:
        """
        
        # check a deck exists
        if self.bridge.deckTable.item(0, 0) is None:
            self.bridge.statusLog.insertItem(0, 'Warning: Unable to calculate energy loss without bridge deck')
            self.bridge.statusLabel.setText('Status: Warning')
            return
        # calculate area
        underDeck = False
        self.area = 0
        for i, xsElev in enumerate(self.xSectionElev):
            obvert = self.obverts[i]
            offset = self.xSectionOffset[i]
            if i == 0:
                xsElevPrev = xsElev
                iPrev = i
                obvertPrev = obvert
                offsetPrev = offset
                if xsElev < obvert:
                    underDeck = True
                    continue
            elif xsElev < obvert and xsElevPrev > obvertPrev:
                underDeck = True
                offsetPrev = self.interpolate(obvert, xsElevPrev, xsElev, offsetPrev, offset)
                xsElevPrev = obvert
            elif xsElev > obvert and xsElevPrev < obvertPrev:
                underDeck = False
                offset = self.interpolate(obvert, xsElevPrev, xsElev, offsetPrev, offset)
                xsElev = obvert
                x = offset - offsetPrev
                y1 = obvertPrev - xsElevPrev
                y2 = obvert - xsElev
                y = (y1 + y2) / 2.0
                self.area += x * y
            elif xsElev == obvert and xsElevPrev > obvertPrev:
                underDeck = True
                xsElevPrev = xsElev
                iPrev = i
                obvertPrev = obvert
                offsetPrev = offset
                continue
            if underDeck:
                x = offset - offsetPrev
                y1 = obvertPrev - xsElevPrev
                y2 = obvert - xsElev
                y = (y1 + y2) / 2.0
                self.area += x * y
            xsElevPrev = xsElev
            iPrev = i
            obvertPrev = obvert
            offsetPrev = offset
        self.bridge.statusLabel.setText('Status: Successful')
        
    def calculatePierArea(self):
        """
        Calculates the area obstructed by the piers
        
        :return:
        """
        
        self.pierArea = 0
        if self.bridge.pierTable.item(0, 0) is None:
            return
        else:
            for i, pier in enumerate(self.pierPatches):
                xEnd = float(self.bridge.pierTable.item(i, 0).text()) + self.bridge.pierWidth.value() / 2
                area = 0
                end = False
                for j, v in enumerate(pier):
                    x = v[0]
                    yGround = v[1]  # ground
                    yObvert = self.interpolateVLookupObvert(x)  # obvert
                    if j == 0:
                        xPrev = x
                        yGroundPrev = yGround
                        yObvertPrev = yObvert
                    else:
                        dx = x - xPrev
                        dy1 = yObvert - yGround
                        dy2 = yObvertPrev - yGroundPrev
                        area += dx * (dy1 + dy2) / 2.0
                        xPrev = x
                        yGroundPrev = yGround
                        yObvertPrev = yObvert
                        if x == xEnd:
                            break
                self.pierArea += area
        
    def updatePlot(self):
        """
        Update the plot window
        
        :return: void
        """

        self.updateXsectionData()
        self.updateDeckOffset()
        # Set up default limits
        ymax = -99999
        # Reset and clear plot
        self.bridge.subplot.cla()
        self.bridge.artists = []
        self.bridge.labels = []
        # Update X Section
        a, = self.bridge.subplot.plot(self.xSectionOffset, self.xSectionElev)
        label = 'X-Section'
        ymax = max(ymax, max(self.xSectionElev))
        self.bridge.labels.append(label)
        self.bridge.artists.append(a)
        self.bridge.subplot.hold(True)
        # Update Pier Data
        self.createPierPatches()
        for pier in self.pierPatches:
            for v in pier:
                ymax = max(ymax, v[1])
            patch = Polygon(pier, facecolor='0.9', edgecolor='0.5')
            self.bridge.subplot.add_patch(patch)
        # Update Deck Data
        self.createDeckPatch()
        for v in self.deckPatch:
            ymax = max(ymax, v[1])
        if self.deckPatch:
            patch = Polygon(self.deckPatch, facecolor='0.9', edgecolor='0.5')
            self.bridge.subplot.add_patch(patch)
        # Draw
        self.bridge.manageMatplotlibAxe(self.bridge.subplot)
        yTicks = self.bridge.subplot.get_yticks()
        yInc = yTicks[1] - yTicks[0]
        self.bridge.subplot.set_ybound(upper=ymax + yInc)
        self.bridge.fig.tight_layout()
        self.bridge.plotWdg.draw()
    
    def updateAttributes(self):
        """
        Update the text fields on the OUTPUT tab
        
        :return:
        """
        
        # Invert
        if self.bridge.enforceInTerrain.isChecked():
            self.bridge.invert.setText('0')
            self.bridge.label_44.setText('Enforcing Bridge Invert- Points layer will be created')
            self.variableGeom = True
        else:
            self.bridge.invert.setText('99999')
            self.bridge.label_44.setText('Adopting existing Zpts as bridge invert')
        # dZ
        self.bridge.dz.setText('0')
        # Shape Width
        self.bridge.shapeWidth.setText('{0:.1f}'.format(float(self.bridge.zLineWidth.text())))
        if self.bridge.pierTable.item(0, 0) is None:
            self.bridge.statusLog.insertItem(0, 'Warning: No Piers Defined in Table')
            self.bridge.statusLabel.setText('Status: Warning')
        else:
            self.bridge.layer1Obv.setText(self.bridge.deckTable.item(0, 1).text())
        # pier values
        self.calculateFlowArea()
        self.calculatePierArea()
        self.bridge.layer1Block.setText('{0:.1f}'.format(self.pierArea / self.area * 100))
        self.bridge.layer1Flc.setText('{0:.2f}'.format(lookupPierLoss(int(self.bridge.pierShape.currentText()), self.pierArea / self.area)))
        # elevation values
        self.bridge.layer1Obv.setText(str(self.bridge.deckElevationBottom.value()))
        self.bridge.layer2Depth.setText(str(self.bridge.deckThickness.value()))
        self.bridge.layer3Depth.setText(str(self.bridge.handRailDepth.value()))
        self.bridge.label_35.setText('Constant level')
        self.bridge.label_36.setText('Constant level')
        self.bridge.label_37.setText('Constant level')
        if self.variableGeom:
            self.bridge.layer1Obv.setText('0')
            self.bridge.layer2Depth.setText('0')
            self.bridge.layer3Depth.setText('0')
            self.bridge.label_35.setText('Variable elevation- Points layer will be created')
            self.bridge.label_36.setText('Variable elevation- Points layer will be created')
            self.bridge.label_37.setText('Variable elevation- Points layer will be created')
        else:
            for i in range(self.bridge.deckTable.rowCount()):
                elev = float(self.bridge.deckTable.item(i, 1).text())
                if i == 0:
                    elevPrev = elev
                else:
                    if elev != elevPrev:
                        self.bridge.layer1Obv.setText('0')
                        self.bridge.layer2Depth.setText('0')
                        self.bridge.layer3Depth.setText('0')
                        self.bridge.label_35.setText('Variable elevation- Points layer will be created')
                        self.bridge.label_36.setText('Variable elevation- Points layer will be created')
                        self.bridge.label_37.setText('Variable elevation- Points layer will be created')
                        self.variableGeom = True
                        break
        # other blockage and FLC values
        self.bridge.layer2Block.setText('100')
        self.bridge.layer3Block.setText(str(self.bridge.handRailBlockage.value()))
        self.bridge.layer3Flc.setText(str(self.bridge.handRailFlc.value()))
        if self.bridge.rbDrowned.isChecked():
            self.bridge.layer2Flc.setText('0.5')
        else:
            self.bridge.layer2Flc.setText('1.56')
        # comment
        self.bridge.comment.setText(self.bridge.bridgeName.text())
