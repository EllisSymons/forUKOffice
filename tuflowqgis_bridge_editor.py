from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui
from qgis.core import *
import sys
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.patches import Patch
from matplotlib.patches import Polygon
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
import numpy
from tuflowqgis_library import *
import tuflowqgis_dialog
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
        self.connected = False
        self.connect()
        self.populateDems()
        self.initialisePlot()

    def __del__(self):
        self.qgis_disconnect()

    def connect(self):
        if not self.connected:
            self.pbUpdate.clicked.connect(self.updatePlot)
            self.pbUpdate.clicked.connect(lambda: self.updateTable(self.XSectionTable, 0))
            self.iface.currentLayerChanged.connect(self.populateDems)
            self.connected = True

    def disconnect(self):
        if self.connected:
            self.pbUpdate.clicked.disconnect(self.updatePlot)
            self.pbUpdate.clicked.disconnect(lambda: self.updateTable(self.XSectionTable, 0))
            self.iface.currentLayerChanged.disconnect(self.populateDems)
            self.connected = False

    def initialisePlot(self):
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
        axe1.grid()
        axe1.tick_params(axis="both", which="major", direction="out", length=10, width=1, bottom=True, top=False,
                         left=True, right=False)
        axe1.minorticks_on()
        axe1.tick_params(axis="both", which="minor", direction="out", length=5, width=1, bottom=True, top=False,
                         left=True, right=False)

    def populateDems(self):
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

    def updateTable(self, tableWidget, data):
        tableWidget.setRowCount(5)

    def updatePlot(self):
        self.fig.tight_layout()
        self.plotWdg.draw()