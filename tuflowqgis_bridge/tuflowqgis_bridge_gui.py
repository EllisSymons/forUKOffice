# coding=utf-8
from tuflowqgis_bridge_editor import *
from tuflowqgis_bridge_filehandler import *
from tuflow.tuflowqgis_library import findAllRasterLyrs
import sys
import cPickle
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
        self.bridge = bridgeEditor(self, self.iface)
        self.qgis_connect()

    def qgis_connect(self):
        """
        Set up signal connections.

        :return: void
        """
    
        if not self.connected:
            self.canvas.layersChanged.connect(self.populateDems)
            self.canvas.layersChanged.connect(self.checkForBridge)
            self.canvas.currentLayerChanged.connect(self.checkForBridge)
            self.canvas.selectionChanged.connect(self.checkForBridge)
            self.pbDrawXsection.clicked.connect(self.startNewBridge)
            self.pbSaveFile.clicked.connect(lambda: saveFile(self))
            self.connected = True

    def qgis_disconnect(self):
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
        
        self.bridge.clearXsection()
        self.bridge.qgis_disconnect()
        self.bridge = bridgeEditor(self, self.iface)
        self.bridge.useTempPolyline()

    def checkForBridge(self):
        """
        Check for pre-existing bridge data
        
        :return:
        """

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
                    inFile = '{0}.tuflowbridge'.format(os.path.splitext(lyrSource)[0])
                    if os.path.exists(inFile):
                        loadFile(self, inFile)
                    if bridgeKey in self.bridges.keys():
                        self.loadBridge(self.bridges[bridgeKey])
        
    def loadBridge(self, bridge):
        """
        Load saved and pre-existing bridge class object
        
        :param bridge: tuflowqgis_bridge_editor clas object
        :return:
        """
        
        self.bridge.qgis_disconnect()
        self.bridge.gui = None
        self.bridge = bridge
        self.bridge.loadGui(self)
        self.bridge.loadData()
        self.bridge.populateAttributes()
    
    def newBridge(self):
        self.bridge = bridgeEditor(self, self.iface)
        
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
            lyrName = lyr.name()
            feat = self.bridge.feature
            fid = feat.id()
            self.bridge.updated = False
            self.bridges['{0},{1}'.format(lyrName, fid)] = self.bridge
            self.new_bridge = False
            
