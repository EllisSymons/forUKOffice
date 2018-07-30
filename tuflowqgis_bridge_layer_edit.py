# coding=utf-8
from PyQt4.QtGui import *
from tuflowqgis_library import tuflowqgis_find_layer, tuflowqgis_import_empty_tf
from tuflowqgis_dialog import tuflowqgis_increment_dialog


def createLayer(bridge_editor):
	"""
	Import an empty 2d_lfcsh layer and add temp layer feature with attributes

	:return:
	"""
	
	# precheck to see if there is a feature to create
	if bridge_editor.feat is None:
		bridge_editor.bridge.statusLog.insertItem(0, 'Error: No features to create layer from')
		bridge_editor.bridge.statusLabel.setText('Status: Error')
		return
	# import empty file
	emptyTypes = ['2d_lfcsh']
	lines = True
	points = False
	regions = False
	if bridge_editor.variableGeom:
		points = True
	message = tuflowqgis_import_empty_tf(bridge_editor.iface, bridge_editor.bridge.emptydir.text(), bridge_editor.bridge.runId.text(), emptyTypes,
	                                     points, lines, regions)
	if message is not None:
		QMessageBox.critical(bridge_editor.iface.mainWindow(), "Importing TUFLOW Empty File(s)", message)
	# add features
	editLayer(bridge_editor, tuflowqgis_find_layer('2d_lfcsh_{0}_L'.format(bridge_editor.bridge.runId.text())), bridge_editor.feat, True)


def updateLayer(bridge_editor):
	"""
	Update the selected bridge layer with either updated attributes of selected feature, or add new feature

	:return:
	"""
	
	lyr = bridge_editor.iface.mapCanvas().currentLayer()  # QgsVectorLayer
	feat = lyr.selectedFeatures()  # list [QgsFeature]
	if bridge_editor.feat is None:
		if len(feat) > 0:
			editLayer(bridge_editor, lyr, feat[0], False)
		else:
			bridge_editor.bridge.statusLog.insertItem(0, 'Error: No edits to update')
			bridge_editor.bridge.statusLabel.setText('Status: Error')
	else:
		editLayer(bridge_editor, lyr, bridge_editor.feat, True)


def incrementLayer(bridge_editor):
	"""
	Increment layer then update with new feature or updated fields

	:return:
	"""
	
	# get current layer
	lyr = bridge_editor.iface.mapCanvas().currentLayer()  # QgsVectorLayer
	feat = lyr.selectedFeatures()  # QgsFeature
	if len(feat) > 0:
		fid = feat[0].id()
	# increment layer
	bridge_editor.incrementDialog = tuflowqgis_increment_dialog(bridge_editor.iface)
	bridge_editor.incrementDialog.exec_()
	# get new layer
	lyr = tuflowqgis_find_layer(bridge_editor.incrementDialog.outname)
	if len(feat) > 0:
		for feature in lyr.getFeatures():
			if feature.id() == fid:
				feat = feature
				break
			else:
				feat = None
	if bridge_editor.feat is None:
		if feat is not None:
			editLayer(bridge_editor, lyr, feat, False)
		else:
			bridge_editor.bridge.statusLog.insertItem(0, 'Error: No edits to update')
			bridge_editor.bridge.statusLabel.setText('Status: Error')
	else:
		editLayer(bridge_editor, lyr, bridge_editor.feat, True)


def editLayer(bridge_editor, layer, feat, append):
	"""
	edit layer with new feature or updated fields

	:param layer: QgsVectorLayer
	:param feat: QgsFeature
	:param append: bool - True for append to layer, false for don't append
	:return:
	"""
	
	dp = layer.dataProvider()
	attributes = [float(bridge_editor.bridge.invert.text()),
	              float(bridge_editor.bridge.dz.text()),
	              float(bridge_editor.bridge.shapeWidth.text()),
	              bridge_editor.bridge.shapeOptions.text(),
	              float(bridge_editor.bridge.layer1Obv.text()),
	              float(bridge_editor.bridge.layer1Block.text()),
	              float(bridge_editor.bridge.layer1Flc.text()),
	              float(bridge_editor.bridge.layer2Depth.text()),
	              float(bridge_editor.bridge.layer2Block.text()),
	              float(bridge_editor.bridge.layer2Flc.text()),
	              float(bridge_editor.bridge.layer3Depth.text()),
	              float(bridge_editor.bridge.layer3Block.text()),
	              float(bridge_editor.bridge.layer3Flc.text()),
	              bridge_editor.bridge.comment.text()]
	layer.startEditing()
	feat.setAttributes(attributes)
	if append:
		dp.addFeatures([feat])
	else:
		layer.updateFeature(feat)
	layer.commitChanges()
	# select created feature
	if append:
		layer.removeSelection()
		no_features = layer.featureCount()
		count = 1
		for f in layer.getFeatures():
			if count == no_features:
				bridge_editor.feature = f
				fid = f.id()
				layer.select(fid)
				break
			count += 1
	bridge_editor.canvas.scene().removeItem(bridge_editor.rubberBand)  # Remove previous temp layer
	bridge_editor.layer = layer
	bridge_editor.updated = True
	bridge_editor.saveData()
	bridge_editor.clearXsection()
	bridge_editor.feat = None
	layer.triggerRepaint()
	bridge_editor.bridge.statusLabel.setText('Status: Successful')
	bridge_editor.qgis_disconnect()
	bridge_editor.bridge = None