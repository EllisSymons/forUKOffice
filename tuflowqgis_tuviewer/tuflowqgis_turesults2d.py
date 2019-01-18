import os
import sys
from datetime import datetime, timedelta
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from qgis.core import *
from PyQt5.QtWidgets import *
from qgis.PyQt.QtXml import QDomDocument
from tuflow.tuflowqgis_tuviewer.tuflowqgis_turesultsindex import TuResultsIndex
from tuflow.tuflowqgis_library import tuflowqgis_find_layer, findAllMeshLyrs, loadSetting, roundSeconds, \
	getPropertiesFrom2dm



class TuResults2D():
	"""
	Class for handling 2D results
	
	"""
	
	def __init__(self, TuView):
		self.tuView = TuView
		self.iface = TuView.iface
		self.rsScalar = QgsMeshRendererScalarSettings()
		self.rsVector = QgsMeshRendererVectorSettings()
		self.activeMeshLayers = []  # list of selected QgsMeshLayer (layer.type() == 3)
		self.activeScalar = None  # active scalar to be rendered e.g. depth
		self.activeVector = None  # active vector to be rendered e.g. velocity vector
		self.activeDatasets = []  # list of active result datasets including time series and long plots
		self.activeScalar, self.activeVector = None, None
		self.meshProperties = {}
		self.results2d = {}  # holds 2d properties e.g. 'path'
	
	def importResults(self, inFileNames):
		"""
		Imports function that opens result mesh layer

		:param inFileNames: list -> str - full path to mesh result file
		:return: bool -> True for successful, False for unsuccessful
		"""

		self.tuView.project.layersAdded.disconnect(self.tuView.layersAdded)

		for j, f in enumerate(inFileNames):

			# Load Mesh
			if type(inFileNames) is dict:  # being loaded in from a sup file
				m = inFileNames[f]['mesh']
				mLayer, name, preExisting = self.loadMeshLayer(m, name=f)
			else:
				mLayer, name, preExisting = self.loadMeshLayer(f)
			if mLayer is None or name is None:
				self.tuView.project.layersAdded.connect(self.tuView.layersAdded)
				return False
			
			# Load Results
			if type(inFileNames) is dict:  # being loaded in from a sup file
				datasets = inFileNames[f]['datasets']
				for d in datasets:
					l = self.loadDataGroup(d, mLayer, preExisting)
			else:
				loaded = self.loadDataGroup(f, mLayer, preExisting)
			#res = {'path': f}
			#self.results2d[mLayer.name()] = res
			
			# Open layer in map
			self.tuView.project.addMapLayer(mLayer)
			name = mLayer.name()
			mLayer.nameChanged.connect(lambda: self.layerNameChanged(mLayer, name, mLayer.name()))  # if name is changed can capture this in indexing
			
			rs = mLayer.rendererSettings()
			rsMesh = rs.nativeMeshSettings()
			rsMesh.setEnabled(self.tuView.tuOptions.showGrid)
			rs.setNativeMeshSettings(rsMesh)
			mLayer.setRendererSettings(rs)
			#mLayer.repaintRequested.connect(lambda: self.tuView.repaintRequested(mLayer))
			
			# Index results
			ext = os.path.splitext(f)[-1]  # added because .dat scalar and vector need to be combined
			index = self.getResultMetaData(name, mLayer, ext)
			if not index:
				self.tuView.project.layersAdded.connect(self.tuView.layersAdded)
				return False
			
			# add to result list widget
			names = []
			for i in range(self.tuView.OpenResults.count()):
				if self.tuView.OpenResults.item(i).text() not in names:
					names.append(self.tuView.OpenResults.item(i).text())
			if name not in names:
				self.tuView.OpenResults.addItem(name)  # add to widget
			k = self.tuView.OpenResults.findItems(name, Qt.MatchRecursive)[0]
			k.setSelected(True)
			updated = self.updateActiveMeshLayers()  # update list of active mesh layers
			if not updated:
				self.tuView.project.layersAdded.connect(self.tuView.layersAdded)
				return False
			self.tuView.resultChangeSignalCount = 0  # reset signal count back to 0
			
		self.tuView.project.layersAdded.connect(self.tuView.layersAdded)
			
		return True
		
	def loadMeshLayer(self, fpath, **kwargs):
		"""
		Load the mesh layer i.e. .xmdf

		:param fpath: str
		:return: QgsMeshLayer
		:return: str
		"""
		
		# deal with kwargs
		name = kwargs['name'] if 'name' in kwargs else None

		# Parse out file names
		basepath, fext = os.path.splitext(fpath)
		basename = os.path.basename(basepath)
		dirname = os.path.dirname(basepath)
		if fext.lower() == '.xmdf' or fext.lower() == '.dat' or fext.lower() == '.2dm':
			mesh = '{0}.2dm'.format(basepath)
			while not os.path.exists(mesh):  # put in for res_to_res results e.g. M01_5m_002_V_va.xmdf (velocity angle)
				components = basename.split('_')
				components.pop()
				if not components:
					break
				basename = '_'.join(components)
				mesh = '{0}.2dm'.format(os.path.join(dirname, basename))
			if not os.path.exists(mesh):
				# ask user for location
				inFileNames = QFileDialog.getOpenFileNames(self.tuView.iface.mainWindow(), 'Mesh file location', fpath,
				                                           "TUFLOW Mesh File (*.2dm)")
				if not inFileNames[0]:  # empty list
					return None, None, False
				else:
					if os.path.exists(inFileNames[0][0]):
						mesh = inFileNames[0][0]
					else:
						QMessageBox.information(self.iface, "TUVIEW", "Could not find mesh file")
						return None, None, False
		else:
			QMessageBox.information(self.iface, "TUVIEW", "Must select a .xmdf .dat or .2dm file type")
			return None, None, False
		
		# does mesh layer already exist in workspace
		layer = tuflowqgis_find_layer(basename)
		if layer is not None:
			return layer, basename, True
		
		# Load mesh if layer does not exist already
		name = basename if name is None else name
		layer = QgsMeshLayer(mesh, name, 'mdal')
		if layer.isValid():
			prop = {}
			cellSize, wllVerticalOffset, origin, orientation, gridSize = getPropertiesFrom2dm(mesh)
			prop['cell size'] = cellSize
			prop['wll vertical offset'] = wllVerticalOffset
			prop['origin'] = origin
			prop['orientation'] = orientation
			prop['grid size'] = gridSize
			self.meshProperties[name] = prop
			self.tuView.tuOptions.resolution = cellSize
			return layer, name, False
		
		QMessageBox.information(self.iface, "TUVIEW", "Could not load mesh file")
		return None, None, False
	
	def loadDataGroup(self, fpath, layer, preExisting):
		"""
		Add results to mesh layer

		:param fpath: str
		:param layer: QgsMeshLayer
		:param preExisting: bool -> if the mesh is pre-existingi in workspace
		:return: bool -> True for successful, False for unsuccessful
		"""
		
		# Parse out file names
		basepath, fext = os.path.splitext(fpath)
		basename = os.path.basename(basepath)
		mesh = '{0}.2dm'.format(basepath)
		if fext.lower() == '.xmdf' or fext.lower() == '.dat':
			dataGroup = fpath
		else:
			return False  # No datasets loaded because extension not recognised
		
		# check if datagroup has already been loaded
		if preExisting:
			if layer.dataProvider().datasetGroupCount() > 1:
				if fext.lower() == '.xmdf':
					# return False  # most likely already loaded
					pass  # better off leaving this until better logic is possible
					
		# load results onto mesh
		dp = layer.dataProvider()
		try:
			dp.addDataset(dataGroup)
			return True  # successful
		except:
			return False  # unsuccessful
		
	def getDatasetGroupTypes(self, layer):
		"""
		Collects dataset group types i.e. depth. Will ignore Bed Elevation. Will accept both file path or QgsMeshLayer
		
		:param layer: QgsMeshLayer or str -> mesh location i.e. .xmdf
		:return: list -> str types
		"""
		
		types = []
		
		if type(layer) == QgsMeshLayer:
			for i in range(layer.dataProvider().datasetGroupCount()):
				groupName = layer.dataProvider().datasetGroupMetadata(i).name()
				if groupName.lower() != 'bed elevation':
					types.append(groupName)
					
		elif type(layer) == str:
			# load mesh layer
			mLayer, basename, preExisting = self.loadMeshLayer(layer)
			# load dataset group assuming it's not pre-existing
			self.loadDataGroup(layer, mLayer, False)
			# loop through dataset groups as per above loop
			for i in range(mLayer.dataProvider().datasetGroupCount()):
				groupName = mLayer.dataProvider().datasetGroupMetadata(i).name()
				if groupName.lower() != 'bed elevation':
					types.append(groupName)
					
		return types
	
	def getResultMetaData(self, name, layer, ext=''):
		"""
		Get all the result types and timesteps for 2D results.

		:param layer: QgsMeshLayer
		:return: bool -> True for successful, False for unsuccessful
		"""

		results = self.tuView.tuResults.results  # dict
		timekey2time = self.tuView.tuResults.timekey2time  # dict
		timekey2date = self.tuView.tuResults.timekey2date  # dict
		time2date = self.tuView.tuResults.time2date  # dict
		date2timekey = self.tuView.tuResults.date2timekey  # dict
		date2time = self.tuView.tuResults.date2time  # dict
		zeroTime = self.tuView.tuOptions.zeroTime
		
		if name not in results.keys():  # add results to dict
			results[name] = {}
		
		timesteps, maxResultTypes, temporalResultTypes = [], [], []
		dp = layer.dataProvider()  # QgsMeshDataProvider
		
		for i in range(dp.datasetGroupCount()):
			
			# Get result type e.g. depth, velocity, max depth
			mdGroup = dp.datasetGroupMetadata(i)  # Group Metadata
			if mdGroup.isScalar() or ext.upper() == '.DAT':
				type = 1
			else:
				type = 2
			if '/Maximums' in mdGroup.name():
				if mdGroup.name() not in maxResultTypes:
					
					# add to max result type list
					maxResultTypes.append(mdGroup.name().split('/')[0])
					
					# initiate in results dict
					results[name][mdGroup.name()] = {}  # add result type to results dictionary
					
					# add max result as time -99999
					results[name][mdGroup.name()]['-99999'] = (-99999, type, QgsMeshDatasetIndex(i, 0))
					timekey2time['-99999'] = -99999
					timekey2date['-99999'] = -99999
					time2date['-99999'] = -99999
					date2timekey[-99999] = '-99999'
					date2time[-99999] = '-99999'
					
					# apply any default rendering styles to datagroup
					if mdGroup.isScalar() or ext.upper() == '.DAT':
						resultType = mdGroup.name().split('/')[0]
						# try finding if style has been saved as a ramp first
						key = 'TUFLOW_scalarRenderer/{0}_ramp'.format(resultType)
						file = QSettings().value(key)
						if file:
							self.applyScalarRenderSettings(layer, i, file, type='ramp')
						# else try map
						key = 'TUFLOW_scalarRenderer/{0}_map'.format(resultType)
						file = QSettings().value(key)
						if file:
							self.applyScalarRenderSettings(layer, i, file, type='map')
					if mdGroup.isVector():
						vectorProperties = QSettings().value('TUFLOW_vectorRenderer/vector')
						if vectorProperties:
							self.applyVectorRenderSettings(layer, i, vectorProperties)
						
			else:
				if mdGroup.name() not in temporalResultTypes:
					
					# add to temporal result type list
					if ext.upper() == '.DAT' and mdGroup.isVector():  # because dat files need to load in as both vector and scalar
						temporalResultTypes.append('{0} Vector'.format(mdGroup.name()))
						temporalResultTypes.append(mdGroup.name())
					else:
						temporalResultTypes.append(mdGroup.name())
					
					# initiate in result dict
					if ext.upper() == '.DAT' and mdGroup.isVector():  # because dat files need to load in as both vector and scalar
						results[name][mdGroup.name()] = {}
						results[name]['{0} Vector'.format(mdGroup.name())] = {}
					else:
						results[name][mdGroup.name()] = {}  # add result type to results dictionary
					
					# apply any default rendering styles to datagroup
					if mdGroup.isScalar() or ext.upper() == '.DAT':
						resultType = mdGroup.name()
						# try finding if style has been saved as a ramp first
						key = 'TUFLOW_scalarRenderer/{0}_ramp'.format(resultType)
						file = QSettings().value(key)
						if file:
							self.applyScalarRenderSettings(layer, i, file, type='ramp')
						# else try map
						key = 'TUFLOW_scalarRenderer/{0}_map'.format(resultType)
						file = QSettings().value(key)
						if file:
							self.applyScalarRenderSettings(layer, i, file, type='map')
					if mdGroup.isVector():
						vectorProperties = QSettings().value('TUFLOW_vectorRenderer/vector')
						if vectorProperties:
							self.applyVectorRenderSettings(layer, i, vectorProperties)
				
				# Get timesteps
				if not timesteps:  # only if not populated yet
					for j in range(dp.datasetCount(i)):
						md = dp.datasetMetadata(QgsMeshDatasetIndex(i, j))  # metadata for individual timestep
						timesteps.append(md.time())  # only difference between this and below code block
						results[name][mdGroup.name()]['{0:.4f}'.format(md.time())] = \
							(md.time(), type, QgsMeshDatasetIndex(i, j))  # add result index to results dict
						timekey2time['{0:.4f}'.format(md.time())] = md.time()
						date = zeroTime + timedelta(hours=md.time())
						date = roundSeconds(date)
						timekey2date['{0:.4f}'.format(md.time())] = date
						time2date[md.time()] = date
						date2timekey[date] = '{0:.4f}'.format(md.time())
						date2time[date] = md.time()
						if ext.upper() == '.DAT' and mdGroup.isVector():  # need to add result type again as vector type
							md = dp.datasetMetadata(QgsMeshDatasetIndex(i, j))  # metadata for individual timestep
							timesteps.append(md.time())  # only difference between this and below code block
							results[name]['{0} Vector'.format(mdGroup.name())]['{0:.4f}'.format(md.time())] = \
								(md.time(), 2, QgsMeshDatasetIndex(i, j))  # add result index to results dict
							timekey2time['{0:.4f}'.format(md.time())] = md.time()
							date = zeroTime + timedelta(hours=md.time())
							date = roundSeconds(date)
							timekey2date['{0:.4f}'.format(md.time())] = date
							time2date[md.time()] = date
							date2timekey[date] = '{0:.4f}'.format(md.time())
							date2time[date] = md.time()
				else:
					for j in range(dp.datasetCount(i)):
						md = dp.datasetMetadata(QgsMeshDatasetIndex(i, j))  # metadata for individual timestep
						results[name][mdGroup.name()]['{0:.4f}'.format(md.time())] = \
							(md.time(), type, QgsMeshDatasetIndex(i, j))  # add result index to results dict
						timekey2time['{0:.4f}'.format(md.time())] = md.time()
						date = zeroTime + timedelta(hours=md.time())
						date = roundSeconds(date)
						timekey2date['{0:.4f}'.format(md.time())] = date
						time2date[md.time()] = date
						date2timekey[date] = '{0:.4f}'.format(md.time())
						date2time[date] = md.time()
						if ext.upper() == '.DAT' and mdGroup.isVector():  # need to add result type again as vector type
							md = dp.datasetMetadata(QgsMeshDatasetIndex(i, j))  # metadata for individual timestep
							results[name]['{0} Vector'.format(mdGroup.name())]['{0:.4f}'.format(md.time())] = \
								(md.time(), 2, QgsMeshDatasetIndex(i, j))  # add result index to results dict
							timekey2time['{0:.4f}'.format(md.time())] = md.time()
							date = zeroTime + timedelta(hours=md.time())
							date = roundSeconds(date)
							timekey2date['{0:.4f}'.format(md.time())] = date
							time2date[md.time()] = date
							date2timekey[date] = '{0:.4f}'.format(md.time())
							date2time[date] = md.time()
							
						
		return True
	
	def updateActiveMeshLayers(self):
		"""
		Updates the list of selected 2D results.
		
		:return: bool -> True for successful, False for unsuccessful
		"""
		
		self.activeMeshLayers = []
		openResults = self.tuView.OpenResults  # QListWidget
		
		for r in range(openResults.count()):
			item = openResults.item(r)
			
			# find selected layer
			layer = tuflowqgis_find_layer(item.text())
			if layer is not None:
				if layer.type() == 3:
					if item.isSelected():
						self.activeMeshLayers.append(layer)
					else:
						rs = layer.rendererSettings()
						rs.setActiveScalarDataset(QgsMeshDatasetIndex(-1, -1))
						layer.setRendererSettings(rs)
						rs.setActiveVectorDataset(QgsMeshDatasetIndex(-1, -1))
						layer.setRendererSettings(rs)
		
		return True
	
	
	def renderMap(self):
		"""
		Renders the active scalar and vector layers.
		
		:return: bool -> True for successful, False for unsuccessful
		"""

		for layer in self.activeMeshLayers:
			
			rs = layer.rendererSettings()
			
			# Get result index
			activeScalarIndex = TuResultsIndex(layer.name(), self.activeScalar,
			                                   self.tuView.tuResults.activeTime, self.tuView.tuResults.isMax('scalar'))
			activeVectorIndex = TuResultsIndex(layer.name(), self.activeVector,
			                                   self.tuView.tuResults.activeTime, self.tuView.tuResults.isMax('vector'))
			
			# Get QgsMeshLayerIndex from result index
			activeScalarMeshIndex = self.tuView.tuResults.getResult(activeScalarIndex, force_get_time='next lower')
			activeVectorMeshIndex = self.tuView.tuResults.getResult(activeVectorIndex, force_get_time='next lower')
			
			# render results
			if activeScalarMeshIndex and type(activeScalarMeshIndex) == tuple:
				rs.setActiveScalarDataset(activeScalarMeshIndex[-1])
				layer.setRendererSettings(rs)
			if activeVectorMeshIndex and type(activeVectorMeshIndex) == tuple:
				rs.setActiveVectorDataset(activeVectorMeshIndex[-1])
				layer.setRendererSettings(rs)
				
			# turn on / off mesh and triangles
			if rs.nativeMeshSettings().isEnabled() != self.tuView.tuOptions.showGrid:
				rsMesh = rs.nativeMeshSettings()
				rsMesh.setEnabled(self.tuView.tuOptions.showGrid)
				rs.setNativeMeshSettings(rsMesh)
				layer.setRendererSettings(rs)
			self.tuView.tuPlot.tuPlotToolbar.meshGridAction.setChecked(self.tuView.tuOptions.showGrid)
			if rs.triangularMeshSettings().isEnabled() != self.tuView.tuOptions.showTriangles:
				rsTriangles = rs.triangularMeshSettings()
				rsTriangles.setEnabled(self.tuView.tuOptions.showTriangles)
				rs.setTriangularMeshSettings(rsTriangles)
				layer.setRendererSettings(rs)
		
		# disconnect map canvas refresh if it is connected - used for rendering after loading from project
		try:
			self.tuView.canvas.mapCanvasRefreshed.disconnect(self.renderMap)
		except:
			pass
			
		return True
	
	def removeResults(self, resList):
		"""
		Removes the 2D results from the indexed results and ui.
		
		:param resList: list -> str result name e.g. M01_5m_001
		:return: bool -> True for successful, False for unsuccessful
		"""
		
		results = self.tuView.tuResults.results

		for res in resList:
			if res in results.keys():
				# remove from indexed results
				for resultType in list(results[res].keys()):
					if '_ts' not in resultType and '_lp' not in resultType:
						del results[res][resultType]

				# remove from map
				#layer = tuflowqgis_find_layer(res)
				#self.tuView.project.removeMapLayer(layer)
				#self.tuView.canvas.refresh()
				
				# check if result type is now empty
				if len(results[res]) == 0:
					del results[res]
					for i in range(self.tuView.OpenResults.count()):
						item = self.tuView.OpenResults.item(i)
						if item is not None and item.text() == res:
							self.tuView.OpenResults.takeItem(i)
						
		return True
	
	def loadOpenMeshLayers(self, **kwargs):
		"""
		Checks the workspace for already open mesh layers and adds datasets to mesh and loads into interface.
		
		:return: bool -> True for successful, False for unsuccessful
		"""
		
		layer = kwargs['layer'] if 'layer' in kwargs.keys() else None
		
		if layer:
			meshLayers = [layer]
		else:
			meshLayers = findAllMeshLyrs()
		
		for ml in meshLayers:
			layer = tuflowqgis_find_layer(ml)
			if layer is not None:
				mesh = layer.source()
				
				# check for xmdf
				xmdf = '{0}.xmdf'.format(os.path.splitext(mesh)[0])
				results2D = []
				if os.path.exists(xmdf):
					results2D.append(xmdf)
				# check for dat
				else:
					outputFolder2D = os.path.dirname(mesh)
					if os.path.exists(outputFolder2D):
						for file in os.listdir(outputFolder2D):
							name, ext = os.path.splitext(file)
							# name = os.path.basename(f)
							if ext.lower() == '.dat' and ml.lower() in name.lower():
								results2D.append(os.path.join(outputFolder2D, file))
				
				loaded = self.tuView.tuMenuBar.tuMenuFunctions.load2dResults(result_2D=[results2D])
				
				# if not loaded it may mean that results are already loaded in so index results and add to gui, else at least load in bed elevation
				if not loaded:
					self.getResultMetaData(layer)
					self.tuView.OpenResults.addItem(ml)

	def applyScalarRenderSettings(self, layer, datasetGroupIndex, file, type, save_type='xml'):
		"""
		Applies scalar renderer settings to a datagroup based on a color ramp properties.
		
		:param layer: QgsMeshLayer
		:param datasetGroupIndex: int
		:param file: str
		:param type: str -> 'ramp'
						    'map'
		:return: bool -> True for successful, False for unsuccessful
		"""

		rs = layer.rendererSettings()
		rsScalar = rs.scalarSettings(datasetGroupIndex)
		
		if type == 'ramp':
			minValue = rsScalar.colorRampShader().colorRampItemList()[0].value
			maxValue = rsScalar.colorRampShader().colorRampItemList()[-1].value
			shader = rsScalar.colorRampShader()
			doc = QDomDocument()
			xml = QFile(file)
			statusOK, errorStr, errorLine, errorColumn = doc.setContent(xml, True)
			if statusOK:
				element = doc.documentElement()
				shader.readXml(element)
				shader.setMinimumValue(minValue)
				shader.setMaximumValue(maxValue)
				shader.setColorRampType(0)
				shader.classifyColorRamp(5, -1, QgsRectangle(), None)
				rsScalar.setColorRampShader(shader)
			else:
				return False
		elif type == 'map':
			doc = QDomDocument()
			xml = QFile(file) if save_type == 'xml' else file
			statusOK, errorStr, errorLine, errorColumn = doc.setContent(xml, True)
			if statusOK:
				element = doc.documentElement()
				rsScalar.readXml(element)
			else:
				return False
		else:
			return False
			
		rs.setScalarSettings(datasetGroupIndex, rsScalar)
		layer.setRendererSettings(rs)
		
		return True
	
	def applyVectorRenderSettings(self, layer, datasetGroupIndex, vectorProperties):
		"""
		Applies vector renderer settings to a vector datset group based on vector properties.
		
		:param layer: QgsMeshLayer
		:param datasetGroupIndex: int
		:param vectorProperties: dict
		:return: bool -> True for successful, False for unsuccessful
		"""
		
		rs = layer.rendererSettings()
		rsVector = rs.vectorSettings(datasetGroupIndex)
		
		rsVector.setArrowHeadLengthRatio(vectorProperties['arrow head length ratio'])
		rsVector.setArrowHeadWidthRatio(vectorProperties['arrow head width ratio'])
		rsVector.setColor(vectorProperties['color'])
		rsVector.setFilterMax(vectorProperties['filter max'])
		rsVector.setFilterMin(vectorProperties['filter min'])
		rsVector.setLineWidth(vectorProperties['line width'])
		
		method = vectorProperties['shaft length method']
		rsVector.setShaftLengthMethod(method)
		
		if method == 0:  # min max
			rsVector.setMaxShaftLength(vectorProperties['max shaft length'])
			rsVector.setMinShaftLength(vectorProperties['min shaft length'])
		elif method == 1:  # scaled
			rsVector.setScaleFactor(vectorProperties['scale factor'])
		elif method == 2:  # fixed
			rsVector.setFixedShaftLength(vectorProperties['fixed shaft length'])
		else:
			return False
		
		rs.setVectorSettings(datasetGroupIndex, rsVector)
		layer.setRendererSettings(rs)
		
		return True
	
	def layerNameChanged(self, layer, oldName, newName):
		"""
		
		
		:param layer:
		:return:
		"""
		
		layer.nameChanged.disconnect()
		
		# change name in list widget
		selectedItems = self.tuView.OpenResults.selectedItems()
		for i in range(self.tuView.OpenResults.count()):
			item = self.tuView.OpenResults.item(i)
			if item.text() == oldName:
				self.tuView.OpenResults.takeItem(i)
				self.tuView.OpenResults.insertItem(i, newName)
				if item in selectedItems:
					self.tuView.OpenResults.item(i).setSelected(True)
					
		# change name in results dict
		results = self.tuView.tuResults.results
		for key, entry in results.items():
			if key == oldName:
				results[newName] = entry
				del results[oldName]
				
		layer.nameChanged.connect(lambda: self.layerNameChanged(layer, newName, layer.name()))
				
		return True