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
from tuflowqgis_library import lineToPoints, getRasterValue, findAllRasterLyrs, tuflowqgis_find_layer
from canvas_event import canvasEvent
from Pier_Losses import lookupPierLoss
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/forms")
from ui_tuflowqgis_bridge_editor import Ui_tuflowqgis_BridgeEditor
# Debug using PyCharm
sys.path.append(r'C:\Program Files\JetBrains\PyCharm 2018.1\debug-eggs')
sys.path.append(r'C:\Program Files\JetBrains\PyCharm 2018.1\helpers\pydev')

class bridgeEditor(QDockWidget, Ui_tuflowqgis_BridgeEditor):

    def __init__(self, iface, **kwargs):
        QDockWidget.__init__(self)
        self.wdg = Ui_tuflowqgis_BridgeEditor.__init__(self)
        self.setupUi(self)
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.connected = False
        self.cursorTrackingConnected = False
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
        self.initialisePlot()
        self.qgis_connect()
        self.populateDems()
        
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
            self.emptydir.setText(os.path.join(basepath, "TUFLOW", "model", "gis", "empty"))
        else:
            self.emptydir.setText("ERROR - Project not loaded")

    def __del__(self):
        self.qgis_disconnect()

    def qgis_connect(self):
        """
        Set up signal connections.
        
        :return: void
        """
        
        if not self.connected:
            self.pbUpdate.clicked.connect(self.updatePlot)
            self.pbUpdatePierData.clicked.connect(self.updatePierTable)
            self.pbUpdateDeckData.clicked.connect(self.updateDeckTable)
            self.pbUseMapWindowSel.clicked.connect(self.getCurrSel)
            self.pbDrawXsection.clicked.connect(self.useTempPolyline)
            self.pbClearXsection.clicked.connect(self.clearXsection)
            self.pbUpdateAttributes.clicked.connect(self.updateAttributes)
            self.iface.currentLayerChanged.connect(self.populateDems)
            self.xSectionRowCount.valueChanged.connect(lambda: self.tableRowCountChanged(self.xSectionRowCount, self.xSectionTable))
            self.deckRowCount.valueChanged.connect(lambda: self.tableRowCountChanged(self.deckRowCount, self.deckTable))
            self.pierRowCount.valueChanged.connect(lambda: self.tableRowCountChanged(self.pierRowCount, self.pierTable))
            self.plotWdg.setContextMenuPolicy(Qt.CustomContextMenu)
            self.plotWdg.customContextMenuRequested.connect(self.showMenu)
            self.xSectionTableRowHeaders = self.xSectionTable.verticalHeader()
            self.pierTableRowHeaders = self.pierTable.verticalHeader()
            self.deckTableRowHeaders = self.deckTable.verticalHeader()
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
            self.pbUpdate.clicked.disconnect(self.updatePlot)
            self.pbUpdatePierData.clicked.disconnect(self.updatePierTable)
            self.pbUpdateDeckData.clicked.disconnect(self.updateDeckTable)
            self.pbUseMapWindowSel.clicked.disconnect(self.getCurrSel)
            self.pbDrawXsection.clicked.disconnect(self.useTempPolyline)
            self.pbClearXsection.clicked.disconnect(self.clearXsection)
            self.pbUpdateAttributes.clicked.disconnect(self.updateAttributes)
            self.iface.currentLayerChanged.disconnect(self.populateDems)
            self.xSectionRowCount.valueChanged.disconnect(lambda: self.tableRowCountChanged(self.xSectionRowCount, self.xSectionTable))
            self.deckRowCount.valueChanged.disconnect(lambda: self.tableRowCountChanged(self.deckRowCount, self.deckTable))
            self.pierRowCount.valueChanged.disconnect(lambda: self.tableRowCountChanged(self.pierRowCount, self.pierTable))
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
            mpltoolbar = matplotlib.backends.backend_qt4agg.NavigationToolbar2QT(self.plotWdg, self.frame_for_toolbar)
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
                self.statusLog.insertItem(0, 'Error: Layer is not a polyline type')
                self.statusLabel.setText('Status: Error')
                return
            else:
                self.statusLabel.setText('Status: Successful')
        # Check number of features selected
        if len(feat) == 0:
            self.statusLog.insertItem(0, 'Error: No Features Selected')
            self.statusLabel.setText('Status: Error')
            return
        if len(feat) > 1:
            self.statusLog.insertItem(0, 'Warning: More than one feature selected - using first selection in {0}'.format(lyr.name()))
            self.statusLabel.setText('Status: Warning')
        else:
            #self.statusLog.insertItem(0, 'Message: Draping line in {0}'.format(lyr.name()))
            self.statusLabel.setText('Status: Successful')
        feat = feat[0]  # QgsFeature
        # Get DEM for draping
        dem = tuflowqgis_find_layer(self.demComboBox.currentText())  # QgsRasterLayer
        if dem is None:
            self.statusLog.insertItem(0, 'Error: No DEM selected')
            self.statusLabel.setText('Status: Error')
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
        self.xSectionTable.setRowCount(0)
        self.deckTable.setRowCount(0)
        self.pierTable.setRowCount(0)
        # clear spinboxes
        self.xSectionRowCount.setValue(0)
        self.deckRowCount.setValue(0)
        self.pierRowCount.setValue(0)
    
    def createMemoryLayerFromTempLayer(self):
        """
        Creates a QgsFeature from the QgsPoint vertices in the temp layer
        
        :return:
        """
        
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromPolyline(self.points))
        self.extractXSection(None, [feat])
    
    def useTempPolyline(self):
        """
        Creates a graphic polyline that can be drawn on the map canvas
        
        :return: void
        """
        
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

        self.xSectionTable.setRowCount(len(self.xSectionOffset))
        self.xSectionTable.setItem(0, 0, QTableWidgetItem('test'))
        for i, value in enumerate(self.xSectionOffset):
            self.xSectionTable.setItem(i, 0, QTableWidgetItem(str(value)))
            self.xSectionTable.setItem(i, 1, QTableWidgetItem(str(self.xSectionElev[i])))
        # update spinbox
        self.xSectionRowCount.setValue(self.xSectionTable.rowCount())

    def updateXsectionData(self):
        """
        Update data based on the data in the table
        
        :return: list self.xSectionOffset
        :return: list self.xSectionElev
        """
        
        self.xSectionOffset = []
        self.xSectionElev = []
        for i in range(self.xSectionTable.rowCount()):
            self.xSectionOffset.append(float(self.xSectionTable.item(i, 0).text()))
            self.xSectionElev.append(float(self.xSectionTable.item(i, 1).text()))
            
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
        self.pierTable.setRowCount(self.pierNo.value())
        # Populate values and column headers
        self.pierRowHeaders = []
        for i in range(1, self.pierNo.value() + 1):
            self.pierRowHeaders.append('Pier {0}'.format(i))
            if i == 1:
                offset = self.pierWidthLeft.value() + self.pierWidth.value() / 2
            else:
                offset += self.pierWidth.value() + self.pierGap.value()
            self.pierOffset.append(offset)
        self.pierTable.setVerticalHeaderLabels(self.pierRowHeaders)
        for i, pier in enumerate(self.pierOffset):
            self.pierTable.setItem(i, 0, QTableWidgetItem(str(pier)))
        # update spinbox
        self.pierRowCount.setValue(self.pierTable.rowCount())

    def createPierPatches(self):
        """
        Creates a list of patches to be used to create matplotlib patches

        :return: void updates self.pierPatches
        """
        
        if self.pierTable.item(0, 0) is None:
            self.statusLog.insertItem(0, 'Warning: No Piers Defined in Table')
            self.statusLabel.setText('Status: Warning')
            return
        self.pierPatches = []
        for i in range(self.pierTable.rowCount()):
            x = []
            y = []
            x1 = float(self.pierTable.item(i, 0).text()) - self.pierWidth.value() / 2
            x2 = float(self.pierTable.item(i, 0).text()) + self.pierWidth.value() / 2
            y1a = self.getGroundAtX(x1)
            y1b = self.getGroundAtX(x2)
            y2a = self.interpolateVLookupObvert(x1)
            y2b = self.interpolateVLookupObvert(x2)
            if y2a <= y1a or y2b <= y1b:
                self.statusLog.insertItem(0, 'Error: Bridge deck level is lower than ground')
                self.statusLabel.setText('Status: Error')
                return
            else:
                self.statusLabel.setText('Status: Successful')
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
        self.statusLabel.setText('Status: Successful')
            
    def updateDeckTable(self):
        """
        Updates the deck table widget based on the input parameters
        
        :return:
        """

        self.mouseTrackDisconnect()
        # Set up table
        self.deckTable.setRowCount(2)
        # Update parameters
        xmin = self.getXatElevation(self.deckElevationBottom.value(), 1)
        xmax = self.getXatElevation(self.deckElevationBottom.value(), -1)
        self.deckTable.setItem(0, 0, QTableWidgetItem(str(xmin)))
        self.deckTable.setItem(1, 0, QTableWidgetItem(str(xmax)))
        self.deckTable.setItem(0, 1, QTableWidgetItem(str(self.deckElevationBottom.value())))
        self.deckTable.setItem(1, 1, QTableWidgetItem(str(self.deckElevationBottom.value())))
        
    def updateDeckOffset(self):
        """
        Updates the first and last offset value in the deck table to be where the deck meets the Xsection
        
        :return:
        """
        
        if self.deckTable.item(0, 0) is not None:
            # first value
            elevation = float(self.deckTable.item(0, 1).text())
            offset = self.getXatElevation(elevation, 1)
            self.deckTable.setItem(0, 0, QTableWidgetItem(str(self.getXatElevation(elevation, 1))))
            # last value
            lastRow = self.deckTable.rowCount() - 1
            elevation = float(self.deckTable.item(lastRow, 1).text())
            offset = self.getXatElevation(elevation, -1)
            self.deckTable.setItem(lastRow, 0, QTableWidgetItem(str(offset)))
            self.updateObverts()
        # Update spinbox
        self.deckRowCount.setValue(self.deckTable.rowCount())
            
    def interpolateVLookupObvert(self, x):
        """
        A vertical lookup from the deck table. Will interpolate between values
        
        :param x: float- offset for lookup
        :return: float- elevation value
        """
        
        
        for i in range(self.deckTable.rowCount()):
            offset = float(self.deckTable.item(i, 0).text())
            y = float(self.deckTable.item(i, 1).text())
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
        lastRow = self.deckTable.rowCount() - 1
        for offset in self.xSectionOffset:
            if offset == float(self.deckTable.item(0, 0).text()):  # equal to the first entry in the deck table
                self.obverts.append(float(self.deckTable.item(0, 1).text()))
            elif offset == float(self.deckTable.item(lastRow, 0).text()):  # equal to the last entry in the deck table
                self.obverts.append(float(self.deckTable.item(lastRow, 1).text()))
            elif offset > float(self.deckTable.item(0, 0).text()) and offset < float(self.deckTable.item(lastRow, 0).text()):  # in between first and last entry- interpolate
                self.obverts.append(self.interpolateVLookupObvert(offset))
            elif offset > float(self.deckTable.item(lastRow, 0).text()):  # after last entry
                self.obverts.append(float(self.deckTable.item(lastRow, 1).text()))
            else:  # before first entry
                self.obverts.append(float(self.deckTable.item(0, 1).text()))
        
    def createDeckPatch(self):
        """
        Creates a matplotlib patch for plotting the bridge deck
        
        :return: void updates self.deckPatch
        """
        
        if self.deckTable.item(0, 0) is None:
            self.statusLog.insertItem(0, 'Warning: No Piers Defined in Table')
            self.statusLabel.setText('Status: Warning')
            return
        x = []
        y = []
        # Get patch values between upper and lower deck cords on left hand side
        y1 = float(self.deckTable.item(0, 1).text())  # lower cord on left hand deck limit
        y2 = y1 + self.deckThickness.value()  # upper cord on left hand deck limit
        x1 = float(self.deckTable.item(0, 0).text())  # x value of lower cord on left hand deck limit
        x2 = self.getXatElevation(y2, 1)  # x value of upper cord on left hand deck limit
        x.append(x2)
        y.append(y2)
        iStart = None
        iEnd = None
        # Follow xsection for path between upper and lower cords
        for i, offset in enumerate(self.xSectionOffset):
            if i == 0:
                if x2 == offset:
                    x.append(offset)
                    y.append(self.xSectionElev[i])
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
        iMax = self.deckTable.rowCount() - 1
        underDeck = False
        start = False
        for i, xsElev in enumerate(self.xSectionElev):
            if i == 90:
                pass
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
            elif offset >= float(self.deckTable.item(iMax, 0).text()):
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
                #if offset >= float(self.deckTable.item(iMax, 0).text()):
                #    start = False
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
        y3 = float(self.deckTable.item(iMax, 1).text())  # lower cord on right hand deck limit
        y4 = y3 + self.deckThickness.value()  # upper cord on right hand deck limit
        x3 = float(self.deckTable.item(iMax, 0).text())  # x value of lower cord on right hand deck limit
        x4 = self.getXatElevation(y4, -1)  # x value of upper cord on right hand deck limit
        x.append(x3)
        y.append(y3)
        iStart = None
        iEnd = None
        for i, offset in enumerate(self.xSectionOffset):
            if i == 0:
                if x3 == offset:
                    x.append(offset)
                    y.append(self.xSectionElev[i])
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
            obvert = self.obverts[i] + self.deckThickness.value()
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
            elif xsElev < obvert and xsElevPrev > obvertPrev:
                underDeck = True
                start = True
                x.append(self.interpolate(obvert, xsElevPrev, xsElev, offsetPrev, offset))
                y.append(obvert)
            elif xsElev > obvert and xsElevPrev < obvertPrev:
                underDeck = False
                x.append(self.interpolate(obvert, xsElevPrev, xsElev, offsetPrev, offset))
                y.append(obvert)
                if offset <= float(self.deckTable.item(0, 0).text()):
                    start = False
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
                    self.statusLabel.setText('Status: Successful')
                    return self.xSectionElev[i]
                xPrev = offset
                iPrev = i
            else:
                if x == offset:
                    self.statusLabel.setText('Status: Successful')
                    return self.xSectionElev[i]
                elif x > xPrev and x < offset:
                    self.statusLabel.setText('Status: Successful')
                    return self.interpolate(x, xPrev, offset, self.xSectionElev[iPrev], self.xSectionElev[i])
                else:
                    xPrev = offset
                    iPrev = i
        self.statusLog.insertItem(0, 'Error: Unable to find ground level at pier offset')
        self.statusLabel.setText('Status: Error')
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
        if self.deckTable.item(0, 0) is None:
            self.statusLog.insertItem(0, 'Warning: Unable to calculate energy loss without bridge deck')
            self.statusLabel.setText('Status: Warning')
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
        self.statusLabel.setText('Status: Successful')
        
    def calculatePierArea(self):
        """
        Calculates the area obstructed by the piers
        
        :return:
        """
        
        self.pierArea = 0
        if self.pierTable.item(0, 0) is None:
            return
        else:
            for i, pier in enumerate(self.pierPatches):
                xEnd = float(self.pierTable.item(i, 0).text()) + self.pierWidth.value() / 2
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
        
        menu = QMenu(self)
        insertRowBefore_action = QAction("Insert Row (before)", menu)
        insertRowAfter_action = QAction("Insert Row (after)", menu)
        deleteRow_action = QAction("Delete Row", menu)
        insertRowBefore_action.triggered.connect(lambda: self.insertRowBefore(self.pierTable))
        insertRowAfter_action.triggered.connect(lambda: self.insertRowAfter(self.pierTable))
        deleteRow_action.triggered.connect(lambda: self.deleteRow(self.pierTable))
        menu.addAction(insertRowBefore_action)
        menu.addAction(insertRowAfter_action)
        menu.addAction(deleteRow_action)
        menu.popup(self.pierTable.mapToGlobal(pos))
        
    def showDeckTableMenu(self, pos):
        """
        Table right click menu

        :param pos: QPoint & pos
        :return:
        """
        
        menu = QMenu(self)
        insertRowBefore_action = QAction("Insert Row (before)", menu)
        insertRowAfter_action = QAction("Insert Row (after)", menu)
        deleteRow_action = QAction("Delete Row", menu)
        insertRowBefore_action.triggered.connect(lambda: self.insertRowBefore(self.deckTable))
        insertRowAfter_action.triggered.connect(lambda: self.insertRowAfter(self.deckTable))
        deleteRow_action.triggered.connect(lambda: self.deleteRow(self.deckTable))
        menu.addAction(insertRowBefore_action)
        menu.addAction(insertRowAfter_action)
        menu.addAction(deleteRow_action)
        menu.popup(self.pierTable.mapToGlobal(pos))
        
    def showXsectionTableMenu(self, pos):
        """
        Table right click menu

        :param pos: QPoint & pos
        :return:
        """
        
        menu = QMenu(self)
        insertRowBefore_action = QAction("Insert Row (before)", menu)
        insertRowAfter_action = QAction("Insert Row (after)", menu)
        deleteRow_action = QAction("Delete Row", menu)
        insertRowBefore_action.triggered.connect(lambda: self.insertRowBefore(self.xSectionTable))
        insertRowAfter_action.triggered.connect(lambda: self.insertRowAfter(self.xSectionTable))
        deleteRow_action.triggered.connect(lambda: self.deleteRow(self.xSectionTable))
        menu.addAction(insertRowBefore_action)
        menu.addAction(insertRowAfter_action)
        menu.addAction(deleteRow_action)
        menu.popup(self.pierTable.mapToGlobal(pos))
        
    def insertRowBefore(self, table):
        """
        Insert row in QTableWidget before the current selection
        
        :param table: QTableWidget
        :return:
        """
        
        # Get selected row
        currentRow = table.currentRow()
        if currentRow is None:
            self.statusLog.insertItem(0, 'Error: No row selected')
            self.statusLabel.setText('Status: Error')
            return
        # store data
        x = []  # list of strings
        y = []  # list of strings
        for i in range(table.rowCount()):
            x.append(table.item(i, 0).text())
            if table != self.pierTable:
                y.append(table.item(i, 1).text())
        # add row and populate data
        table.setRowCount(len(x) + 1)
        if table == self.pierTable:  # populate pier numbering
            headers = ['Pier {0}'.format(p) for p in range(1, table.rowCount() + 1)]
            table.setVerticalHeaderLabels(headers)
        for i in range(table.rowCount()):
            if i < currentRow:
                table.setItem(i, 0, QTableWidgetItem(x[i]))
                if table != self.pierTable:
                    table.setItem(i, 1, QTableWidgetItem(y[i]))
            elif i == currentRow:
                table.setItem(i, 0, QTableWidgetItem('0'))
                if table != self.pierTable:
                    table.setItem(i, 1, QTableWidgetItem('0'))
            elif i > currentRow:
                table.setItem(i, 0, QTableWidgetItem(x[i - 1]))
                if table != self.pierTable:
                   table.setItem(i, 1, QTableWidgetItem(y[i - 1]))
        # update class properties for XSection data
        if table == self.xSectionTable:
            self.updateXsectionData()
        # Update spinbox
        dict = {self.xSectionTable: self.xSectionRowCount, self.deckTable: self.deckRowCount, self.pierTable: self.pierRowCount}
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
            self.statusLog.insertItem(0, 'Error: No row selected')
            self.statusLabel.setText('Status: Error')
            return
        # store data
        x = []  # list of strings
        y = []  # list of strings
        for i in range(table.rowCount()):
            x.append(table.item(i, 0).text())
            if table != self.pierTable:
                y.append(table.item(i, 1).text())
        # add row and populate data
        table.setRowCount(len(x) + 1)
        if table == self.pierTable:  # populate pier numbering
            headers = ['Pier {0}'.format(p) for p in range(1, table.rowCount() + 1)]
            table.setVerticalHeaderLabels(headers)
        for i in range(table.rowCount()):
            if i < currentRow:
                table.setItem(i, 0, QTableWidgetItem(x[i]))
                if table != self.pierTable:
                    table.setItem(i, 1, QTableWidgetItem(y[i]))
            elif i == currentRow:
                table.setItem(i, 0, QTableWidgetItem('0'))
                if table != self.pierTable:
                    table.setItem(i, 1, QTableWidgetItem('0'))
            elif i > currentRow:
                table.setItem(i, 0, QTableWidgetItem(x[i - 1]))
                if table != self.pierTable:
                    table.setItem(i, 1, QTableWidgetItem(y[i - 1]))
        # update class properties for XSection data
        if table == self.xSectionTable:
            self.updateXsectionData()
        # Update spinbox
        dict = {self.xSectionTable: self.xSectionRowCount, self.deckTable: self.deckRowCount,
                self.pierTable: self.pierRowCount}
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
            self.statusLog.insertItem(0, 'Error: No row selected')
            self.statusLabel.setText('Status: Error')
            return
        # store data
        x = []  # list of strings
        y = []  # list of strings
        for i in range(table.rowCount()):
            x.append(table.item(i, 0).text())
            if table != self.pierTable:
                y.append(table.item(i, 1).text())
        # remove row and populate data
        table.setRowCount(len(x) - 1)
        if table == self.pierTable:  # populate pier numbering
            headers = ['Pier {0}'.format(p) for p in range(1, table.rowCount() - 1)]
            table.setVerticalHeaderLabels(headers)
        x.pop(currentRow)
        if table != self.pierTable:
            y.pop(currentRow)
        for i in range(table.rowCount()):
            table.setItem(i, 0, QTableWidgetItem(x[i]))
            if table != self.pierTable:
                table.setItem(i, 1, QTableWidgetItem(y[i]))
        # update class properties for XSection data
        if table == self.xSectionTable:
            self.updateXsectionData()
        # Update spinbox
        dict = {self.xSectionTable: self.xSectionRowCount, self.deckTable: self.deckRowCount,
                self.pierTable: self.pierRowCount}
        spinBox = dict[table]
        spinBox.setValue(table.rowCount())

    def tableRowCountChanged(self, spinBox, table):
        # get number of rows
        rowCount = spinBox.value()
        # set number of rows - by default the last row is added and deleted
        table.setRowCount(rowCount)
        if table == self.pierTable:
            headers = headers = ['Pier {0}'.format(p) for p in range(1, table.rowCount() + 1)]
            table.setVerticalHeaderLabels(headers)
    
    def showMenu(self, pos):
        """
        graph right click menu
        
        :param pos: position on widget
        :return:
        """
        
        menu = QMenu(self)
        exportCsv_action = QAction("Export Plot Data to Csv", menu)
        exportCsv_action.triggered.connect(self.export_csv)
        menu.addAction(exportCsv_action)
        menu.popup(self.plotWdg.mapToGlobal(pos))
    
    def updateAttributes(self):
        # Invert
        self.invert.setText('99999')
        # dZ
        self.dz.setText('0')
        # Shape Width
        self.shapeWidth.setText('{0:.1f}'.format(float(self.zLineWidth.text())))
        if self.pierTable.item(0, 0) is None:
            self.statusLog.insertItem(0, 'Warning: No Piers Defined in Table')
            self.statusLabel.setText('Status: Warning')
        else:
            self.layer1Obv.setText(self.deckTable.item(0, 1).text())
        # pier values
        self.calculateFlowArea()
        self.calculatePierArea()
        self.layer1Block.setText('{0:.1f}'.format(self.pierArea / self.area * 100))
        self.layer1Flc.setText('{0:.2f}'.format(lookupPierLoss(int(self.pierShape.currentText()), self.pierArea / self.area)))
        # elevation values
        self.layer1Obv.setText(str(self.deckElevationBottom.value()))
        self.layer2Depth.setText(str(self.deckThickness.value()))
        self.layer3Depth.setText(str(self.handRailDepth.value()))
        self.label_35.setText('Constant level')
        self.label_36.setText('Constant level')
        self.label_37.setText('Constant level')
        for i in range(self.deckTable.rowCount()):
            elev = float(self.deckTable.item(i, 1).text())
            if i == 0:
                elevPrev = elev
            else:
                if elev != elevPrev:
                    self.layer1Obv.setText('0')
                    self.layer2Depth.setText('0')
                    self.layer3Depth.setText('0')
                    self.label_35.setText('Variable elevation- Points layer will be created')
                    self.label_36.setText('Variable elevation- Points layer will be created')
                    self.label_37.setText('Variable elevation- Points layer will be created')
                    break
        # other blockage and FLC values
        self.layer2Block.setText('100')
        self.layer3Block.setText(str(self.handRailBlockage.value()))
        self.layer3Flc.setText(str(self.handRailFlc.value()))
        if self.rbDrowned.isChecked():
            self.layer2Flc.setText('0.5')
        else:
            self.layer2Flc.setText('1.56')
        # comment
        if not self.comment.text():
            self.comment.setText(self.bridgeName.text())

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
                self.statusLog.insertItem(0, 'Error: Opening File for editing')
                self.statusLabel.setText('Status: Error')
                return
        self.statusLog.insertItem(0, 'Successfully exported csv')
        self.statusLabel.setText('Status: Successful')