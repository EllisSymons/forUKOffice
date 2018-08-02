# coding=utf-8
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *


def mouseTrackConnect(bridge_editor):
	"""
	Captures signals from the custom map tool
	
	:param bridge_editor: tuflowqgis_bridge_editor class object
	:return:
	"""

	if not bridge_editor.cursorTrackingConnected:
		bridge_editor.cursorTrackingConnected = True
		QApplication.setOverrideCursor(Qt.CrossCursor)
		bridge_editor.tempPolyline.moved.connect(lambda pos: moved(bridge_editor, pos))
		bridge_editor.tempPolyline.rightClicked.connect(lambda pos: rightClick(bridge_editor, pos))
		bridge_editor.tempPolyline.leftClicked.connect(lambda pos: leftClick(bridge_editor, pos))
		bridge_editor.canvas.keyPressed.connect(lambda key: escape(bridge_editor, key))


def mouseTrackDisconnect(bridge_editor):
	"""
	Turn off capturing of the custom map tool
	
	:param bridge_editor: tuflowqgis_bridge_editor class object
	:return:
	"""
	
	if bridge_editor.cursorTrackingConnected:
		bridge_editor.cursorTrackingConnected = False
		QApplication.restoreOverrideCursor()
		bridge_editor.tempPolyline.moved.disconnect()
		bridge_editor.tempPolyline.rightClicked.disconnect()
		bridge_editor.tempPolyline.leftClicked.disconnect()
		bridge_editor.canvas.keyPressed.disconnect()


def moved(bridge_editor, position):
	"""
	Signal sent when cursor is moved on the map canvas

	:param bridge_editor: tuflowqgis_bridge_editor class object
	:param position: dict event signal position
	:return: void
	"""
	
	x = position['x']
	y = position['y']
	point = bridge_editor.canvas.getCoordinateTransform().toMapCoordinates(x, y)
	if bridge_editor.points:
		try:  # QGIS 2
			if QGis.QGIS_VERSION >= 10900:
				bridge_editor.rubberBand.reset(QGis.Line)
			else:
				bridge_editor.rubberBand.reset(False)
		except:  # QGIS 3
			bridge_editor.rubberBand.reset(QgsWkbTypes.LineGeometry)
		# self.points.pop()
		# self.points.append(point)
		bridge_editor.rubberBand.setToGeometry(QgsGeometry.fromPolyline(bridge_editor.points), None)
		bridge_editor.rubberBand.addPoint(point)


def leftClick(bridge_editor, position):
	"""
	Signal sent when canvas is left clicked

	:param bridge_editor: tuflowqgis_bridge_editor class object
	:param position: dict event signal position
	:return: void
	"""
	
	x = position['x']
	y = position['y']
	point = bridge_editor.canvas.getCoordinateTransform().toMapCoordinates(x, y)
	bridge_editor.points.append(point)
	bridge_editor.rubberBand.addPoint(point)


def rightClick(bridge_editor, position):
	"""
	Signal sent when canvas is right clicked

	:param bridge_editor: tuflowqgis_bridge_editor class object
	:param position: dict event signal position
	:return: void

	:param position:
	:return:
	"""
	
	bridge_editor.rubberBand.setToGeometry(QgsGeometry.fromPolyline(bridge_editor.points), None)
	mouseTrackDisconnect(bridge_editor)
	bridge_editor.createMemoryLayerFromTempLayer()


def escape(bridge_editor, key):
	"""
	Signal sent when a key is pressed in qgis. Will cancel the line if escape is pressed

	:param bridge_editor: tuflowqgis_bridge_editor class object
	:param key: QKeyEvent
	:return:
	"""
	
	# QMessageBox.information(self.iface.mainWindow(), "debug", "{0}".format(key.key()))
	if key.key() == 16777216:  # Escape key
		bridge_editor.canvas.scene().removeItem(bridge_editor.rubberBand)  # Remove previous temp layer
		mouseTrackDisconnect(bridge_editor)