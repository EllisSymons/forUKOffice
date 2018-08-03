# coding=utf-8
from tuflowqgis_bridge_editor import *
from tuflowqgis_bridge_filehandler import *
from tuflow.tuflowqgis_library import findAllRasterLyrs
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
        self.cLyr = self.canvas.currentLayer()
        self.bridges = {}  # lyr name,fid: bridgeEditor class object
        self.connected = False  # connections for gui
        self.buttonsConnected = False  # gui buttons connected via editor
        self.initialisePlot()
        self.populateDems()
        self.bridge = bridgeEditor(self, self.iface)
        
        # setup context menus
        self.xSectionTableRowHeaders = self.xSectionTable.verticalHeader()
        self.pierTableRowHeaders = self.pierTable.verticalHeader()
        self.deckTableRowHeaders = self.deckTable.verticalHeader()
        self.plotWdg.setContextMenuPolicy(Qt.CustomContextMenu)
        self.xSectionTableRowHeaders.setContextMenuPolicy(Qt.CustomContextMenu)
        self.deckTableRowHeaders.setContextMenuPolicy(Qt.CustomContextMenu)
        self.pierTableRowHeaders.setContextMenuPolicy(Qt.CustomContextMenu)
        
        # set up signals
        self.parent_connect()  # connect signal independent of if bridge editor object
        self.child_connect()  # connect signals that edit bridge editor object
        
    def __del__(self):
        self.child_disconnect()
        self.parent_disconnect()
        
    def parent_connect(self):
        """
        Set up signal connections for global gui window i.e. independent of if a bridge editor object is present.

        :return: void
        """
    
        if not self.connected:
            self.canvas.layersChanged.connect(self.populateDems)
            self.canvas.layersChanged.connect(self.checkForBridge)
            self.canvas.currentLayerChanged.connect(self.checkForBridge)
            self.canvas.selectionChanged.connect(self.checkForBridge)
            self.pbDrawXsection.clicked.connect(self.startNewBridge)
            self.pbSaveFile.clicked.connect(self.saveBridge)
            self.connected = True
            
    def child_connect(self):
        """
        Set up signal connections for bridge editor object.
        Done through GUI as this seems to allow for better python class de-constructor
        
        :return:
        """
        
        if not self.buttonsConnected:
            # push buttons
            self.pbUpdate.clicked.connect(self.bridge.updatePlot)
            self.pbUpdatePierData.clicked.connect(self.bridge.updatePierTable)
            self.pbUpdateDeckData.clicked.connect(self.bridge.updateDeckTable)
            self.pbUseMapWindowSel.clicked.connect(self.bridge.getCurrSel)
            self.pbClearXsection.clicked.connect(self.bridge.clearXsection)
            self.pbUpdateAttributes.clicked.connect(self.bridge.updateAttributes)
            self.pbCreateLayer.clicked.connect(lambda: createLayer(self.bridge))
            self.pbUpdateLayer.clicked.connect(lambda: updateLayer(self.bridge))
            self.pbIncrementLayer.clicked.connect(lambda: incrementLayer(self.bridge))
            # Spin boxes
            self.xSectionRowCount.valueChanged.connect(lambda: tableRowCountChanged(self.bridge, self.xSectionRowCount, self.xSectionTable))
            self.deckRowCount.valueChanged.connect(lambda: tableRowCountChanged(self.bridge, self.deckRowCount, self.deckTable))
            self.pierRowCount.valueChanged.connect(lambda: tableRowCountChanged(self.bridge, self.pierRowCount, self.pierTable))
            # Right Click (Context) Menus
            self.xSectionTableRowHeaders.customContextMenuRequested.connect(lambda pos: xSectionTableMenu(self.bridge, pos))
            self.deckTableRowHeaders.customContextMenuRequested.connect(lambda pos: deckTableMenu(self.bridge, pos))
            self.pierTableRowHeaders.customContextMenuRequested.connect(lambda pos: pierTableMenu(self.bridge, pos))
            self.plotWdg.customContextMenuRequested.connect(lambda pos: plotterMenu(self.bridge, pos))
            # Other connections to tell the object that there has been an update
            self.bridgeName.textChanged.connect(self.bridge.setUpdated)
            self.deckElevationBottom.valueChanged.connect(self.bridge.setUpdated)
            self.deckThickness.valueChanged.connect(self.bridge.setUpdated)
            self.handRailDepth.valueChanged.connect(self.bridge.setUpdated)
            self.handRailFlc.valueChanged.connect(self.bridge.setUpdated)
            self.handRailBlockage.valueChanged.connect(self.bridge.setUpdated)
            self.rbDrowned.toggled.connect(self.bridge.setUpdated)
            self.pierNo.valueChanged.connect(self.bridge.setUpdated)
            self.pierWidth.valueChanged.connect(self.bridge.setUpdated)
            self.pierWidthLeft.valueChanged.connect(self.bridge.setUpdated)
            self.pierGap.valueChanged.connect(self.bridge.setUpdated)
            self.pierShape.currentIndexChanged.connect(self.bridge.setUpdated)
            self.zLineWidth.valueChanged.connect(self.bridge.setUpdated)
            self.enforceInTerrain.stateChanged.connect(self.bridge.setUpdated)
            self.cLyr.editingStopped.connect(self.bridge.setUpdated)
            #self.pierTable.itemActivated.connect(self.bridge.setUpdated)
    
            self.buttonsConnected = True

    def parent_disconnect(self):
        """
        Disconnect signal connections

        :return: void
        """
    
        if self.connected:
            self.canvas.layersChanged.disconnect(self.populateDems)
            self.canvas.layersChanged.disconnect(self.checkForBridge)
            self.canvas.currentLayerChanged.disconnect(self.checkForBridge)
            self.canvas.selectionChanged.disconnect(self.checkForBridge)
            self.pbDrawXsection.clicked.disconnect(self.startNewBridge)
            self.pbSaveFile.clicked.disconnect()
            self.connected = False

    def child_disconnect(self):
        """
        Disconnect signal connections
        
        :return:
        """
    
        if self.buttonsConnected:
            # push buttons
            self.pbUpdate.clicked.disconnect()
            self.pbUpdatePierData.clicked.disconnect()
            self.pbUpdateDeckData.clicked.disconnect()
            self.pbUseMapWindowSel.clicked.disconnect()
            # self.gui.pbDrawXsection.clicked.connect(self.useTempPolyline)
            self.pbClearXsection.clicked.disconnect()
            self.pbUpdateAttributes.clicked.disconnect()
            self.pbCreateLayer.clicked.disconnect()
            self.pbUpdateLayer.clicked.disconnect()
            self.pbIncrementLayer.clicked.disconnect()
            # Spin boxes
            self.xSectionRowCount.valueChanged.disconnect()
            self.deckRowCount.valueChanged.disconnect()
            self.pierRowCount.valueChanged.disconnect()
            # Right Click (Context) Menus
            self.xSectionTableRowHeaders.customContextMenuRequested.disconnect()
            self.deckTableRowHeaders.customContextMenuRequested.disconnect()
            self.pierTableRowHeaders.customContextMenuRequested.disconnect()
            self.plotWdg.customContextMenuRequested.disconnect()
            # Other connections to tell the object that there has been an update
            self.bridgeName.textChanged.disconnect()
            self.deckElevationBottom.valueChanged.disconnect()
            self.deckThickness.valueChanged.disconnect()
            self.handRailDepth.valueChanged.disconnect()
            self.handRailFlc.valueChanged.disconnect()
            self.handRailBlockage.valueChanged.disconnect()
            self.rbDrowned.toggled.disconnect()
            self.pierNo.valueChanged.disconnect()
            self.pierWidth.valueChanged.disconnect()
            self.pierWidthLeft.valueChanged.disconnect()
            self.pierGap.valueChanged.disconnect()
            self.pierShape.currentIndexChanged.disconnect()
            self.zLineWidth.valueChanged.disconnect()
            self.enforceInTerrain.stateChanged.disconnect()
        
            self.buttonsConnected = False

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

    def browse(self):
        """
        Browse to user defined Empty File Directory
        
        :return:
        """
        
        outFile_old = None
        if len(self.emptydir.text()) > 0:
            outFile_old = self.outFile.text()
        settings = QSettings()
        lastFolder = str(settings.value("bridge_editor/emptydir", os.sep))
        if len(lastFolder) > 0:  # use last folder if stored
            fpath = lastFolder
        else:
            fpath = os.getcwd()
        outFile = QFileDialog.getExistingDirectory(None, "Empty Directory")
        if outFile is None or len(outFile) < 3 or outFile == os.sep or outFile == 'c:\\':
            if outFile_old is not None:
                self.emptydir.setText(outFile_old)
        else:
            settings.setValue("bridge_editor/emptydir", os.path.dirname(outFile))
            self.emptydir.setText(outFile)
    
    def startNewBridge(self):
        """
        Initiate new bridge class
        
        :return:
        """

        self.child_disconnect()
        self.bridge.clearXsection()
        self.checkBridgeExistsInFile()
        self.bridge = bridgeEditor(self, self.iface)
        self.child_connect()
        self.bridge.useTempPolyline()

    def checkForBridge(self):
        """
        Check for pre-existing bridge data
        
        :return:
        """
        
        self.cLyr = self.canvas.currentLayer()  # grab current layer when lyr is changed
        
        self.saveBridge()  # save changes to current bridge class object before loading new
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
                    lyrSource = lyr.dataProvider().dataSourceUri().split('|')[0]
                    inFile = '{0}.tbe'.format(os.path.splitext(lyrSource)[0])
                    if os.path.exists(inFile):
                        loadFile(self, inFile)
                    if bridgeKey in self.bridges.keys():
                        self.loadBridge(self.bridges[bridgeKey])
        
    def loadBridge(self, bridge):
        """
        Load saved and pre-existing bridge class object
        
        :param bridge: tuflowqgis_bridge_editor class object
        :return:
        """

        self.child_disconnect()
        self.bridge.gui = None
        self.checkBridgeExistsInFile()
        self.bridge = bridge
        self.bridge.loadGui(self)
        self.bridge.loadData()
        self.bridge.populateAttributes()
        self.child_connect()
    
    def checkBridgeExistsInFile(self):
        """
        Checks if current bridge editor object is saved somewhere, otherwise can be deleted from memory
        
        :return:
        """
        
        if len(self.bridges) > 0:
            for i, (key, item) in enumerate(self.bridges.items()):
                if item == self.bridge:  # don't delete current bridge object
                    break
                elif i + 1 == len(self.bridges):  # delete current bridge object so there's no phantom object in memory
                    del self.bridge
        else:
            del self.bridge
            
    def checkForBridgeFeature(self):
        """
        Checks to see if corresponding feature in map window still exists for bridge
        
        :return:
        """
        
        if len(self.bridges) > 0:
            for key, item in self.bridges.items():
                lyrName, fid = key.split(',')
                for i, (name, search_layer) in enumerate(QgsMapLayerRegistry.instance().mapLayers().items()):
                    if search_layer.name() == lyrName:
                        for j, f in enumerate(search_layer.getFeatures()):
                            if f.id() == int(fid):
                                break
                            elif j + 1 == search_layer.featureCount():
                                del self.bridges[key]
                    #elif i + 1 == len(QgsMapLayerRegistry.instance().mapLayers()):
                    #    del self.bridges[key]
    
    def incrementBridge(self, newLyr, oldLyr):
        """
        Increment the bridges dictionary object so that it has new layer name
        
        :param newLyr: string
        :param oldLyr: string
        :return:
        """
        
        for key, bridge in self.bridges.items():
            lyr, fid = key.split(',')
            if lyr == oldLyr:
                self.bridges['{0},{1}'.format(newLyr, fid)] = bridge
                del self.bridges[key]
        
    def saveBridge(self):
        """
        Save bridge editor class object to dictionary for quick access later
        
        :return:
        """

        if self.bridge.updated:
            lyr = self.bridge.layer
            
            
            if lyr is None:  # get lyr from key if needed
                for key, item in self.bridges.items():
                    if item == self.bridge:
                        lyrName, fid = key.split(',')
                        lyr = tuflowqgis_find_layer(lyrName)
                        break
            
            
            if lyr is not None:  # continue
                lyrName = lyr.name()
                feat = self.bridge.feature
                
                
                if feat is None:  # get feature from key if needed
                    for f in lyr.getFeatures():
                        x = f.id()
                        if f.id() == int(fid):
                            feat = f
                            break
                
                
                if feat is not None:  # continue
                    fid = feat.id()
                    self.bridge.saveData()
                    self.bridge.updated = False
                    self.bridges['{0},{1}'.format(lyrName, fid)] = self.bridge
                    self.checkForBridgeFeature()  # check if features have been deleted
                    saveFile(self)
