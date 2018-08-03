from PyQt4 import QtGui
from qgis.gui import *
import sys
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.patches import Patch
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.patches import Polygon
from tuflow.tuflowqgis_settings import TF_Settings
from tuflow.tuflowqgis_library import lineToPoints, getRasterValue
from tuflowqgis_bridge_context_menus import *
from tuflow.tuflowqgis_bridge.tuflowqgis_bridge_rubberband import *
from tuflowqgis_bridge_layer_edit import *
from tuflow.canvas_event import canvasEvent
from tuflow.Pier_Losses import lookupPierLoss
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/forms")
# Debug using PyCharm
sys.path.append(r'C:\Program Files\JetBrains\PyCharm 2018.1\debug-eggs')
sys.path.append(r'C:\Program Files\JetBrains\PyCharm 2018.1\helpers\pydev')

#class bridgeEditor(QDockWidget, Ui_tuflowqgis_BridgeEditor):
class bridgeEditor():

    def __init__(self, gui, iface, **kwargs):
        self.updated = False
        self.gui = gui  # bridge gui class
        self.iface = iface  # QgsInterface
        self.canvas = self.iface.mapCanvas()  # QgsMapCanvas
        self.connected = False  # signal connections
        self.cursorTrackingConnected = False  # temp polyline signals
        self.xSectionOffset = []  # XSection offset values
        self.xSectionElev = []
        self.pierOffset = []  # list of pier offsets [[pier 1 offset], [pier 2 offset]]
        self.pierRowHeaders = []  # list of pier row names
        self.pierPatches = []  # patches used for plotting piers
        self.deckPatch = []  # patch used for plotting deck
        self.rubberBand = QgsRubberBand(self.iface.mapCanvas(), False)  # temporary polyline
        self.tempPolyline = None
        self.points = []  # QgsPoints used for temporary created layer
        self.obverts = []  # list of obvert values aligning with xSectionOffset list
        self.area = 0  # area under bridge deck
        self.pierArea = 0  # area of piers in waterway
        self.layer = None  # QgsVectorLayer - layer created by tool
        self.feat = None  # QgsFeature layer, used for storing temporary data only
        self.feature = None  # also QgsFeature Layer, confusing but this one is used when new layer is created
        self.variableGeom = False  # True means a point layer will have to be used
        
        # set up variables for connections
        self.xSectionTableRowHeaders = self.gui.xSectionTable.verticalHeader()
        self.pierTableRowHeaders = self.gui.pierTable.verticalHeader()
        self.deckTableRowHeaders = self.gui.deckTable.verticalHeader()
        self.gui.plotWdg.setContextMenuPolicy(Qt.CustomContextMenu)
        self.xSectionTableRowHeaders.setContextMenuPolicy(Qt.CustomContextMenu)
        self.deckTableRowHeaders.setContextMenuPolicy(Qt.CustomContextMenu)
        self.pierTableRowHeaders.setContextMenuPolicy(Qt.CustomContextMenu)
        
        #self.qgis_connect()
        self.populateAttributes()
        
        # Save data
        # save tables
        self.saved_object = False
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
        self.saved_handRailFlc = None
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
            self.gui.emptydir.setText(os.path.join(basepath, "TUFLOW", "model", "gis", "empty"))
        else:
            self.gui.emptydir.setText("ERROR - Project not loaded")
		    
    def __del__(self):
        self.qgis_disconnect()  # ensure signals are disconnected

    def qgis_connect(self):
        """
        Connect signal connections
        
        :return:
        """
        
        if not self.connected:
            # currently not used but reserved in case of future use
            self.connected = True
    
    def qgis_disconnect(self):
        """
        Disconnect signal connections
        
        :return: void
        """

        if self.connected:
            # currently not used but reserved in case of future use
            self.connected = False
        if self.gui is not None:
            if self.gui.buttonsConnected:
                # push buttons
                self.gui.pbUpdate.clicked.disconnect()
                self.gui.pbUpdatePierData.clicked.disconnect()
                self.gui.pbUpdateDeckData.clicked.disconnect()
                self.gui.pbUseMapWindowSel.clicked.disconnect()
                self.gui.pbClearXsection.clicked.disconnect()
                self.gui.pbUpdateAttributes.clicked.disconnect()
                self.gui.pbCreateLayer.clicked.disconnect()
                self.gui.pbUpdateLayer.clicked.disconnect()
                self.gui.pbIncrementLayer.clicked.disconnect()
                # Spin boxes
                self.gui.xSectionRowCount.valueChanged.disconnect()
                self.gui.deckRowCount.valueChanged.disconnect()
                self.gui.pierRowCount.valueChanged.disconnect()
                # Right Click (Context) Menus
                self.xSectionTableRowHeaders.customContextMenuRequested.disconnect()
                self.deckTableRowHeaders.customContextMenuRequested.disconnect()
                self.pierTableRowHeaders.customContextMenuRequested.disconnect()
                self.gui.plotWdg.customContextMenuRequested.disconnect()
                # Other connections to tell the object that there has been an update
                self.gui.bridgeName.textChanged.disconnect()
                self.gui.deckElevationBottom.valueChanged.disconnect()
                self.gui.deckThickness.valueChanged.disconnect()
                self.gui.handRailDepth.valueChanged.disconnect()
                self.gui.handRailFlc.valueChanged.disconnect()
                self.gui.handRailBlockage.valueChanged.disconnect()
                self.gui.rbDrowned.toggled.disconnect()
                self.gui.pierNo.valueChanged.disconnect()
                self.gui.pierWidth.valueChanged.disconnect()
                self.gui.pierWidthLeft.valueChanged.disconnect()
                self.gui.pierGap.valueChanged.disconnect()
                self.gui.pierShape.currentIndexChanged.disconnect()
                self.gui.zLineWidth.valueChanged.disconnect()
                self.gui.enforceInTerrain.stateChanged.disconnect()
                
                self.gui.buttonsConnected = False

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
                        self.gui.invert.setText('{0}'.format(feat[0].attributes()[0]))
                        self.gui.dz.setText('{0}'.format(feat[0].attributes()[1]))
                        self.gui.shapeWidth.setText('{0}'.format(feat[0].attributes()[2]))
                        self.gui.shapeOptions.setText('{0}'.format(feat[0].attributes()[3]) if feat[0].attributes()[3] != NULL else '')
                        self.gui.layer1Block.setText('{0}'.format(feat[0].attributes()[4]))
                        self.gui.layer1Obv.setText('{0}'.format(feat[0].attributes()[5]))
                        self.gui.layer1Flc.setText('{0}'.format(feat[0].attributes()[6]))
                        self.gui.layer2Depth.setText('{0}'.format(feat[0].attributes()[7]))
                        self.gui.layer2Block.setText('{0}'.format(feat[0].attributes()[8]))
                        self.gui.layer2Flc.setText('{0}'.format(feat[0].attributes()[9]))
                        self.gui.layer3Depth.setText('{0}'.format(feat[0].attributes()[10]))
                        self.gui.layer3Block.setText('{0}'.format(feat[0].attributes()[11]))
                        self.gui.layer3Flc.setText('{0}'.format(feat[0].attributes()[12]))
                        self.gui.comment.setText('{0}'.format(feat[0].attributes()[13]))

    def loadGui(self, gui):
        """
        Loads the GUI class
        
        :param gui: tuflowqgis_bridge_gui class object
        :return:
        """
        
        self.gui = gui
    
    def saveData(self):
        """
        Save the GUI data into the editor object
        
        :return:
        """
        
        # save tables
        x = []
        y = []
        for i in range(self.gui.xSectionTable.rowCount()):
            x.append(self.gui.xSectionTable.item(i, 0).text())
            y.append(self.gui.xSectionTable.item(i, 1).text())
        self.saved_xSectionTable = [x, y]
        x = []
        y = []
        for i in range(self.gui.deckTable.rowCount()):
            x.append(self.gui.deckTable.item(i, 0).text())
            y.append(self.gui.deckTable.item(i, 1).text())
        self.saved_deckTable = [x, y]
        x = []
        for i in range(self.gui.pierTable.rowCount()):
            x.append(self.gui.pierTable.item(i, 0).text())
        self.saved_pierTable = x[:]
        # save spinboxes
        self.saved_xSectionRowCount = self.gui.xSectionRowCount.value()
        self.saved_deckRowCount = self.gui.deckRowCount.value()
        self.saved_pierRowCount = self.gui.pierRowCount.value()
        # save input boxes
        self.saved_bridgeName = self.gui.bridgeName.text()
        self.saved_deckElevationBottom = self.gui.deckElevationBottom.value()
        self.saved_deckThickness = self.gui.deckThickness.value()
        self.saved_handRailDepth = self.gui.handRailDepth.value()
        self.saved_handRailFlc = self.gui.handRailFlc.value()
        self.saved_handRailBlockage = self.gui.handRailBlockage.value()
        self.saved_rbDrowned = self.gui.rbDrowned.isChecked()
        self.saved_pierNo = self.gui.pierNo.value()
        self.saved_pierWidth = self.gui.pierWidth.value()
        self.saved_pierWidthLeft = self.gui.pierWidthLeft.value()
        self.saved_pierGap = self.gui.pierGap.value()
        self.saved_pierShape = self.gui.pierShape.currentIndex()
        self.saved_zLineWidth = self.gui.zLineWidth.value()
        self.saved_enforceInTerrain = self.gui.enforceInTerrain.isChecked()
        
        self.saved_object = True
        
    def loadData(self):
        """
        loads the plot from a previous bridge editor class

        :return:
        """
        
        if self.saved_object:
            # save tables
            self.gui.xSectionTable.setRowCount(len(self.saved_xSectionTable[0]))
            for i in range(self.gui.xSectionTable.rowCount()):
                self.gui.xSectionTable.setItem(i, 0, QTableWidgetItem(self.saved_xSectionTable[0][i]))
                self.gui.xSectionTable.setItem(i, 1, QTableWidgetItem(self.saved_xSectionTable[1][i]))
            self.gui.deckTable.setRowCount(len(self.saved_deckTable[0]))
            for i in range(self.gui.deckTable.rowCount()):
                self.gui.deckTable.setItem(i, 0, QTableWidgetItem(self.saved_deckTable[0][i]))
                self.gui.deckTable.setItem(i, 1, QTableWidgetItem(self.saved_deckTable[1][i]))
            self.gui.pierTable.setRowCount(len(self.saved_pierTable))
            for i in range(self.gui.pierTable.rowCount()):
                self.gui.pierTable.setItem(i, 0, QTableWidgetItem(self.saved_pierTable[i]))
            # save spinboxes
            self.gui.xSectionRowCount.setValue(self.saved_xSectionRowCount)
            self.gui.deckRowCount.setValue(self.saved_deckRowCount)
            self.gui.pierRowCount.setValue(self.saved_pierRowCount)
            # save input boxes
            self.gui.bridgeName.setText(self.saved_bridgeName)
            self.gui.deckElevationBottom.setValue(self.saved_deckElevationBottom)
            self.gui.deckThickness.setValue(self.saved_deckThickness)
            self.gui.handRailDepth.setValue(self.saved_handRailDepth)
            self.gui.handRailFlc.setValue(self.saved_handRailFlc)
            self.gui.handRailBlockage.setValue(self.saved_handRailBlockage)
            self.gui.rbDrowned.setChecked(self.saved_rbDrowned)
            self.gui.pierNo.setValue(self.saved_pierNo)
            self.gui.pierWidth.setValue(self.saved_pierWidth)
            self.gui.pierWidthLeft.setValue(self.saved_pierWidthLeft)
            self.gui.pierGap.setValue(self.saved_pierGap)
            self.gui.pierShape.setCurrentIndex(self.saved_pierShape)
            self.gui.zLineWidth.setValue(self.saved_zLineWidth)
            self.gui.enforceInTerrain.setChecked(self.saved_enforceInTerrain)
    
            self.qgis_connect()
            self.updatePlot()
    
    def setUpdated(self):
        """
        Sets the updated status to true
        
        :return:
        """
        
        self.updated = True
    
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
                self.gui.statusLog.insertItem(0, 'Error: Layer is not a polyline type')
                self.gui.statusLabel.setText('Status: Error')
                return
            else:
                self.gui.statusLabel.setText('Status: Successful')
        # Check number of features selected
        if len(feat) == 0:
            self.gui.statusLog.insertItem(0, 'Error: No Features Selected')
            self.gui.statusLabel.setText('Status: Error')
            return
        if len(feat) > 1:
            self.gui.statusLog.insertItem(0, 'Warning: More than one feature selected - using first selection in {0}'.format(lyr.name()))
            self.gui.statusLabel.setText('Status: Warning')
        else:
            #self.statusLog.insertItem(0, 'Message: Draping line in {0}'.format(lyr.name()))
            self.gui.statusLabel.setText('Status: Successful')
        feat = feat[0]  # QgsFeature
        # Get DEM for draping
        dem = tuflowqgis_find_layer(self.gui.demComboBox.currentText())  # QgsRasterLayer
        if dem is None:
            self.gui.statusLog.insertItem(0, 'Error: No DEM selected')
            self.gui.statusLabel.setText('Status: Error')
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
        self.gui.labels = []
        self.xSectionElev = []
        self.xSectionOffset = []
        self.deckPatch = []
        self.pierPatches = []
        self.gui.subplot.cla()  # clear axis
        self.feat = None
        # create curve
        self.gui.manageMatplotlibAxe(self.gui.subplot)
        label = "test"
        x = numpy.linspace(-numpy.pi, numpy.pi, 201)
        y = numpy.sin(x)
        a, = self.gui.subplot.plot(x, y)
        self.gui.artists.append(a)
        self.gui.labels.append(label)
        self.gui.subplot.hold(True)
        #self.fig.tight_layout()
        self.gui.plotWdg.draw()
        # clear tables
        self.gui.xSectionTable.setRowCount(0)
        self.gui.deckTable.setRowCount(0)
        self.gui.pierTable.setRowCount(0)
        # clear spinboxes
        self.gui.xSectionRowCount.setValue(0)
        self.gui.deckRowCount.setValue(0)
        self.gui.pierRowCount.setValue(0)
        # clear input boxes
        self.gui.bridgeName.setText('')
        self.gui.deckElevationBottom.setValue(0)
        self.gui.deckThickness.setValue(0)
        self.gui.handRailDepth.setValue(0)
        self.gui.handRailFlc.setValue(0)
        self.gui.handRailBlockage.setValue(0)
        self.gui.rbDrowned.setChecked(True)
        self.gui.pierNo.setValue(0)
        self.gui.pierWidth.setValue(0)
        self.gui.pierWidthLeft.setValue(0)
        self.gui.pierGap.setValue(0)
        self.gui.pierShape.setCurrentIndex(0)
        self.gui.zLineWidth.setValue(0)
        self.gui.enforceInTerrain.setChecked(False)
        # clear attributes
        self.gui.invert.setText('')
        self.gui.dz.setText('')
        self.gui.shapeWidth.setText('')
        self.gui.shapeOptions.setText('')
        self.gui.layer1Obv.setText('')
        self.gui.layer1Block.setText('')
        self.gui.layer1Flc.setText('')
        self.gui.layer2Depth.setText('')
        self.gui.layer2Block.setText('')
        self.gui.layer2Flc.setText('')
        self.gui.layer3Depth.setText('')
        self.gui.layer3Block.setText('')
        self.gui.layer3Flc.setText('')
        self.gui.comment.setText('')
        self.gui.label_44.setText('')
        self.gui.label_35.setText('')
        self.gui.label_36.setText('')
        self.gui.label_37.setText('')

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

        self.gui.xSectionTable.setRowCount(len(self.xSectionOffset))
        self.gui.xSectionTable.setItem(0, 0, QTableWidgetItem('test'))
        for i, value in enumerate(self.xSectionOffset):
            self.gui.xSectionTable.setItem(i, 0, QTableWidgetItem(str(value)))
            self.gui.xSectionTable.setItem(i, 1, QTableWidgetItem(str(self.xSectionElev[i])))
        # update spinbox
        self.gui.xSectionRowCount.setValue(self.gui.xSectionTable.rowCount())

    def updateXsectionData(self):
        """
        Update data based on the data in the table
        
        :return: list self.xSectionOffset
        :return: list self.xSectionElev
        """

        self.xSectionOffset = []
        self.xSectionElev = []
        for i in range(self.gui.xSectionTable.rowCount()):
            if self.gui.xSectionTable.item(i, 0).text() != '' and self.gui.xSectionTable.item(i, 1).text() != '':  # otherwise skip
                if self.gui.xSectionTable.item(i, 0).text() != '':
                    try:
                        self.xSectionOffset.append(float(self.gui.xSectionTable.item(i, 0).text()))
                    except:
                        QMessage.critical(self.iface.mainWindow(), 'Error', 'Table entry must be a number (Offset, row {0})'.format(i + 1))
                if self.gui.xSectionTable.item(i, 1).text() != '':
                    try:
                        self.xSectionElev.append(float(self.gui.xSectionTable.item(i, 1).text()))
                    except:
                        QMessage.critical(self.iface.mainWindow(), 'Error', 'Table entry must be a number (Elevation, row {0})'.format(i + 1))
            
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
        self.gui.pierTable.setRowCount(self.gui.pierNo.value())
        # Populate values and column headers
        self.pierRowHeaders = []
        for i in range(1, self.gui.pierNo.value() + 1):
            self.pierRowHeaders.append('Pier {0}'.format(i))
            if i == 1:
                offset = self.gui.pierWidthLeft.value() + self.gui.pierWidth.value() / 2
            else:
                offset += self.gui.pierWidth.value() + self.gui.pierGap.value()
            self.pierOffset.append(offset)
        self.gui.pierTable.setVerticalHeaderLabels(self.pierRowHeaders)
        for i, pier in enumerate(self.pierOffset):
            self.gui.pierTable.setItem(i, 0, QTableWidgetItem(str(pier)))
        # update spinbox
        self.gui.pierRowCount.setValue(self.gui.pierTable.rowCount())
        
        self.updated = True
        self.updatePlot()

    def createPierPatches(self):
        """
        Creates a list of patches to be used to create matplotlib patches

        :return: void updates self.pierPatches
        """
        
        if self.gui.pierTable.item(0, 0) is None:
            self.gui.statusLog.insertItem(0, 'Warning: No Piers Defined in Table')
            self.gui.statusLabel.setText('Status: Warning')
            return
        self.pierPatches = []
        for i in range(self.gui.pierTable.rowCount()):
            x = []
            y = []
            x1 = float(self.gui.pierTable.item(i, 0).text()) - self.gui.pierWidth.value() / 2
            x2 = float(self.gui.pierTable.item(i, 0).text()) + self.gui.pierWidth.value() / 2
            y1a = self.getGroundAtX(x1)
            y1b = self.getGroundAtX(x2)
            y2a = self.interpolateVLookupObvert(x1)
            y2b = self.interpolateVLookupObvert(x2)
            if y2a <= y1a or y2b <= y1b:
                self.gui.statusLog.insertItem(0, 'Error: Bridge deck level is lower than ground')
                self.gui.statusLabel.setText('Status: Error')
                return
            else:
                self.gui.statusLabel.setText('Status: Successful')
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
        self.gui.statusLabel.setText('Status: Successful')
            
    def updateDeckTable(self):
        """
        Updates the deck table widget based on the input parameters
        
        :return:
        """

        # Set up table
        self.gui.deckTable.setRowCount(2)
        # Update parameters
        if self.xSectionElev[0] <= self.gui.deckElevationBottom.value():
            xmin = self.xSectionOffset[0]
        else:
            xmin = self.getXatElevation(self.gui.deckElevationBottom.value(), 1)
        if self.xSectionElev[-1] <= self.gui.deckElevationBottom.value():
            xmax = self.xSectionOffset[-1]
        else:
            xmax = self.getXatElevation(self.gui.deckElevationBottom.value(), -1)
        self.gui.deckTable.setItem(0, 0, QTableWidgetItem(str(xmin)))
        self.gui.deckTable.setItem(1, 0, QTableWidgetItem(str(xmax)))
        self.gui.deckTable.setItem(0, 1, QTableWidgetItem(str(self.gui.deckElevationBottom.value())))
        self.gui.deckTable.setItem(1, 1, QTableWidgetItem(str(self.gui.deckElevationBottom.value())))
        
        self.updated = True
        self.updatePlot()
        
    def updateDeckOffset(self):
        """
        Updates the first and last offset value in the deck table to be where the deck meets the Xsection
        
        :return:
        """
        
        if self.gui.deckTable.item(0, 0) is not None:
            # first value
            elevation = float(self.gui.deckTable.item(0, 1).text())
            if elevation >= self.xSectionElev[0]:
                offset = self.xSectionOffset[0]
            else:
                offset = self.getXatElevation(elevation, 1)
            self.gui.deckTable.setItem(0, 0, QTableWidgetItem(str(offset)))
            # last value
            lastRow = self.gui.deckTable.rowCount() - 1
            elevation = float(self.gui.deckTable.item(lastRow, 1).text())
            if elevation >= self.xSectionElev[-1]:
                offset = self.xSectionOffset[-1]
            else:
                offset = self.getXatElevation(elevation, -1)
            self.gui.deckTable.setItem(lastRow, 0, QTableWidgetItem(str(offset)))
            self.updateObverts()
        # Update spinbox
        self.gui.deckRowCount.setValue(self.gui.deckTable.rowCount())
            
    def interpolateVLookupObvert(self, x):
        """
        A vertical lookup from the deck table. Will interpolate between values
        
        :param x: float- offset for lookup
        :return: float- elevation value
        """
        
        
        for i in range(self.gui.deckTable.rowCount()):
            offset = float(self.gui.deckTable.item(i, 0).text())
            y = float(self.gui.deckTable.item(i, 1).text())
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
        lastRow = self.gui.deckTable.rowCount() - 1
        for offset in self.xSectionOffset:
            if offset == float(self.gui.deckTable.item(0, 0).text()):  # equal to the first entry in the deck table
                self.obverts.append(float(self.gui.deckTable.item(0, 1).text()))
            elif offset == float(self.gui.deckTable.item(lastRow, 0).text()):  # equal to the last entry in the deck table
                self.obverts.append(float(self.gui.deckTable.item(lastRow, 1).text()))
            elif offset > float(self.gui.deckTable.item(0, 0).text()) and offset < float(self.gui.deckTable.item(lastRow, 0).text()):  # in between first and last entry- interpolate
                self.obverts.append(self.interpolateVLookupObvert(offset))
            elif offset > float(self.gui.deckTable.item(lastRow, 0).text()):  # after last entry
                self.obverts.append(float(self.gui.deckTable.item(lastRow, 1).text()))
            else:  # before first entry
                self.obverts.append(float(self.gui.deckTable.item(0, 1).text()))
        
    def createDeckPatch(self):
        """
        Creates a matplotlib patch for plotting the bridge deck
        
        :return: void updates self.deckPatch
        """

        if self.gui.deckTable.item(0, 0) is None:
            self.gui.statusLog.insertItem(0, 'Warning: No Piers Defined in Table')
            self.gui.statusLabel.setText('Status: Warning')
            return
        x = []
        y = []
        # Get patch values between upper and lower deck cords on left hand side
        y1 = float(self.gui.deckTable.item(0, 1).text())  # lower cord on left hand deck limit
        y2 = y1 + self.gui.deckThickness.value()  # upper cord on left hand deck limit
        x1 = float(self.gui.deckTable.item(0, 0).text())  # x value of lower cord on left hand deck limit
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
        iMax = self.gui.deckTable.rowCount() - 1
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
            elif offset >= float(self.gui.deckTable.item(iMax, 0).text()):
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
        y3 = float(self.gui.deckTable.item(iMax, 1).text())  # lower cord on right hand deck limit
        y4 = y3 + self.gui.deckThickness.value()  # upper cord on right hand deck limit
        x3 = float(self.gui.deckTable.item(iMax, 0).text())  # x value of lower cord on right hand deck limit
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
            obvert = self.obverts[i] + self.gui.deckThickness.value()
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
            elif offset <= float(self.gui.deckTable.item(0, 0).text()):
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
                    self.gui.statusLabel.setText('Status: Successful')
                    return self.xSectionElev[i]
                xPrev = offset
                iPrev = i
            else:
                if x == offset:
                    self.gui.statusLabel.setText('Status: Successful')
                    return self.xSectionElev[i]
                elif x > xPrev and x < offset:
                    self.gui.statusLabel.setText('Status: Successful')
                    return self.interpolate(x, xPrev, offset, self.xSectionElev[iPrev], self.xSectionElev[i])
                else:
                    xPrev = offset
                    iPrev = i
        self.gui.statusLog.insertItem(0, 'Error: Unable to find ground level at pier offset')
        self.gui.statusLabel.setText('Status: Error')
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
        if self.gui.deckTable.item(0, 0) is None:
            self.gui.statusLog.insertItem(0, 'Warning: Unable to calculate energy loss without bridge deck')
            self.gui.statusLabel.setText('Status: Warning')
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
        self.gui.statusLabel.setText('Status: Successful')
        
    def calculatePierArea(self):
        """
        Calculates the area obstructed by the piers
        
        :return:
        """
        
        self.pierArea = 0
        if self.gui.pierTable.item(0, 0) is None:
            return
        else:
            for i, pier in enumerate(self.pierPatches):
                xEnd = float(self.gui.pierTable.item(i, 0).text()) + self.gui.pierWidth.value() / 2
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
        self.gui.subplot.cla()
        self.gui.artists = []
        self.gui.labels = []
        # Update X Section
        a, = self.gui.subplot.plot(self.xSectionOffset, self.xSectionElev)
        label = 'X-Section'
        ymax = max(ymax, max(self.xSectionElev))
        self.gui.labels.append(label)
        self.gui.artists.append(a)
        self.gui.subplot.hold(True)
        # Update Pier Data
        self.createPierPatches()
        for pier in self.pierPatches:
            for v in pier:
                ymax = max(ymax, v[1])
            patch = Polygon(pier, facecolor='0.9', edgecolor='0.5')
            self.gui.subplot.add_patch(patch)
        # Update Deck Data
        self.createDeckPatch()
        for v in self.deckPatch:
            ymax = max(ymax, v[1])
        if self.deckPatch:
            patch = Polygon(self.deckPatch, facecolor='0.9', edgecolor='0.5')
            self.gui.subplot.add_patch(patch)
        # Draw
        self.gui.manageMatplotlibAxe(self.gui.subplot)
        yTicks = self.gui.subplot.get_yticks()
        yInc = yTicks[1] - yTicks[0]
        self.gui.subplot.set_ybound(upper=ymax + yInc)
        self.gui.fig.tight_layout()
        self.gui.plotWdg.draw()
    
    def updateAttributes(self):
        """
        Update the text fields on the OUTPUT tab
        
        :return:
        """
        
        # Invert
        if self.gui.enforceInTerrain.isChecked():
            self.gui.invert.setText('0')
            self.gui.label_44.setText('Enforcing Bridge Invert- Points layer will be created')
            self.variableGeom = True
        else:
            self.gui.invert.setText('99999')
            self.gui.label_44.setText('Adopting existing Zpts as bridge invert')
        # dZ
        self.gui.dz.setText('0')
        # Shape Width
        self.gui.shapeWidth.setText('{0:.1f}'.format(float(self.gui.zLineWidth.text())))
        if self.gui.pierTable.item(0, 0) is None:
            self.gui.statusLog.insertItem(0, 'Warning: No Piers Defined in Table')
            self.gui.statusLabel.setText('Status: Warning')
        else:
            self.gui.layer1Obv.setText(self.gui.deckTable.item(0, 1).text())
        # pier values
        self.calculateFlowArea()
        self.calculatePierArea()
        self.gui.layer1Block.setText('{0:.1f}'.format(self.pierArea / self.area * 100))
        self.gui.layer1Flc.setText('{0:.2f}'.format(lookupPierLoss(int(self.gui.pierShape.currentText()), self.pierArea / self.area)))
        # elevation values
        self.gui.layer1Obv.setText(str(self.gui.deckElevationBottom.value()))
        self.gui.layer2Depth.setText(str(self.gui.deckThickness.value()))
        self.gui.layer3Depth.setText(str(self.gui.handRailDepth.value()))
        self.gui.label_35.setText('Constant level')
        self.gui.label_36.setText('Constant level')
        self.gui.label_37.setText('Constant level')
        if self.variableGeom:
            self.gui.layer1Obv.setText('0')
            self.gui.layer2Depth.setText('0')
            self.gui.layer3Depth.setText('0')
            self.gui.label_35.setText('Variable elevation- Points layer will be created')
            self.gui.label_36.setText('Variable elevation- Points layer will be created')
            self.gui.label_37.setText('Variable elevation- Points layer will be created')
        else:
            for i in range(self.gui.deckTable.rowCount()):
                elev = float(self.gui.deckTable.item(i, 1).text())
                if i == 0:
                    elevPrev = elev
                else:
                    if elev != elevPrev:
                        self.gui.layer1Obv.setText('0')
                        self.gui.layer2Depth.setText('0')
                        self.gui.layer3Depth.setText('0')
                        self.gui.label_35.setText('Variable elevation- Points layer will be created')
                        self.gui.label_36.setText('Variable elevation- Points layer will be created')
                        self.gui.label_37.setText('Variable elevation- Points layer will be created')
                        self.variableGeom = True
                        break
        # other blockage and FLC values
        self.gui.layer2Block.setText('100')
        self.gui.layer3Block.setText(str(self.gui.handRailBlockage.value()))
        self.gui.layer3Flc.setText(str(self.gui.handRailFlc.value()))
        if self.gui.rbDrowned.isChecked():
            self.gui.layer2Flc.setText('0.5')
        else:
            self.gui.layer2Flc.setText('1.56')
        # comment
        self.gui.comment.setText(self.gui.bridgeName.text())
