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
import numpy
from tuflowqgis_settings import TF_Settings
from tuflowqgis_library import lineToPoints, getRasterValue, findAllRasterLyrs, tuflowqgis_find_layer, tuflowqgis_import_empty_tf
from tuflowqgis_dialog import tuflowqgis_increment_dialog
from canvas_event import canvasEvent
from Pier_Losses import lookupPierLoss
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/forms")
#from ui_tuflowqgis_bridge_editor import Ui_tuflowqgis_BridgeEditor
# Debug using PyCharm
sys.path.append(r'C:\Program Files\JetBrains\PyCharm 2018.1\debug-eggs')
sys.path.append(r'C:\Program Files\JetBrains\PyCharm 2018.1\helpers\pydev')

#class bridgeEditor(QDockWidget, Ui_tuflowqgis_BridgeEditor):
class bridgeEditor():

    def __init__(self, bridge, iface, **kwargs):
        #QDockWidget.__init__(self)
        #self.wdg = Ui_tuflowqgis_BridgeEditor.__init__(self)
        #self.setupUi(self)
        self.updated = False
        self.bridge = bridge
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
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
        self.initialisePlot()
        self.qgis_connect()
        #self.populateDems()
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
            
        # Get loaded bridge editor data
        if 'loaded_data' in kwargs.keys():
            self.loadedBridge = kwargs['loaded_data']
            #self.loadData()
        else:
            self.loadedBridge = None
		    
    def __del__(self):
        self.qgis_disconnect()

    def qgis_connect(self):
        """
        Set up signal connections.
        
        :return: void
        """
        
        if not self.connected:
            # canvas interactions
            #self.canvas.layersChanged.connect(self.populateDems)
            # push buttons
            self.bridge.pbUpdate.clicked.connect(self.updatePlot)
            self.bridge.pbUpdatePierData.clicked.connect(self.updatePierTable)
            self.bridge.pbUpdateDeckData.clicked.connect(self.updateDeckTable)
            self.bridge.pbUseMapWindowSel.clicked.connect(self.getCurrSel)
            self.bridge.pbDrawXsection.clicked.connect(self.useTempPolyline)
            self.bridge.pbClearXsection.clicked.connect(self.clearXsection)
            self.bridge.pbUpdateAttributes.clicked.connect(self.updateAttributes)
            self.bridge.pbCreateLayer.clicked.connect(self.createLayer)
            self.bridge.pbUpdateLayer.clicked.connect(self.updateLayer)
            self.bridge.pbIncrementLayer.clicked.connect(self.incrementLayer)
            # Spin boxes
            self.bridge.xSectionRowCount.valueChanged.connect(lambda: self.tableRowCountChanged(self.bridge.xSectionRowCount, self.bridge.xSectionTable))
            self.bridge.deckRowCount.valueChanged.connect(lambda: self.tableRowCountChanged(self.bridge.deckRowCount, self.bridge.deckTable))
            self.bridge.pierRowCount.valueChanged.connect(lambda: self.tableRowCountChanged(self.bridge.pierRowCount, self.bridge.pierTable))
            # Right Click (Context) Menus
            self.plotWdg.setContextMenuPolicy(Qt.CustomContextMenu)
            self.plotWdg.customContextMenuRequested.connect(self.showMenu)
            self.xSectionTableRowHeaders = self.bridge.xSectionTable.verticalHeader()
            self.pierTableRowHeaders = self.bridge.pierTable.verticalHeader()
            self.deckTableRowHeaders = self.bridge.deckTable.verticalHeader()
            self.xSectionTableRowHeaders.setContextMenuPolicy(Qt.CustomContextMenu)
            self.deckTableRowHeaders.setContextMenuPolicy(Qt.CustomContextMenu)
            self.pierTableRowHeaders.setContextMenuPolicy(Qt.CustomContextMenu)
            self.xSectionTableRowHeaders.customContextMenuRequested.connect(self.showXsectionTableMenu)
            self.deckTableRowHeaders.customContextMenuRequested.connect(self.showDeckTableMenu)
            self.pierTableRowHeaders.customContextMenuRequested.connect(self.showPierTableMenu)
            self.connected = True

    def qgis_disconnect(self):
        """
        Disconnect signal connections
        
        :return: void
        """

        if self.connected:
            # canvas interactions
            #self.canvas.layersChanged.disconnect(self.populateDems)
            # push buttons
            self.bridge.pbUpdate.clicked.disconnect(self.updatePlot)
            self.bridge.pbUpdatePierData.clicked.disconnect(self.updatePierTable)
            self.bridge.pbUpdateDeckData.clicked.disconnect(self.updateDeckTable)
            self.bridge.pbUseMapWindowSel.clicked.disconnect(self.getCurrSel)
            self.bridge.pbDrawXsection.clicked.disconnect(self.useTempPolyline)
            self.bridge.pbClearXsection.clicked.disconnect(self.clearXsection)
            self.bridge.pbUpdateAttributes.clicked.disconnect(self.updateAttributes)
            self.bridge.pbCreateLayer.clicked.connect(self.createLayer)
            self.bridge.pbUpdateLayer.clicked.connect(self.updateLayer)
            self.bridge.pbIncrementLayer.clicked.connect(self.incrementLayer)
            # Spin boxes
            self.bridge.xSectionRowCount.valueChanged.disconnect(lambda: self.tableRowCountChanged(self.bridge.xSectionRowCount, self.bridge.xSectionTable))
            self.bridge.deckRowCount.valueChanged.disconnect(lambda: self.tableRowCountChanged(self.bridge.deckRowCount, self.bridge.deckTable))
            self.bridge.pierRowCount.valueChanged.disconnect(lambda: self.tableRowCountChanged(self.bridge.pierRowCount, self.bridge.pierTable))
            # Right Click (Context) Menus
            self.plotWdg.customContextMenuRequested.disconnect(self.showMenu)
            self.xSectionTableRowHeaders.customContextMenuRequested.disconnect(self.showXsectionTableMenu)
            self.deckTableRowHeaders.customContextMenuRequested.disconnect(self.showDeckTableMenu)
            self.pierTableRowHeaders.customContextMenuRequested.disconnect(self.showPierTableMenu)
            self.connected = False
            
    def initialisePlot(self):
        """
        Initialise matplotlib plotting
        
        :return: void matplotlib plot widget
        """
        
        # Initialise ui packing
        self.layout = self.bridge.frame_for_plot_2.layout()
        minsize = self.bridge.minimumSize()
        maxsize = self.bridge.maximumSize()
        self.bridge.setMinimumSize(minsize)
        self.bridge.setMaximumSize(maxsize)
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
        self.bridge.gridLayout_3.addWidget(self.plotWdg)
        if matplotlib.__version__ < 1.5:
            mpltoolbar = matplotlib.backends.backend_qt4agg.NavigationToolbar2QTAgg(self.plotWdg,
                                                                                    self.bridge.frame_for_toolbar)
        else:
            mpltoolbar = matplotlib.backends.backend_qt4agg.NavigationToolbar2QT(self.plotWdg, self.bridge.frame_for_toolbar)
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
        self.fig.tight_layout()
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

    def populateAttributes(self):
        """
        Populate the attributes in the bridge editor from  feature
        
        :return:
        """
        
        if self.feat is None:
            lyr = self.canvas.currentLayer()
            if lyr.type() == 0:  # QgsVectorLayer
                feat = lyr.selectedFeatures()
                if len(feat) > 0:
                    self.bridge.invert.setText('{0}'.format(feat[0].attributes()[0]))
                    self.bridge.dz.setText('{0}'.format(feat[0].attributes()[1]))
                    self.bridge.shapeWidth.setText('{0}'.format(feat[0].attributes()[2]))
                    self.bridge.shapeOptions.setText('{0}'.format(feat[0].attributes()[3]))
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

    def loadEditor(self, editor):
        self.bridge = editor
    
    def saveData(self):
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
        loads the plot from a previous bridge editor

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
    
    def getCurrSel(self):
        """
        Get Current Selection
        
        :return:
        """
        
        self.mouseTrackDisconnect()
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
        self.labels = []
        self.subplot.cla()  # clear axis
        self.feat = None
        # create curve
        self.manageMatplotlibAxe(self.subplot)
        label = "test"
        x = numpy.linspace(-numpy.pi, numpy.pi, 201)
        y = numpy.sin(x)
        a, = self.subplot.plot(x, y)
        self.artists.append(a)
        self.labels.append(label)
        self.subplot.hold(True)
        self.fig.tight_layout()
        self.plotWdg.draw()
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
        self.mouseTrackConnect()
        
    def moved(self, position):
        """
        Signal sent when cursor is moved on the map canvas
        
        :param position: dict event signal position
        :return: void
        """
        
        x = position['x']
        y = position['y']
        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        if self.points:
            try:  # QGIS 2
                if QGis.QGIS_VERSION >= 10900:
                    self.rubberBand.reset(QGis.Line)
                else:
                    self.rubberBand.reset(False)
            except:  # QGIS 3
                self.rubberBand.reset(QgsWkbTypes.LineGeometry)
            #self.points.pop()
            #self.points.append(point)
            self.rubberBand.setToGeometry(QgsGeometry.fromPolyline(self.points), None)
            self.rubberBand.addPoint(point)
    
    def leftClick(self, position):
        """
        Signal sent when canvas is left clicked
        
        :param position: dict event signal position
        :return: void
        """
        
        x = position['x']
        y = position['y']
        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        self.points.append(point)
        self.rubberBand.addPoint(point)
    
    def rightClick(self, position):
        """
        Signal sent when canvas is right clicked
        
        :param position: dict event signal position
        :return: void
        
        :param position:
        :return:
        """
        
        self.mouseTrackDisconnect()
        self.createMemoryLayerFromTempLayer()

    def escape(self, key):
        """
        Signal sent when a key is pressed in qgis. Will cancel the line if escape is pressed
        
        :param key: QKeyEvent
        :return:
        """
        
        #QMessageBox.information(self.iface.mainWindow(), "debug", "{0}".format(key.key()))
        if key.key() == 16777216:  # Escape key
            self.canvas.scene().removeItem(self.rubberBand)  # Remove previous temp layer
            self.mouseTrackDisconnect()
    
    def mouseTrackConnect(self):
        """
        Captures signals from the custom map tool
        
        :return:
        """
        
        if not self.cursorTrackingConnected:
            self.cursorTrackingConnected = True
            QApplication.setOverrideCursor(Qt.CrossCursor)
            self.tempPolyline.moved.connect(self.moved)
            self.tempPolyline.rightClicked.connect(self.rightClick)
            self.tempPolyline.leftClicked.connect(self.leftClick)
            self.canvas.keyPressed.connect(self.escape)

    def mouseTrackDisconnect(self):
        """
        Turn off capturing of the custom map tool
        
        :return:
        """
        
        if self.cursorTrackingConnected:
            self.cursorTrackingConnected = False
            QApplication.restoreOverrideCursor()
            self.tempPolyline.moved.disconnect(self.moved)
            self.tempPolyline.rightClicked.disconnect(self.rightClick)
            self.tempPolyline.leftClicked.disconnect(self.leftClick)
    
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

        self.mouseTrackDisconnect()
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

        self.mouseTrackDisconnect()
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

        self.mouseTrackDisconnect()
        self.updateDeckOffset()
        # Set up default limits
        ymax = -99999
        # Reset and clear plot
        self.subplot.cla()
        self.artists = []
        self.labels = []
        # Update X Section
        self.updateXsectionData()
        a, = self.subplot.plot(self.xSectionOffset, self.xSectionElev)
        label = 'X-Section'
        ymax = max(ymax, max(self.xSectionElev))
        self.labels.append(label)
        self.artists.append(a)
        self.subplot.hold(True)
        # Update Pier Data
        self.createPierPatches()
        for pier in self.pierPatches:
            for v in pier:
                ymax = max(ymax, v[1])
            patch = Polygon(pier, facecolor='0.9', edgecolor='0.5')
            self.subplot.add_patch(patch)
        # Update Deck Data
        self.createDeckPatch()
        for v in self.deckPatch:
            ymax = max(ymax, v[1])
        if self.deckPatch:
            patch = Polygon(self.deckPatch, facecolor='0.9', edgecolor='0.5')
            self.subplot.add_patch(patch)
        # Draw
        self.manageMatplotlibAxe(self.subplot)
        yTicks = self.subplot.get_yticks()
        yInc = yTicks[1] - yTicks[0]
        self.subplot.set_ybound(upper=ymax + yInc)
        self.fig.tight_layout()
        self.plotWdg.draw()

    def showPierTableMenu(self, pos):
        """
        Table right click menu
        
        :param pos: QPoint & pos
        :return:
        """
        
        menu = QMenu(self.bridge)
        insertRowBefore_action = QAction("Insert Row (before)", menu)
        insertRowAfter_action = QAction("Insert Row (after)", menu)
        deleteRow_action = QAction("Delete Row", menu)
        insertRowBefore_action.triggered.connect(lambda: self.insertRowBefore(self.bridge.pierTable))
        insertRowAfter_action.triggered.connect(lambda: self.insertRowAfter(self.bridge.pierTable))
        deleteRow_action.triggered.connect(lambda: self.deleteRow(self.bridge.pierTable))
        menu.addAction(insertRowBefore_action)
        menu.addAction(insertRowAfter_action)
        menu.addAction(deleteRow_action)
        menu.popup(self.bridge.pierTable.mapToGlobal(pos))
        
    def showDeckTableMenu(self, pos):
        """
        Table right click menu

        :param pos: QPoint & pos
        :return:
        """
        
        menu = QMenu(self.bridge)
        insertRowBefore_action = QAction("Insert Row (before)", menu)
        insertRowAfter_action = QAction("Insert Row (after)", menu)
        deleteRow_action = QAction("Delete Row", menu)
        insertRowBefore_action.triggered.connect(lambda: self.insertRowBefore(self.bridge.deckTable))
        insertRowAfter_action.triggered.connect(lambda: self.insertRowAfter(self.bridge.deckTable))
        deleteRow_action.triggered.connect(lambda: self.deleteRow(self.bridge.deckTable))
        menu.addAction(insertRowBefore_action)
        menu.addAction(insertRowAfter_action)
        menu.addAction(deleteRow_action)
        menu.popup(self.bridge.pierTable.mapToGlobal(pos))
        
    def showXsectionTableMenu(self, pos):
        """
        Table right click menu

        :param pos: QPoint & pos
        :return:
        """
        
        menu = QMenu(self.bridge)
        insertRowBefore_action = QAction("Insert Row (before)", menu)
        insertRowAfter_action = QAction("Insert Row (after)", menu)
        deleteRow_action = QAction("Delete Row", menu)
        insertRowBefore_action.triggered.connect(lambda: self.insertRowBefore(self.bridge.xSectionTable))
        insertRowAfter_action.triggered.connect(lambda: self.insertRowAfter(self.bridge.xSectionTable))
        deleteRow_action.triggered.connect(lambda: self.deleteRow(self.bridge.xSectionTable))
        menu.addAction(insertRowBefore_action)
        menu.addAction(insertRowAfter_action)
        menu.addAction(deleteRow_action)
        menu.popup(self.bridge.pierTable.mapToGlobal(pos))
        
    def insertRowBefore(self, table):
        """
        Insert row in QTableWidget before the current selection
        
        :param table: QTableWidget
        :return:
        """
        
        # Get selected row
        currentRow = table.currentRow()
        if currentRow is None:
            self.bridge.statusLog.insertItem(0, 'Error: No row selected')
            self.bridge.statusLabel.setText('Status: Error')
            return
        # store data
        x = []  # list of strings
        y = []  # list of strings
        for i in range(table.rowCount()):
            x.append(table.item(i, 0).text())
            if table != self.bridge.pierTable:
                y.append(table.item(i, 1).text())
        # add row and populate data
        table.setRowCount(len(x) + 1)
        if table == self.bridge.pierTable:  # populate pier numbering
            headers = ['Pier {0}'.format(p) for p in range(1, table.rowCount() + 1)]
            table.setVerticalHeaderLabels(headers)
        for i in range(table.rowCount()):
            if i < currentRow:
                table.setItem(i, 0, QTableWidgetItem(x[i]))
                if table != self.bridge.pierTable:
                    table.setItem(i, 1, QTableWidgetItem(y[i]))
            elif i == currentRow:
                table.setItem(i, 0, QTableWidgetItem('0'))
                if table != self.bridge.pierTable:
                    table.setItem(i, 1, QTableWidgetItem('0'))
            elif i > currentRow:
                table.setItem(i, 0, QTableWidgetItem(x[i - 1]))
                if table != self.bridge.pierTable:
                   table.setItem(i, 1, QTableWidgetItem(y[i - 1]))
        # update class properties for XSection data
        if table == self.bridge.xSectionTable:
            self.updateXsectionData()
        # Update spinbox
        dict = {self.bridge.xSectionTable: self.bridge.xSectionRowCount, self.bridge.deckTable: self.bridge.deckRowCount, self.bridge.pierTable: self.bridge.pierRowCount}
        spinBox = dict[table]
        spinBox.setValue(table.rowCount())

    def insertRowAfter(self, table):
        """
        Insert row in QTableWidget after the current selection

        :param table: QTableWidget
        :return:
        """
    
        # Get selected row
        currentRow = table.currentRow() + 1  # add one so it is inserted after
        if currentRow is None:
            self.bridge.statusLog.insertItem(0, 'Error: No row selected')
            self.bridge.statusLabel.setText('Status: Error')
            return
        # store data
        x = []  # list of strings
        y = []  # list of strings
        for i in range(table.rowCount()):
            x.append(table.item(i, 0).text())
            if table != self.bridge.pierTable:
                y.append(table.item(i, 1).text())
        # add row and populate data
        table.setRowCount(len(x) + 1)
        if table == self.bridge.pierTable:  # populate pier numbering
            headers = ['Pier {0}'.format(p) for p in range(1, table.rowCount() + 1)]
            table.setVerticalHeaderLabels(headers)
        for i in range(table.rowCount()):
            if i < currentRow:
                table.setItem(i, 0, QTableWidgetItem(x[i]))
                if table != self.bridge.pierTable:
                    table.setItem(i, 1, QTableWidgetItem(y[i]))
            elif i == currentRow:
                table.setItem(i, 0, QTableWidgetItem('0'))
                if table != self.bridge.pierTable:
                    table.setItem(i, 1, QTableWidgetItem('0'))
            elif i > currentRow:
                table.setItem(i, 0, QTableWidgetItem(x[i - 1]))
                if table != self.bridge.pierTable:
                    table.setItem(i, 1, QTableWidgetItem(y[i - 1]))
        # update class properties for XSection data
        if table == self.bridge.xSectionTable:
            self.updateXsectionData()
        # Update spinbox
        dict = {self.bridge.xSectionTable: self.bridge.xSectionRowCount, self.bridge.deckTable: self.bridge.deckRowCount,
                self.bridge.pierTable: self.bridge.pierRowCount}
        spinBox = dict[table]
        spinBox.setValue(table.rowCount())
    
    def deleteRow(self, table):
        """
        Delete selected row
        
        :param table: QTableWidget
        :return:
        """
        
        # get selected row
        currentRow = table.currentRow()
        if currentRow is None:
            self.bridge.statusLog.insertItem(0, 'Error: No row selected')
            self.bridge.statusLabel.setText('Status: Error')
            return
        # store data
        x = []  # list of strings
        y = []  # list of strings
        for i in range(table.rowCount()):
            x.append(table.item(i, 0).text())
            if table != self.bridge.pierTable:
                y.append(table.item(i, 1).text())
        # remove row and populate data
        table.setRowCount(len(x) - 1)
        if table == self.bridge.pierTable:  # populate pier numbering
            headers = ['Pier {0}'.format(p) for p in range(1, table.rowCount() - 1)]
            table.setVerticalHeaderLabels(headers)
        x.pop(currentRow)
        if table != self.bridge.pierTable:
            y.pop(currentRow)
        for i in range(table.rowCount()):
            table.setItem(i, 0, QTableWidgetItem(x[i]))
            if table != self.bridge.pierTable:
                table.setItem(i, 1, QTableWidgetItem(y[i]))
        # update class properties for XSection data
        if table == self.bridge.xSectionTable:
            self.updateXsectionData()
        # Update spinbox
        dict = {self.bridge.xSectionTable: self.bridge.xSectionRowCount, self.bridge.deckTable: self.bridge.deckRowCount,
                self.bridge.pierTable: self.bridge.pierRowCount}
        spinBox = dict[table]
        spinBox.setValue(table.rowCount())

    def tableRowCountChanged(self, spinBox, table):
        # get number of rows
        rowCount = spinBox.value()
        # set number of rows - by default the last row is added and deleted
        table.setRowCount(rowCount)
        if table == self.bridge.pierTable:
            headers = headers = ['Pier {0}'.format(p) for p in range(1, table.rowCount() + 1)]
            table.setVerticalHeaderLabels(headers)
    
    def showMenu(self, pos):
        """
        graph right click menu
        
        :param pos: position on widget
        :return:
        """
        
        menu = QMenu(self.bridge)
        exportCsv_action = QAction("Export Plot Data to Csv", menu)
        exportCsv_action.triggered.connect(self.export_csv)
        menu.addAction(exportCsv_action)
        menu.popup(self.plotWdg.mapToGlobal(pos))
    
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

    def export_csv(self):
        """
        Export XS to csv
        
        :return:
        """
    
        settings = QSettings()
        lastFolder = str(settings.value("TUFLOW_Bridge_editor/export_csv", os.sep))
        if (len(lastFolder) > 0):  # use last folder if stored
            fpath = lastFolder
        else:
            fpath = os.getcwd()
        # Get data headers
        dataHeader = 'Offset,Elevation'
        resultFiles = ['elevation']
        c = [0]  # index for change in result files or current time is selected
        maxLen = 0
        for i in c:
            maxLen = max(maxLen, len(self.subplot.lines[i].get_data()[0]))
        # Get data
        for i, resultFile in enumerate(resultFiles):
            if i == 0:
                data = self.subplot.lines[c[i]].get_data()[0]  # write X axis first
                data = numpy.reshape(data, [len(data), 1])
                if len(data) < maxLen:
                    diff = maxLen - len(data)
                    fill = numpy.zeros([diff, 1]) * numpy.nan
                    data = numpy.append(data, fill, axis=0)
            else:
                dataX = self.subplot.lines[c[i]].get_data()[0]  # Write X axis again for new results
                dataX = numpy.reshape(dataX, [len(dataX), 1])
                if len(dataX) < maxLen:
                    diff = maxLen - len(dataX)
                    fill = numpy.zeros([diff, 1]) * numpy.nan
                    dataX = numpy.append(dataX, fill, axis=0)
                data = numpy.append(data, dataX, axis=1)
            if i < len(c) - 1:  # isn't last result file
                for line in self.subplot.lines[c[i]:c[i + 1]]:
                    dataY = line.get_data()[1]
                    dataY = numpy.reshape(dataY, [len(dataY), 1])
                    if len(dataY) < maxLen:
                        diff = maxLen - len(dataY)
                        fill = numpy.zeros([diff, 1]) * numpy.nan
                        dataY = numpy.append(dataY, fill, axis=0)
                    data = numpy.append(data, dataY, axis=1)
            else:  # is last result file
                for line in self.subplot.lines[c[i]:]:
                    dataY = line.get_data()[1]
                    dataY = numpy.reshape(dataY, [len(dataY), 1])
                    if len(dataY) < maxLen:
                        diff = maxLen - len(dataY)
                        fill = numpy.zeros([diff, 1]) * numpy.nan
                        dataY = numpy.append(dataY, fill, axis=0)
                    data = numpy.append(data, dataY, axis=1)
        # Save data out
        saveFile = QFileDialog.getSaveFileName(self, 'Save File', fpath)
        if len(saveFile) < 2:
            return
        else:
            if saveFile != os.sep and saveFile.lower() != 'c:\\' and saveFile != '':
                settings.setValue("TUFLOW_Bridge_editor/export_csv", saveFile)
        if saveFile is not None:
            try:
                file = open(saveFile, 'w')
                file.write('{0}\n'.format(dataHeader))
                for i, row in enumerate(data):
                    line = ''
                    for j, value in enumerate(row):
                        if not numpy.isnan(data[i][j]):
                            line += '{0},'.format(data[i][j])
                        else:
                            line += '{0},'.format('')
                    line += '\n'
                    file.write(line)
                file.close()
            except IOError:
                self.bridge.statusLog.insertItem(0, 'Error: Opening File for editing')
                self.bridge.statusLabel.setText('Status: Error')
                return
        self.bridge.statusLog.insertItem(0, 'Successfully exported csv')
        self.bridge.statusLabel.setText('Status: Successful')
        
    def createLayer(self):
        """
        Import an empty 2d_lfcsh layer and add temp layer feature with attributes
        
        :return:
        """
        
        # precheck to see if there is a feature to create
        if self.feat is None:
            self.bridge.statusLog.insertItem(0, 'Error: No features to create layer from')
            self.bridge.statusLabel.setText('Status: Error')
            return
        # import empty file
        emptyTypes = ['2d_lfcsh']
        lines = True
        points = False
        regions = False
        if self.variableGeom:
            points = True
        message = tuflowqgis_import_empty_tf(self.iface, self.bridge.emptydir.text(), self.bridge.runId.text(), emptyTypes, points, lines, regions)
        if message is not None:
            QMessageBox.critical(self.iface.mainWindow(), "Importing TUFLOW Empty File(s)", message)
        # add features
        self.editLayer(tuflowqgis_find_layer('2d_lfcsh_{0}_L'.format(self.bridge.runId.text())), self.feat, True)
        #self.bridge.statusLabel.setText('Status: Successful')
    
    def updateLayer(self):
        """
        Update the selected bridge layer with either updated attributes of selected feature, or add new feature
        
        :return:
        """
        
        lyr = self.iface.mapCanvas().currentLayer()  # QgsVectorLayer
        feat = lyr.selectedFeatures()   # list [QgsFeature]
        if self.feat is None:
            if len(feat) > 0:
                self.editLayer(lyr, feat[0], False)
            else:
                self.bridge.statusLog.insertItem(0, 'Error: No edits to update')
                self.bridge.statusLabel.setText('Status: Error')
        else:
            self.editLayer(lyr, self.feat, True)
        self.bridge.statusLabel.setText('Status: Successful')
    
    def incrementLayer(self):
        """
        Increment layer then update with new feature or updated fields
        
        :return:
        """
        
        # get current layer
        lyr = self.iface.mapCanvas().currentLayer()  # QgsVectorLayer
        feat = lyr.selectedFeatures()  # QgsFeature
        if len(feat) > 0:
            fid = feat[0].id()
        # increment layer
        self.incrementDialog = tuflowqgis_increment_dialog(self.iface)
        self.incrementDialog.exec_()
        # get new layer
        lyr = tuflowqgis_find_layer(self.incrementDialog.outname)
        if len(feat) > 0:
            for feature in lyr.getFeatures():
                if feature.id() == fid:
                    feat = feature
                    break
                else:
                    feat = None
        if self.feat is None:
            if feat is not None:
                self.editLayer(lyr, feat, False)
            else:
                self.bridge.statusLog.insertItem(0, 'Error: No edits to update')
                self.bridge.statusLabel.setText('Status: Error')
        else:
            self.editLayer(lyr, self.feat, True)
        self.bridge.statusLabel.setText('Status: Successful')
    
    def editLayer(self, layer, feat, append):
        """
        edit layer with new feature or updated fields
        
        :param layer: QgsVectorLayer
        :param feat: QgsFeature
        :param append: bool - True for append to layer, false for don't append
        :return:
        """
        
        dp = layer.dataProvider()
        attributes = [float(self.bridge.invert.text()),
                      float(self.bridge.dz.text()),
                      float(self.bridge.shapeWidth.text()),
                      self.bridge.shapeOptions.text(),
                      float(self.bridge.layer1Obv.text()),
                      float(self.bridge.layer1Block.text()),
                      float(self.bridge.layer1Flc.text()),
                      float(self.bridge.layer2Depth.text()),
                      float(self.bridge.layer2Block.text()),
                      float(self.bridge.layer2Flc.text()),
                      float(self.bridge.layer3Depth.text()),
                      float(self.bridge.layer3Block.text()),
                      float(self.bridge.layer3Flc.text()),
                      self.bridge.comment.text()]
        layer.startEditing()
        feat.setAttributes(attributes)
        if append:
            dp.addFeatures([feat])
        else:
            layer.updateFeature(feat)
        layer.commitChanges()
        # select created feature
        #if append:
        #    fid = feat.id()
        #    for f in layer.getFeatures():
        #        if f.id() == fid:
        #            layer.select(fid)
        self.canvas.scene().removeItem(self.rubberBand)  # Remove previous temp layer
        self.layer = layer
        self.updated = True
        self.saveData()
        self.clearXsection()
        self.feat = None
        layer.triggerRepaint()
        self.bridge.statusLabel.setText('Status: Successful')
        self.bridge = None