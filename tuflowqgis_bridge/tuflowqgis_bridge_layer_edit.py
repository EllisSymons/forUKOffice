# coding=utf-8
from PyQt4.QtGui import *
from tuflow.tuflowqgis_library import tuflowqgis_find_layer, tuflowqgis_import_empty_tf
from tuflow.tuflowqgis_dialog import tuflowqgis_increment_dialog


def createLayer(bridge_editor):
	"""
	Import an empty 2d_lfcsh layer and add temp layer feature with attributes

	:param bridge_editor: tuflowqgis_bridge_editor class object
	:return:
	"""
	
	# precheck to see if there is a feature to create
	if bridge_editor.feat is None:
		bridge_editor.gui.statusLog.insertItem(0, 'Error: No features to create layer from')
		bridge_editor.gui.statusLabel.setText('Status: Error')
		return
	# import empty file
	emptyTypes = ['2d_lfcsh']
	lines = True
	points = False
	regions = False
	if bridge_editor.variableGeom:
		points = True
	message = tuflowqgis_import_empty_tf(bridge_editor.iface, bridge_editor.gui.emptydir.text(), bridge_editor.gui.runId.text(), emptyTypes,
	                                     points, lines, regions)
	if message is not None:
		QMessageBox.critical(bridge_editor.iface.mainWindow(), "Importing TUFLOW Empty File(s)", message)
	# add features
	editLayer(bridge_editor, tuflowqgis_find_layer('2d_lfcsh_{0}_L'.format(bridge_editor.gui.runId.text())), bridge_editor.feat, True, False)


def updateLayer(bridge_editor):
	"""
	Update the selected bridge layer with either updated attributes of selected feature, or add new feature

	:param bridge_editor: tuflowqgis_bridge_editor class object
	:return:
	"""
	
	lyr = bridge_editor.iface.mapCanvas().currentLayer()  # QgsVectorLayer
	feat = lyr.selectedFeatures()  # list [QgsFeature]
	if bridge_editor.feat is None:
		if len(feat) > 0:
			editLayer(bridge_editor, lyr, feat[0], False, False)
		else:
			bridge_editor.gui.statusLog.insertItem(0, 'Error: No edits to update')
			bridge_editor.gui.statusLabel.setText('Status: Error')
	else:
		editLayer(bridge_editor, lyr, bridge_editor.feat, True, False)


def incrementLayer(bridge_editor):
	"""
	Increment layer then update with new feature or updated fields

	:param bridge_editor: tuflowqgis_bridge_editor class object
	:return:
	"""
	
	# get current layer
	lyr = bridge_editor.iface.mapCanvas().currentLayer()  # QgsVectorLayer
	lyrName = lyr.name()
	feat = lyr.selectedFeatures()  # QgsFeature
	if len(feat) > 0:
		fid = feat[0].id()
	# increment layer
	bridge_editor.incrementDialog = tuflowqgis_increment_dialog(bridge_editor.iface)
	bridge_editor.incrementDialog.exec_()
	# get new layer
	newLyr = tuflowqgis_find_layer(bridge_editor.incrementDialog.outname)
	if len(feat) > 0:
		for feature in newLyr.getFeatures():
			if feature.id() == fid:
				feat = feature
				break
			else:
				feat = None
	if bridge_editor.feat is None:
		if feat is not None:
			editLayer(bridge_editor, newLyr, feat, False, True, old_lyr_name=lyrName)
		else:
			bridge_editor.gui.statusLog.insertItem(0, 'Error: No edits to update')
			bridge_editor.gui.statusLabel.setText('Status: Error')
	else:
		editLayer(bridge_editor, newLyr, bridge_editor.feat, True, True, old_lyr_name=lyrName)


def editLayer(bridge_editor, layer, feat, append, increment, **kwargs):
	"""
	edit layer with new feature or updated fields

	:param bridge_editor: tuflowqgis_bridge_editor class object
	:param layer: QgsVectorLayer
	:param feat: QgsFeature
	:param append: bool - True for append to layer, false for don't append
	:param increment: bool - True if the layer has been incremented
	:return:
	"""
	
	dp = layer.dataProvider()
	attributes = [float(bridge_editor.gui.invert.text()),
	              float(bridge_editor.gui.dz.text()),
	              float(bridge_editor.gui.shapeWidth.text()),
	              bridge_editor.gui.shapeOptions.text(),
	              float(bridge_editor.gui.layer1Obv.text()),
	              float(bridge_editor.gui.layer1Block.text()),
	              float(bridge_editor.gui.layer1Flc.text()),
	              float(bridge_editor.gui.layer2Depth.text()),
	              float(bridge_editor.gui.layer2Block.text()),
	              float(bridge_editor.gui.layer2Flc.text()),
	              float(bridge_editor.gui.layer3Depth.text()),
	              float(bridge_editor.gui.layer3Block.text()),
	              float(bridge_editor.gui.layer3Flc.text()),
	              bridge_editor.gui.comment.text()]
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
	if increment:  # rewrite the dictionary to refer to new layer
		oldLyrName = kwargs['old_lyr_name']
		bridge_editor.gui.incrementBridge(layer.name(), oldLyrName)
	bridge_editor.gui.statusLabel.setText('Status: Successful')
	bridge_editor.qgis_disconnect()
	bridge_editor.gui = None