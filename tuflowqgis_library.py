"""
 --------------------------------------------------------
		tuflowqgis_library - tuflowqgis operation functions
        begin                : 2013-08-27
        copyright            : (C) 2013 by Phillip Ryan
        email                : support@tuflow.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import csv
import sys
import time
import os.path
import operator

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from math import *
import numpy
import matplotlib
import glob # MJS 11/02
import tuflowqgis_styles

#sys.path.append(r'C:\Program Files\JetBrains\PyCharm 2018.1\debug-eggs')
#sys.path.append(r'C:\Program Files\JetBrains\PyCharm 2018.1\helpers\pydev')
#import pydevd

#sys.path.append(r'C:\Users\Ellis\.p2\pool\plugins\org.python.pydev.core_6.3.2.201803171248\pysrc')
#import pydevd

# --------------------------------------------------------
#    tuflowqgis Utility Functions
# --------------------------------------------------------

def tuflowqgis_find_layer(layer_name):

	for name, search_layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
		if search_layer.name() == layer_name:
			return search_layer

	return None

def tuflowqgis_find_plot_layers():

	plotLayers = []

	for name, search_layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
		if '_PLOT_P' in search_layer.name() or 'PLOT_L' in search_layer.name():
			plotLayers.append(search_layer)
		if len(plotLayers) == 2:
			return plotLayers

	if len(plotLayers) == 1:
		return plotLayers
	else:
		return None
	
def tuflowqgis_duplicate_file(qgis, layer, savename, keepform):
	if (layer == None) and (layer.type() != QgsMapLayer.VectorLayer):
		return "Invalid Vector Layer " + layer.name()
		
	# Create output file
	if len(savename) <= 0:
		return "Invalid output filename given"
	
	if QFile(savename).exists():
		if not QgsVectorFileWriter.deleteShapeFile(savename):
			return "Failure deleting existing shapefile: " + savename
	
	outfile = QgsVectorFileWriter(savename, "System", 
		layer.dataProvider().fields(), layer.wkbType(), layer.dataProvider().crs())
	
	if (outfile.hasError() != QgsVectorFileWriter.NoError):
		return "Failure creating output shapefile: " + unicode(outfile.errorMessage())	
		
	# Iterate through each feature in the source layer
	feature_count = layer.dataProvider().featureCount()

	#feature = QgsFeature()
	#layer.dataProvider().select(layer.dataProvider().attributeIndexes())
	#layer.dataProvider().rewind()
	for f in layer.getFeatures():
	#while layer.dataProvider().nextFeature(feature):
		outfile.addFeature(f)
		
	del outfile
	
	# create qml from input layer
	if keepform:
		qml = savename.replace('.shp','.qml')
		if QFile(qml).exists():
			return "QML File for output already exists."
		else:
			QMessageBox.information(qgis.mainWindow(),"Info", "Creating QML")
			layer.saveNamedStyle(qml)
			QMessageBox.information(qgis.mainWindow(),"Info", "Done")
	
	return None

def tuflowqgis_create_tf_dir(qgis, crs, basepath):
	if (crs == None):
		return "No CRS specified"

	if (basepath == None):
		return "Invalid location specified"
	
	# Create folders, ignore top level (e.g. model, as these are create when the subfolders are created)
	TUFLOW_Folders = ["\\bc_dbase","\\check", "\\model\gis\\empty", "\\results", "\\runs\\log"]
	for x in TUFLOW_Folders:
		tmppath = os.path.join(basepath+"\\TUFLOW"+x)
		if os.path.isdir(tmppath):
			print "Directory Exists"
		else:
			print "Creating Directory"
			os.makedirs(tmppath)

			
	# Write Projection.prj Create a file ('w' for write, creates if doesnt exit)
	prjname = os.path.join(basepath+"\\TUFLOW\\model\\gis\Projection.shp")
	if len(prjname) <= 0:
		return "Error creating projection filename"

	if QFile(prjname).exists():
		return "Projection file already exists: "+prjname

	fields = QgsFields()
	fields.append( QgsField( "notes", QVariant.String ) )
	outfile = QgsVectorFileWriter(prjname, "System", fields, QGis.WKBPoint, crs, "ESRI Shapefile")
	
	if (outfile.hasError() != QgsVectorFileWriter.NoError):
		return "Failure creating output shapefile: " + unicode(outfile.errorMessage())	

	del outfile

	# Write .tcf file
	tcf = os.path.join(basepath+"\\TUFLOW\\runs\\Create_Empties.tcf")
	f = file(tcf, 'w')
	f.write("GIS FORMAT == SHP\n")
	f.write("SHP Projection == ..\model\gis\projection.prj\n")
	f.write("Write Empty GIS Files == ..\model\gis\empty\n")
	f.flush()
	f.close()
	QMessageBox.information(qgis.mainWindow(),"Information", "TUFLOW folder successfully created: "+basepath)
	return None

def tuflowqgis_import_empty_tf(qgis, basepath, runID, empty_types, points, lines, regions):
	if (len(empty_types) == 0):
		return "No Empty File T specified"

	if (basepath == None):
		return "Invalid location specified"
	
	if ((not points) and (not lines) and (not regions)):
		return "No Geometry types selected"
	
	geom_type = []
	if (points):
		geom_type.append('_P')
	if (lines):
		geom_type.append('_L')
	if (regions):
		geom_type.append('_R')
	
	gis_folder = basepath.replace('\empty','')
	# Create folders, ignore top level (e.g. model, as these are create when the subfolders are created)
	for type in empty_types:
		for geom in geom_type:
			fpath = os.path.join(basepath+"\\"+type+"_empty"+geom+".shp")
			#QMessageBox.information(qgis.mainWindow(),"Creating TUFLOW directory", fpath)
			if (os.path.isfile(fpath)):
				layer = QgsVectorLayer(fpath, "tmp", "ogr")
				name = str(type)+'_'+str(runID)+str(geom)+'.shp'
				savename = os.path.join(gis_folder+"\\"+name)
				if QFile(savename).exists():
					QMessageBox.critical(qgis.mainWindow(),"Info", ("File Exists: "+savename))
				#outfile = QgsVectorFileWriter(QString(savename), QString("System"), 
				outfile = QgsVectorFileWriter(savename, "System", 
					layer.dataProvider().fields(), layer.dataProvider().geometryType(), layer.dataProvider().crs())
				if (outfile.hasError() != QgsVectorFileWriter.NoError):
					QMessageBox.critical(qgis.mainWindow(),"Info", ("Error Creating: "+savename))
				del outfile
				qgis.addVectorLayer(savename, name[:-4], "ogr")

	return None
	
def tuflowqgis_get_selected_IDs(qgis,layer):
	QMessageBox.information(qgis.mainWindow(),"Info", "Entering tuflowqgis_get_selected_IDs")
	IDs = []
	if (layer == None) and (layer.type() != QgsMapLayer.VectorLayer):
		return None, "Invalid Vector Layer " + layer.name()

	dataprovider = layer.dataProvider()
	idx = layer.fieldNameIndex('ID')
	QMessageBox.information(qgis.mainWindow(),"IDX", str(idx))
	if (idx == -1):
		QMessageBox.critical(qgis.mainWindow(),"Info", "ID field not found in current layer")
		return None, "ID field not found in current layer"
	
	for feature in layer.selectedFeatures():
		id = feature.attributeMap()[idx].toString()
		IDs.append(id)
	return IDs, None

def check_python_lib(qgis):
	error = False
	py_modules = []
	try:
		py_modules.append('numpy')
		import numpy
	except:
		error = True
		QMessageBox.critical(qgis.mainWindow(),"Error", "python library 'numpy' not installed.")
	try:
		py_modules.append('csv')
		import csv
	except:
		error = True
		QMessageBox.critical(qgis.mainWindow(),"Error", "python library 'csv' not installed.")
	try:
		py_modules.append('matplotlib')
		import matplotlib
	except:
		error = True
		QMessageBox.critical(qgis.mainWindow(),"Error", "python library 'matplotlib' not installed.")
	try:
		py_modules.append('PyQt4')
		import PyQt4
	except:
		error = True
		QMessageBox.critical(qgis.mainWindow(),"Error", "python library 'PyQt4' not installed.")
	try:
		py_modules.append('osgeo.ogr')
		import osgeo.ogr as ogr
	except:
		error = True
		QMessageBox.critical(qgis.mainWindow(),"Error", "python library 'osgeo.ogr' not installed.")
	try:
		py_modules.append('glob')
		import glob
	except:
		error = True
		QMessageBox.critical(qgis.mainWindow(),"Error", "python library 'glob' not installed.")
	try:
		py_modules.append('os')
		import os
	except:
		error = True
		QMessageBox.critical(qgis.mainWindow(),"Error", "python library 'os' not installed.")
	msg = 'Modules tested: \n'
	for mod in py_modules:
		msg = msg+mod+'\n'
	QMessageBox.information(qgis.mainWindow(),"Information", msg)
	
	if error:
		return True
	else:
		return None
		
def run_tuflow(qgis,tfexe,tcf):
	
	#QMessageBox.Information(qgis.mainWindow(),"debug", "Running TUFLOW - tcf: "+tcf)
	try:
		from subprocess import Popen
		tfarg = [tfexe, '-b',tcf]
		tf_proc = Popen(tfarg)
	except:
		return "Error occurred starting TUFLOW"
	#QMessageBox.Information(qgis.mainWindow(),"debug", "TUFLOW started")
	return None

def config_set(project,tuflow_folder,tfexe,projection):
	message = None
	try:
		f = file(config_file, 'w')
		f.write('TUFLOW Folder =='+tuflow_folder+'\n')
		f.write('TUFLOW Exe =='+tfexe+'\n')
		f.write('PROJECTION =='+proj+'\n')
		f.flush()
		f.close()
	except:
		message = "Unable to write TUFLOW config file: "+config_file

	return message
	
def extract_all_points(qgis,layer,col):
	
	#QMessageBox.Information(qgis.mainWindow(),"debug", "starting to extract points")
	try:
		iter = layer.getFeatures()
		npt = 0
		x = []
		y = []
		z = []
		for feature in iter:
			npt = npt + 1
			geom = feat.geometry()
			#QMessageBox.Information(qgis.mainWindow(),"debug", "x = "+str(geom.x())+", y = "+str(geom.y()))
			x.append(geom.x())
			y.append(geom.y())
			zt = feature.attributeMap()[col]
			#QMessageBox.Information(qgis.mainWindow(),"debug", "z = "+str(zt))
			z.append(zt)
		return x, y, z, message
	except:
		return None, None, None, "Error extracting point data"

def get_file_ext(fname):
	try:
		ind = fname.find('|')
		if (ind>0):
			fname = fname[0:ind]
	except:
		return None, None, "Error trimming filename"
	try:
		ind = fname.rfind('.')
		if (ind>0):
			fext = fname[ind+1:]
			fext = fext.upper()
			fname_noext = fname[0:ind]
			return fext, fname_noext, None
		else:
			return None, None, "Could not find . in filename"
	except:
		return None, None, "Error trimming filename"

def load_project(project):
	message = None
	try:
		tffolder = project.readEntry("configure_tuflow", "folder", "Not yet set")[0]
	except:
		message = "Error - Reading from project file."
		QMessageBox.information(qgis.mainWindow(),"Information", message)

	try:
		tfexe = project.readEntry("configure_tuflow", "exe", "Not yet set")[0]
	except:
		message = "Error - Reading from project file."
		QMessageBox.information(qgis.mainWindow(),"Information", message)

	try:
		tf_prj = project.readEntry("configure_tuflow", "projection", "Undefined")[0]
	except:
		message = "Error - Reading from project file."
		QMessageBox.information(qgis.mainWindow(),"Information", message)
	
	error = False
	if (tffolder == "Not yet set"):
		error = True
		QMessageBox.information(qgis.mainWindow(),"Information", "Not set tffolder")
	if (tfexe == "Not yet set"):
		error = True
		QMessageBox.information(qgis.mainWindow(),"Information", "Not set tfexe")
	if (tf_prj == "Undefined"):
		error = True
		QMessageBox.information(qgis.mainWindow(),"Information", "tf_prj")
	if error:
		message = "Project does not appear to be configured.\nPlease run TUFLOW >> Editing >> Configure Project from the plugin menu."
	
	return message, tffolder, tfexe, tf_prj
 
#  tuflowqgis_import_check_tf added MJS 11/02
def tuflowqgis_import_check_tf(qgis, basepath, runID,showchecks):
	#import check file styles using class
	tf_styles = tuflowqgis_styles.TF_Styles()
	error, message = tf_styles.Load()
	if error:
		QMessageBox.critical(qgis.mainWindow(),"Error", message)
		return message

	if (basepath == None):
		return "Invalid location specified"

	# Get all the check files in the given directory
	check_files = glob.glob(basepath +  '\*'+ runID +'*.shp')

	if len(check_files) > 100:
		QMessageBox.critical(qgis.mainWindow(),"Info", ("You have selected over 100 check files. You can use the RunID to reduce this selection."))
		return "Too many check files selected"

	if not check_files:
		check_files = glob.glob(basepath +  '\*'+ runID +'*.mif')
		if len(check_files) > 0: 
			return ".MIF Files are not supported, only .SHP files."
		else:
			return "No check files found for this RunID in this location."

	# Get the legend interface
	legint = qgis.legendInterface()

	# Add each layer to QGIS and style
	for chk in check_files:
		pfft,fname = os.path.split(chk)
		#QMessageBox.information(qgis.mainWindow(),"Debug", fname)
		fname = fname[:-4]
		layer = qgis.addVectorLayer(chk, fname, "ogr")
		renderer = region_renderer(layer)
		if renderer: #if the file requires a attribute based rendered (e.g. BC_Name for a _sac_check_R)
			layer.setRendererV2(renderer)
			layer.triggerRepaint()
		else: # use .qml style using tf_styles
			error, message, slyr = tf_styles.Find(fname) #use tuflow styles to find longest matching 
			if error:
				QMessageBox.critical(qgis.mainWindow(),"ERROR", message)
				return message
			if slyr: #style layer found:
				layer.loadNamedStyle(slyr)
				if os.path.split(slyr)[1][:-4] == '_zpt_check':
					legint.setLayerVisible(layer, False)   # Switch off by default
				elif '_uvpt_check' in fname or '_grd_check' in fname:
					legint.setLayerVisible(layer, False)
				if not showchecks:
					legint.setLayerVisible(layer, False)

	message = None #normal return
	return message


#  region_renderer added MJS 11/02
def region_renderer(layer):
	from random import randrange
	registry = QgsSymbolLayerV2Registry.instance()
	symbol_layer2 = None

	#check if layer needs a renderer
	fsource = layer.source() #includes full filepath and extension
	fname = os.path.split(fsource)[1][:-4] #without extension
	
	if '_bcc_check_R' in fname:
		field_name = 'Source'
	elif '_1d_to_2d_check_R' in fname:
		field_name = 'Primary_No'
	elif '_2d_to_2d_R' in fname:
		field_name = 'Primary_No'
	elif '_sac_check_R' in fname:
		field_name = 'BC_Name'
	elif '2d_bc' in fname or '2d_mat' in fname or '2d_soil' in fname or '1d_bc' in fname:
		field_name = layer.fields().field(0).name()
	elif '1d_nwk' in fname or '1d_nwkb' in fname or '1d_nwke' in fname or '1d_mh' in fname or '1d_pit' in fname or \
		 '1d_nd' in fname:
		field_name = layer.fields().field(1).name()
	else: #render not needed
		return None
		
	# Thankyou Detlev  @ http://gis.stackexchange.com/questions/175068/apply-symbol-to-each-feature-categorized-symbol

	
	# get unique values
	vals = layer.fieldNameIndex(field_name)
	unique_values = layer.dataProvider().uniqueValues(vals)
	#QgsMessageLog.logMessage('These values have been identified: ' + vals, "TUFLOW")

	# define categories
	categories = []
	for unique_value in unique_values:
		# initialize the default symbol for this geometry type
		symbol = QgsSymbolV2.defaultSymbol(layer.geometryType())

		# configure a symbol layer
		layer_style = {}
		color = '%d, %d, %d' % (randrange(0,256), randrange(0,256), randrange(0,256))
		layer_style['color'] = color
		layer_style['outline'] = '#000000'
		if '2d_bc' in fname:
			if layer.geometryType() == 1:
				#QMessageBox.information(qgis.mainWindow(), "DEBUG", 'line 446')
				symbol_layer = QgsSimpleLineSymbolLayerV2.create(layer_style)
				symbol_layer.setWidth(1)
			elif layer.geometryType() == 0:
				symbol_layer = QgsSimpleMarkerSymbolLayerV2.create(layer_style)
				symbol_layer.setSize(1.5)
				symbol_layer.setName('circle')
			else:
				symbol_layer = QgsSimpleFillSymbolLayerV2.create(layer_style)
		elif '1d_nwk' in fname or '1d_nwkb' in fname or '1d_nwke' in fname or '1d_pit' in fname or '1d_nd' in fname:
			if layer.geometryType() == 1:
				#QMessageBox.information(qgis.mainWindow(), "DEBUG", 'line 446')
				symbol_layer = QgsSimpleLineSymbolLayerV2.create(layer_style)
				symbol_layer.setWidth(1)
				symbol_layer2 = QgsMarkerLineSymbolLayerV2.create({'placement': 'lastvertex'})
				markerMeta = registry.symbolLayerMetadata("MarkerLine")
				markerLayer = markerMeta.createSymbolLayer({'width': '0.26', 'color': color, 'rotate': '1', 'placement': 'lastvertex'})
				subSymbol = markerLayer.subSymbol()
				subSymbol.deleteSymbolLayer(0)
				triangle = registry.symbolLayerMetadata("SimpleMarker").createSymbolLayer({'name': 'filled_arrowhead', 'color': color, 'color_border': color, 'offset': '0,0', 'size': '4', 'angle': '0'})
				subSymbol.appendSymbolLayer(triangle)
			elif layer.geometryType() == 0:
				symbol_layer = QgsSimpleMarkerSymbolLayerV2.create(layer_style)
				symbol_layer.setSize(1.5)
				if unique_value == 'NODE':
					symbol_layer.setName('circle')
				else:
					symbol_layer.setName('square')
		elif '2d_mat' in fname:
			symbol_layer = QgsSimpleFillSymbolLayerV2.create(layer_style)
			layer.setLayerTransparency(75)
		elif '2d_soil' in fname:
			symbol_layer = QgsSimpleFillSymbolLayerV2.create(layer_style)
			layer.setLayerTransparency(75)
		elif '1d_bc' in fname:
			if layer.geometryType() == 0:
				symbol_layer = QgsSimpleMarkerSymbolLayerV2.create(layer_style)
				symbol_layer.setSize(1.5)
				symbol_layer.setName('circle')
			else:
				layer_syle['style'] = 'no'
				symbol_layer = QgsSimpleFillSymbolLayerV2.create(layer_style)
				color = QColor(randrange(0,256), randrange(0,256), randrange(0,256))
				symbol_layer.setBorderColor(color)
				symbol_layer.setBorderWidth(1)
		else:
			symbol_layer = QgsSimpleFillSymbolLayerV2.create(layer_style)

		# replace default symbol layer with the configured one
		if symbol_layer is not None:
			symbol.changeSymbolLayer(0, symbol_layer)
			if symbol_layer2 is not None:
				symbol.appendSymbolLayer(markerLayer)
		# create renderer object
		category = QgsRendererCategoryV2(unique_value, symbol, str(unique_value))
		# entry for the list of category items
		categories.append(category)

	# create renderer object
	return QgsCategorizedSymbolRendererV2(field_name, categories)
	
def tuflowqgis_apply_check_tf(qgis):
	#apply check file styles to all open shapefiles
	error = False
	message = None

	#load style layers using tuflowqgis_styles
	tf_styles = tuflowqgis_styles.TF_Styles()
	error, message = tf_styles.Load()
	if error:
		return error, message
		
	for layer_name, layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
		if layer.type() == QgsMapLayer.VectorLayer:
			layer_fname = os.path.split(layer.source())[1][:-4]
			#QMessageBox.information(qgis.mainWindow(), "DEBUG", "shp layer name = "+layer.name())
			renderer = region_renderer(layer)
			if renderer: #if the file requires a attribute based rendered (e.g. BC_Name for a _sac_check_R)
				layer.setRendererV2(renderer)
				layer.triggerRepaint()
			else: # use .qml style using tf_styles
				error, message, slyr = tf_styles.Find(layer_fname, layer) #use tuflow styles to find longest matching 
				if error:
					return error, message
				if slyr: #style layer found:
					layer.loadNamedStyle(slyr)
					layer.triggerRepaint()
	return error, message
	

def tuflowqgis_apply_check_tf_clayer(qgis):
	error = False
	message = None
	try:
		canvas = qgis.mapCanvas()
	except:
		error = True
		message = "ERROR - Unexpected error trying to  QGIS canvas layer."
		return error, message
	try:
		cLayer = canvas.currentLayer()
	except:
		error = True
		message = "ERROR - Unable to get current layer, ensure a selection is made"
		return error, message
	
	#load style layers using tuflowqgis_styles
	tf_styles = tuflowqgis_styles.TF_Styles()
	error, message = tf_styles.Load()
	if error:
		return error, message
		

	if cLayer.type() == QgsMapLayer.VectorLayer:
		layer_fname = os.path.split(cLayer.source())[1][:-4]
		renderer = region_renderer(cLayer)
		if renderer: #if the file requires a attribute based rendered (e.g. BC_Name for a _sac_check_R)
			cLayer.setRendererV2(renderer)
			cLayer.triggerRepaint()
		else: # use .qml style using tf_styles
			error, message, slyr = tf_styles.Find(layer_fname, cLayer) #use tuflow styles to find longest matching 
			if error:
				return error, message
			if slyr: #style layer found:
				cLayer.loadNamedStyle(slyr)
				cLayer.triggerRepaint()
	else:
		error = True
		message = 'ERROR - Layer is not a vector layer: '+cLayer.source()
		return error, message
	return error, message
	
def tuflowqgis_increment_fname(infname):
	#check for file extension (shapefile only, not expecting .mif)
	fext = ''
	if infname[-4:].upper() == '.SHP':
		fext = infname[-4:]
		fname = infname[0:-4]
	else:
		fname = infname

	# check for TUFLOW geometry suffix
	geom = ''
	if fname[-2:].upper() == '_P':
		tmpstr = fname[0:-2]
		geom = fname[-2:]
	elif fname[-2:].upper() == '_L':
		tmpstr = fname[0:-2]
		geom = fname[-2:]
	elif fname[-2:].upper() == '_R':
		tmpstr = fname[0:-2]
		geom = fname[-2:]
	else:
		tmpstr = fname

	#try to find version as integer at end of string
	rind = tmpstr.rfind('_')
	if rind >= 0:
		verstr = tmpstr[rind+1:]
		ndig = len(verstr)
		lstr = tmpstr[0:rind+1]
		try:
			verint = int(verstr)
			verint = verint + 1
			newver = str(verint)
			newverstr = newver.zfill(ndig)
			outfname =lstr+newverstr+geom+fext
		except:
			outfname = tmpstr
	else:
		outfname = tmpstr

	return outfname
	
def tuflowqgis_insert_tf_attributes(qgis, inputLayer, basedir, runID, template, lenFields):
	message = None
	
	if inputLayer.dataProvider().geometryType() == QGis.WKBPoint:
		geomType = '_P'
	elif inputLayer.dataProvider().geometryType() == QGis.WKBPolygon:
		geomType = '_R'
	else:
		geomType = '_L'
		
	
	gis_folder = basedir.replace('\empty', '')
	
	# Create new vector file from template with appended attribute fields
	if template == '1d_nwk':
		if lenFields >= 10:
			template2 = '1d_nwke'
			fpath = os.path.join(basedir, '{0}_empty{1}.shp'.format(template2, geomType))
		else:
			fpath = os.path.join(basedir, '{0}_empty{1}.shp'.format(template, geomType))
	else:
		fpath = os.path.join(basedir, '{0}_empty{1}.shp'.format(template, geomType))
	if os.path.isfile(fpath):
		layer = QgsVectorLayer(fpath, "tmp", "ogr")
		name = '{0}_{1}{2}.shp'.format(template, runID, geomType)
		savename = os.path.join(gis_folder, name)
		if QFile(savename).exists():
			QMessageBox.critical(qgis.mainWindow(),"Info", ("File Exists: {0}".format(savename)))
			message = 'Unable to complete utility because file already exists'
			return message
		outfile = QgsVectorFileWriter(savename, "System", 
			layer.dataProvider().fields(), layer.dataProvider().geometryType(), layer.dataProvider().crs())
		if outfile.hasError() != QgsVectorFileWriter.NoError:
			QMessageBox.critical(qgis.mainWindow(),"Info", ("Error Creating: {0}".format(savename)))
			message = 'Error writing output file. Check output location and output file.'
			return message
		outfile = QgsVectorLayer(savename, "tmp", "ogr")
		outfile.dataProvider().addAttributes(inputLayer.dataProvider().fields())
		
		# Get attribute names of input layers
		layer_attributes = [field.name() for field in layer.fields()]
		inputLayer_attributes = [field.name() for field in inputLayer.fields()]
		
		# Create 2D attribute value list and add features to new file
		row_list = []
		for feature in inputLayer.getFeatures():
			row = [''] * len(layer_attributes)
			for name in inputLayer_attributes:
				row.append(feature[name])
			row_list.append(row)
			outfile.dataProvider().addFeatures([feature])
		
		# correct field values
		for i, feature in enumerate(outfile.getFeatures()):
			row_dict = {}
			for j in range(len(row_list[0])):
				row_dict[j] = row_list[i][j]
			outfile.dataProvider().changeAttributeValues({i: row_dict})
		
		qgis.addVectorLayer(savename, name[:-4], "ogr")
	
	return message
	
def get_tuflow_labelName(layer):
	fsource = layer.source() #includes full filepath and extension
	fname = os.path.split(fsource)[1][:-4] #without extension
	
	if '1d_bc' in fname or '2d_bc' in fname:
		field_name1 = layer.fields().field(0).name()
		field_name2 = layer.fields().field(2).name()
		field_name = "'Name: ' + \"{0}\" + '\n' + 'Type: ' + \"{1}\"".format(field_name2, field_name1)
	elif '1d_mh' in fname or '1d_nd' in fname or '1d_pit' in fname:
		field_name1 = layer.fields().field(0).name()
		field_name2 = layer.fields().field(1).name()
		field_name = "'ID: ' + \"{0}\" + '\n' + 'Type: ' + \"{1}\"".format(field_name1, field_name2)
	elif '1d_nwk' in fname:
		field_name1 = layer.fields().field(0).name()
		field_name2 = layer.fields().field(1).name()
		field_name3 = layer.fields().field(13).name()
		field_name4 = layer.fields().field(14).name()
		field_name = "'ID: ' + \"{0}\" + '\n' + 'Type: ' + \"{1}\" + '\n' + 'Width: ' + " \
		             "if(\"{2}\">=0, to_string(\"{2}\"), \"{2}\") + '\n' + 'Height: ' + " \
		             "if(\"{3}\">=0, to_string(\"{3}\"), \"{3}\")".format(field_name1, field_name2, field_name3,
		                                                                  field_name4)
	elif '2d_fc_' in fname:
		field_name1 = layer.fields().field(0).name()
		field_name2 = layer.fields().field(1).name()
		field_name3 = layer.fields().field(2).name()
		field_name4 = layer.fields().field(5).name()
		field_name = "'Type: ' + \"{0}\" + '\n' + 'Invert: ' + if(\"{1}\">-1000000, to_string(\"{1}\"), \"{1}\") +" \
		             "'\n' + 'Obvert: ' + if(\"{2}\">-100, to_string(\"{2}\"), \"{2}\") + '\n' + 'FLC: ' + " \
		             "if(\"{3}\">=0, to_string(\"{3}\"), \"{3}\")".format(field_name1, field_name2, field_name3, 
		                                                                  field_name4)
	elif '2d_fcsh' in fname:
		field_name1 = layer.fields().field(0).name()
		field_name2 = layer.fields().field(1).name()
		field_name3 = layer.fields().field(5).name()
		field_name4 = layer.fields().field(6).name()
		field_name = "'Invert: ' + if(\"{0}\">-1000000, to_string(\"{0}\"), \"{0}\") + '\n' + 'Obvert: ' + " \
		             "if(\"{1}\">-100, to_string(\"{1}\"), \"{1}\") + '\n'" \
		             " + 'pBlockage: ' + if(\"{2}\">-100, to_string(\"{2}\"), \"{2}\") + '\n' + 'FLC: ' + " \
		             "if(\"{3}\">=0, to_string(\"{3}\"), \"{3}\")".format(field_name1, field_name2, field_name3, 
		                                                                  field_name4)
	elif '2d_lfcsh' in fname:
		field_name1 = layer.fields().field(0).name()
		field_name2 = layer.fields().field(4).name()
		field_name3 = layer.fields().field(5).name()
		field_name4 = layer.fields().field(6).name()
		field_name5 = layer.fields().field(7).name()
		field_name6 = layer.fields().field(8).name()
		field_name7 = layer.fields().field(9).name()
		field_name8 = layer.fields().field(10).name()
		field_name9 = layer.fields().field(11).name()
		field_name10 = layer.fields().field(12).name()
		field_name = "'Invert: ' + if(\"{0}\">-1000000, to_string(\"{0}\"), \"{0}\") + '\n' + 'L1 Obvert: ' + " \
		             "if(\"{1}\">-100, to_string(\"{1}\"), \"{1}\") + '\n'" \
		             " + 'L1 pBlockage: ' + if(\"{2}\">-100, to_string(\"{2}\"), \"{2}\") + '\n' + 'L1 FLC: ' + " \
		             "if(\"{3}\">=0, to_string(\"{3}\"), \"{3}\") + '\n' + 'L2 Depth: ' + " \
		             "if(\"{4}\">=0, to_string(\"{4}\"), \"{4}\") + '\n' + 'L2 pBlockage: ' + " \
		             "if(\"{5}\">=0, to_string(\"{5}\"), \"{5}\") + '\n' + 'L2 FLC: ' + " \
		             "if(\"{6}\">=0, to_string(\"{6}\"), \"{6}\") + '\n' + 'L3 Depth: ' + " \
		             "if(\"{7}\">=0, to_string(\"{7}\"), \"{7}\") + '\n' + 'L3 pBlockage: ' + " \
		             "if(\"{8}\">=0, to_string(\"{8}\"), \"{8}\") + '\n' + 'L3 FLC: ' + " \
		             "if(\"{9}\">=0, to_string(\"{9}\"), \"{9}\")".format(field_name1, field_name2, field_name3, 
		                                                                  field_name4, field_name5, field_name6, 
		                                                                  field_name7, field_name8, field_name9,
		                                                                  field_name10)
	elif '2d_po' in fname or '2d_lp' in fname:
		field_name1 = layer.fields().field(0).name()
		field_name2 = layer.fields().field(1).name()
		field_name = "'Type: ' + \"{0}\" + '\n' + 'Label: ' + \"{1}\"".format(field_name1, field_name2)
	elif '2d_sa_rf' in fname:
		field_name1 = layer.fields().field(0).name()
		field_name2 = layer.fields().field(1).name()
		field_name3 = layer.fields().field(2).name()
		field_name4 = layer.fields().field(3).name()
		field_name5 = layer.fields().field(4).name()
		field_name = "'Name: ' + \"{0}\" + '\n' + 'Catchment Area: ' + if(\"{1}\">0, to_string(\"{1}\"), \"{1}\") + " \
		             "'\n' + 'Rain Gauge: ' + \"{2}\" + '\n' + 'IL: ' + if(\"{3}\">=0, to_string(\"{3}\"), \"{3}\") " \
		             " + '\n' + 'CL: ' + if(\"{4}\">=0, to_string(\"{4}\"), \"{4}\")".format(field_name1, field_name2, 
		                                                                                     field_name3, field_name4,
		                                                                                     field_name5)
	elif '2d_sa_tr' in fname:
		field_name1 = layer.fields().field(0).name()
		field_name2 = layer.fields().field(1).name()
		field_name3 = layer.fields().field(2).name()
		field_name4 = layer.fields().field(3).name()
		field_name = "'Name: ' + \"{0}\" + '\n' + 'Trigger Type: ' + \"{1}\" + '\n' + 'Trigger Location: ' + \"{2}\"" \
		             "+ '\n' + 'Trigger Value: ' + if(\"{3}\">=0, to_string(\"{3}\"), \"{3}\")".format(field_name1, 
		                                                                                               field_name2, 
		                                                                                               field_name3,
		                                                                                               field_name4)
	elif '2d_vzsh' in fname:
		field_name1 = layer.fields().field(0).name()
		field_name2 = layer.fields().field(3).name()
		field_name3 = layer.fields().field(4).name()
		field_name4 = layer.fields().field(5).name()
		field_name5 = layer.fields().field(6).name()
		field_name6 = layer.fields().field(7).name()
		field_name = "'Z: ' + if(\"{0}\">-1000000, to_string(\"{0}\"), \"{0}\") + '\n' + 'Shape Options: ' + \"{1}\"" \
		             "+ '\n' + 'Trigger 1: ' + \"{2}\" + '\n' + 'Trigger 2: ' + \"{3}\" + '\n' + 'Trigger Value: ' "\
		             "+ if(\"{4}\">0, to_string(\"{4}\"), \"{4}\") + '\n' + 'Period: ' + " \
		             "if(\"{5}\">0, to_string(\"{5}\"), \"{5}\")".format(field_name1, field_name2, field_name3,
		                                                                 field_name4, field_name5, field_name6)
	elif '2d_zshr' in fname:
		field_name1 = layer.fields().field(0).name()
		field_name2 = layer.fields().field(3).name()
		field_name3 = layer.fields().field(4).name()
		field_name4 = layer.fields().field(5).name()
		field_name5 = layer.fields().field(6).name()
		field_name = "'Z: ' + if(\"{0}\">-1000000, to_string(\"{0}\"), \"{0}\") + '\n' + 'Shape Options: ' + \"{1}\"" \
		             "+ '\n' + 'Route Name: ' + \"{2}\" + '\n' + 'Cut Off Type: ' + \"{3}\" + '\n' + " \
		             "'Cut Off Values: ' + if(\"{4}\">-1000000, to_string(\"{4}\"), \"{4}\")".format(field_name1, 
		                                                                                             field_name2, 
		                                                                                             field_name3,
		                                                                                             field_name4, 
		                                                                                             field_name5)
	elif '2d_zsh' in fname:
		if layer.geometryType() == 0:
			field_name1 = layer.fields().field(0).name()
			field_name = "'{0}: ' + if(\"{0}\">-1000000, to_string(\"{0}\"), \"{0}\")".format(field_name1)
		elif layer.geometryType() == 1:
			field_name1 = layer.fields().field(0).name()
			field_name2 = layer.fields().field(2).name()
			field_name = "'Z: ' + if(\"{0}\">-1000000, to_string(\"{0}\"), \"{0}\") + '\n' + 'Shape Width: ' + " \
			             "if(\"{1}\">-1000000, to_string(\"{1}\"), \"{1}\")".format(field_name1, field_name2)
		elif layer.geometryType() == 2:
			field_name1 = layer.fields().field(0).name()
			field_name2 = layer.fields().field(3).name()
			field_name = "'Z: ' + if(\"{0}\">-1000000, to_string(\"{0}\"), \"{0}\") + '\n' + 'Shape Options: ' + " \
			             "\"{1}\"".format(field_name1, field_name2)
	elif '_RCP' in fname:
		field_name1 = layer.fields().field(0).name()
		field_name2 = layer.fields().field(1).name()
		field_name3 = layer.fields().field(2).name()
		field_name4 = layer.fields().field(3).name()
		field_name5 = layer.fields().field(4).name()
		field_name = "'Route Name: ' + if(\"{0}\">-1000000, to_string(\"{0}\"), \"{0}\") + '\n' + 'Cut Off Value: ' " \
		             "+ if(\"{1}\">-1000000, to_string(\"{1}\"), \"{1}\") + '\n' + 'First Cut Off Time: ' + " \
		             "if(\"{2}\">-1000000, to_string(\"{2}\"), \"{2}\") + '\n' + 'Last Cutoff Time: ' + " \
		             "if(\"{3}\">-1000000, to_string(\"{3}\"), \"{3}\") + '\n' + 'Duration of Cutoff: ' + " \
		             "if(\"{4}\">-1000000, to_string(\"{4}\"), \"{4}\")".format(field_name1, field_name2, field_name3, 
		                                                                        field_name4, field_name5)
	elif '1d_mmH_P' in fname:
		field_name = ""
		for i, field in enumerate(layer.fields()):
			if i == 0 or i == 1 or i == 3:
				field_name1 = "'{0}: ' + if(\"{0}\">-1000000, to_string(\"{0}\"), \"{0}\")".format(field.name())
				if i != 3:
					field_name = field_name + field_name1 + "+ '\n' +"
				else:
					field_name = field_name + field_name1
	elif '1d_mmQ_P' in fname or '1d_mmV_P' in fname:
		field_name = ""
		for i, field in enumerate(layer.fields()):
			if i == 0 or i == 1 or i == 2 or i == 4 or i == 5:
				field_name1 = "'{0}: ' + if(\"{0}\">-1000000, to_string(\"{0}\"), \"{0}\")".format(field.name())
				if i != 5:
					field_name = field_name + field_name1 + "+ '\n' +"
				else:
					field_name = field_name + field_name1
	elif '1d_ccA_L' in fname:
		field_name = ""
		for i, field in enumerate(layer.fields()):
			if i == 0 or i == 1:
				field_name1 = "'{0}: ' + if(\"{0}\">-1000000, to_string(\"{0}\"), \"{0}\")".format(field.name())
				if i != 1:
					field_name = field_name + field_name1 + "+ '\n' +"
				else:
					field_name = field_name + field_name1
	else:
		field_name1 = layer.fields().field(0).name()
		field_name = "'{0}: ' + if(\"{0}\">-1000000, to_string(\"{0}\"), \"{0}\")".format(field_name1)
	return field_name
	
def tuflowqgis_apply_autoLabel_clayer(qgis):
	#QMessageBox.information(qgis.mainWindow(),"Info", ("{0}".format(enabled)))
	
	error = False
	message = None
	canvas = qgis.mapCanvas()
	#canvas.mapRenderer().setLabelingEngine(QgsPalLabeling())
	
	cLayer = canvas.currentLayer()
	
	labelName = get_tuflow_labelName(cLayer)
	label = QgsPalLayerSettings()
	label.readFromLayer(cLayer)
	if label.enabled == False:
		label.enabled = True
		label.fieldName = labelName
		label.isExpression = True
		if cLayer.geometryType() == 0:
			label.placement = 0
		elif cLayer.geometryType() == 1:
			label.placement = 2
		elif cLayer.geometryType() == 2:
			label.placement = 1
		label.multilineAlign = 0
		label.bufferDraw = True
		label.writeToLayer(cLayer)
		label.drawLabels = True
	else:
		label.enabled = False
		label.fieldIndex = 2
		label.writeToLayer(cLayer)
		label.drawLabels = False
	canvas.refresh()

	return error, message


def find_waterLevelPoint(selection, plotLayer):
	"""Finds snapped PLOT_P layer to selected XS layer

	QgsFeatureLayer selection: current selection in map window
	QgsVectorLayer plotLayer: PLOT_P layer
	"""

	message = ''
	error = False
	intersectedPoints = []
	intersectedLines = []
	plotP = None
	plotL = None

	if plotLayer is None:
		error = True
		message = 'Could not find result gis layers.'
		return intersectedPoints, intersectedLines, message, error

	for plot in plotLayer:
		if '_PLOT_P' in plot.name():
			plotP = plot
		elif '_PLOT_L' in plot.name():
			plotL = plot
	if plotP is None and plotL is None:
		error = True
		message = 'Could not find result gis layers.'
		return intersectedPoints, intersectedLines, message, error

	for xSection in selection:
		if plotP is not None:
			found_intersect = False
			for point in plotP.getFeatures():
				if point.geometry().intersects(xSection.geometry()):
					intersectedPoints.append(point['ID'].strip())
					found_intersect = True
			if found_intersect:
				intersectedLines.append(None)
				continue
			else:
				intersectedPoints.append(None)
				if plotL is not None:
					for line in plotL.getFeatures():
						if line.geometry().intersects(xSection.geometry()):
							intersectedLines.append(line['ID'].strip())
							found_intersect = True
				if not found_intersect:
					intersectedLines.append(None)
		else:
			intersectedPoints.append(None)
			if plotL is not None:
				found_intersect = False
				for line in plotL.getFeatures():
					if line.geometry().intersects(xSection.geometry()):
						intersectedLines.append(line['ID'].strip())
						found_intersect = True
			if not found_intersect:
				intersectedLines.append(None)

	return intersectedPoints, intersectedLines, message, error


def getAngle(line1, line2):
	"""
	Gets the angle between 2 lines
	
	:param line1: list of 2 vertices [start vertex, end vertex]
	:param line2: list of 2 vertices [start vertex, end vertex]
	:return: float angle
	"""
	from math import acos, pi

	a = ((line1[1][1] - line1[0][1]) ** 2 + (line1[1][0] - line1[0][0]) ** 2) ** 0.5  # triangle side a
	b = ((line2[1][1] - line2[0][1]) ** 2 + (line2[1][0] - line2[0][0]) ** 2) ** 0.5  # triangle side b
	c = ((line2[1][1] - line1[0][1]) ** 2 + (line2[1][0] - line1[0][0]) ** 2) ** 0.5  # triangle side c
	
	cosC = float(str((a ** 2 + b ** 2 - c ** 2) / (2 * a * b)))  # cosine rule - annoyingly wasn't working without convert to string then convert back to float!
	angle = acos(cosC) * 180 / pi  # convert to degrees
	
	return angle


def getVertices(lyrs):
	"""
	Creates a dictionary from all layers. For line layers it will get both start and end, for points
	it will get centroid.

	:param lyrs: list of QgisVectorLayers
	:return: compiled dictionary of all QgsVectorLayers in format of {name: [[vertices], feature id, origin lyr, [us invert, ds invert]}
	"""
	
	nullCounter = 1
	vectorDict = {}
	for line in lyrs:
		for feature in line.dataProvider().getFeatures():
			fid = feature.id()
			if line.geometryType() == 0:
				geom = feature.geometry().asPoint()
				if feature.attributes()[0] == NULL:
					name = '{0} {1}'.format(feature.attributes()[1], nullCounter)
					nullCounter += 1
					vectorDict[name] = [[geom], fid, line, [feature.attributes()[6], feature.attributes()[7]]]
				else:
					vectorDict[feature.attributes()[0]] = [[geom], fid, line, [feature.attributes()[6], 
					                                      feature.attributes()[7]]]
			elif line.geometryType() == 1:
				geom = feature.geometry().asPolyline()
				if feature.attributes()[0] == NULL:
					name = '__connector {0}'.format(nullCounter)
					nullCounter += 1
					vectorDict[name] = [[geom[0], geom[-1]], fid, line, [feature.attributes()[6], 
					                   feature.attributes()[7]]]
				else:
					vectorDict[feature.attributes()[0]] = [[geom[0], geom[-1]], fid, line, [feature.attributes()[6], 
					                                      feature.attributes()[7]]]
	
	return vectorDict


def checkSnapping(**kwargs):
	"""
	Takes vertices and checks if there are any matching and returns a list if there are no matching.
	For points, it will check points against lines.
	For lines, it will check against other lines in the same layer

	:param **kwargs: dictionary with line or point vertices {name: [vertices, origin fid, origin lyr, [us invert, ds invert]]}
	:return: list of unsnapped objects (for lines will append '==0' or first vertex, '==1' for last vertex)
	:return: list of unsnapped object names for lines without reference to first or last vertex (not returned for points)
	:return: dict of closest line vertex for unsnapped points and lines {name: [origin lyr, origin fid, closest vertex name, closest vertex coords, closest vertex dist]}
	:return: dict of downstream channels for lines if dnsConn is True {name: [[dns network channels], [us invert, ds invert]]}
	"""
	
	# determine which snapping check is being performed
	checkPoint = False
	checkLine = False
	dnsConn = False
	lineDict = kwargs['lines']  # will need lines no matter what
	lineDict_len = len(lineDict)
	if 'dns_conn' in kwargs.keys():  
		if kwargs['dns_conn']:
			dnsConn = True  # force script to loop through all pipes to get all dns connections
			checkLine = True
		if 'points' in kwargs.keys():  # if points included, check elevations in dns connections
			pointDict = kwargs['points']
			if len(pointDict) > 0:
				checkPoint = True
	if 'assessment' in kwargs.keys():
		if kwargs['assessment'] == 'lines':
			checkLine = True
		elif kwargs['assessment'] == 'points':
			if 'points' in kwargs.keys():  # assessing snapping for points
				checkPoint = True
				pointDict = kwargs['points']
	else:  # assessing for lines
		checkLine = True
	
	xIns = []  # list of X connectors that are entering a side channel - used to determine dns direction for x connectors
	dsNwk = {}  # dict listing the downstream lines
	closestV = {}  # dict closest vertex results
	unsnapped = []  # list of unsnapped vertices
	unsnapped_names = []  # list of unsnapped vertices names (for lines)
	
	# Check to see if line is snapped to another line at both ends
	if checkLine:
		for lName, lParam in lineDict.items():
			lLoc = lParam[0]
			lFid = lParam[1]
			lyr = lParam[2]
			lUsInv = lParam[3][0]
			lDsInv = lParam[3][1]
			xIn = False  # helps determine downstream direction in relation to X connectors
			for j, v in enumerate(lLoc):
				found = False
				found_dns = False
				minDist = 99999
				for i, (lName2, lParam2) in enumerate(sorted(lineDict.items())):  # sort dict so x connectors are assessed first
					lLoc2 = lParam2[0]
					lFid2 = lParam2[1]
					if lName == lName2:
						continue
					if found and not dnsConn:
						break
					for j2, v2 in enumerate(lLoc2):
						if v == v2:
							found = True
							if 'connector' in lName:
								if j == 0 and j2 == 0:  # X Connector is entering side channel
									found_dns = True
									xIn = True
									if lName not in xIns:
										xIns.append(lName)
									if lName not in dsNwk.keys():
										dsNwk[lName] = [[lName2]]
									else:
										dsNwk[lName][0].append(lName2)
									if len(dsNwk[lName]) < 2:
										dsNwk[lName].append([lUsInv, lDsInv])
									if len(dsNwk[lName]) < 3:
										dsNwk[lName].append([])
								elif j == 1 and j2 == 0 and not xIn:  # X connector is leaving side channel
									found_dns = True
									if lName not in dsNwk.keys():
										dsNwk[lName] = [[lName2]]
									else:
										dsNwk[lName][0].append(lName2)
									if len(dsNwk[lName]) < 2:
										dsNwk[lName].append([lUsInv, lDsInv])
									if len(dsNwk[lName]) < 3:
										dsNwk[lName].append([])
							elif 'connector' in lName2:  # end normal nwk connected to end X conn
								if lName2 in xIns:  # entering side channel
									if j == 1 and j2 == 1:
										found_dns = True
										if lName not in dsNwk.keys():
											dsNwk[lName] = [[lName2]]
										else:
											dsNwk[lName][0].append(lName2)
										if len(dsNwk[lName]) < 2:
											dsNwk[lName].append([lUsInv, lDsInv])
										if len(dsNwk[lName]) < 3:
											dsNwk[lName].append([])
								else:  # leaving side channel
									if j == 1 and j2 == 0:
										found_dns = True
										if lName not in dsNwk.keys():
											dsNwk[lName] = [[lName2]]
										else:
											dsNwk[lName][0].append(lName2)
										if len(dsNwk[lName]) < 2:
											dsNwk[lName].append([lUsInv, lDsInv])
										if len(dsNwk[lName]) < 3:
											dsNwk[lName].append([])
							else:  # normal connection
								if j == 1 and j2 == 0:  # end vertex connected to fist vertex i.e. found a dns nwk
									found_dns = True
									if lName not in dsNwk.keys():
										dsNwk[lName] = [[lName2]]
									else:
										dsNwk[lName][0].append(lName2)
									if len(dsNwk[lName]) < 2:
										dsNwk[lName].append([lUsInv, lDsInv])
									if len(dsNwk[lName]) < 3:
										angle = getAngle(lLoc, lLoc2)
										dsNwk[lName].append([angle])
									else:
										angle = getAngle(lLoc, lLoc2)
										if angle not in dsNwk[lName][2]:
											dsNwk[lName][2].append(angle)
							continue
						else:
							dist = ((v2[0] - v[0]) ** 2 + (v2[1] - v[1]) ** 2) ** 0.5
							minDist = min(minDist, dist)
							if minDist == dist:
								v3 = v2
								name = lName2
								node = j2
					if i + 1 == lineDict_len and not found_dns:
						dsNwk[lName] = [[], [lUsInv, lDsInv], []]
					if i + 1 == lineDict_len and not found:
						dsNwk[lName] = [[], [lUsInv, lDsInv]]
						if lName not in unsnapped_names:
							unsnapped_names.append(lName)
						if j == 0:
							unsnapped.append('{0} upstream'.format(lName))
							closestV['{0}==0'.format(lName)] = [lyr, lFid, '{0}=={1}'.format(name, node), v3, minDist]
						else:
							unsnapped.append('{0} downstream'.format(lName))
							closestV['{0}==1'.format(lName)] = [lyr, lFid, '{0}=={1}'.format(name, node), v3, minDist]
		
		if not checkPoint:
			return unsnapped, unsnapped_names, closestV, dsNwk
		
	# Check to see if point is snapped to a line
	if checkPoint:
		for pName, pParam in pointDict.items():  # loop through all points
			pLoc = pParam[0]
			pFid = pParam[1]
			lyr = pParam[2]
			pUsInv = pParam[3][0]
			pDsInv = pParam[3][1]
			found = False
			minDist = 99999
			for i, (lName, lParam) in enumerate(lineDict.items()):  # loop through all lines
				lLoc = lParam[0]
				lFid = lParam[1]
				lUsInv = lParam[3][0]
				lDsInv = lParam[3][1]
				if found and not dnsConn:
					break
				for j, coord in enumerate(lLoc):
					if coord == pLoc[0]:
						found = True
						if dnsConn:
							if j == 0:
								if lUsInv == -99999:
									if pDsInv != -99999:
										usInv = pDsInv
									else:
										usInv = -99999
								else:
									usInv = lUsInv
								if lName not in dsNwk.keys():
									dsNwk[lName] = [[], [usInv]]
								else:
									if len(dsNwk[lName]) < 2:
										dsNwk[lName].append([usInv])
									else:
										dsNwk[lName][1][0] = usInv
							elif j == 1:
								if lDsInv == -99999:
									if pDsInv != -99999:
										dsInv = pDsInv
									else:
										dsInv = -99999
								else:
									dsInv = lDsInv
								if lName not in dsNwk.keys():
									dsNwk[lName] = [[], [dsInv]]
								else:
									if len(dsNwk[lName]) < 2:
										dsNwk[lName].append([dsInv])
									else:
										dsNwk[lName][1][1] = dsInv
						continue
					else:
						dist = ((coord[0] - pLoc[0][0]) ** 2 + (coord[1] - pLoc[0][1]) ** 2) ** 0.5
						minDist = min(minDist, dist)
						if minDist == dist:
							v = coord
							name = lName
							node = j
				if i + 1 == lineDict_len and not found:
					unsnapped.append(pName)
					closestV['{0}'.format(pName)] = [lyr, pFid, '{0}=={1}'.format(name, node), v, minDist]
	
		if not dnsConn:
			return unsnapped, closestV
		else:
			return unsnapped, unsnapped_names, closestV, dsNwk


def findAllRasterLyrs():
	"""
	
	:return: list of open raster layers
	"""
	
	rasterLyrs = []
	for name, search_layer in QgsMapLayerRegistry.instance().mapLayers().iteritems():
		if search_layer.type() == 1:
			rasterLyrs.append(name)
			
	return rasterLyrs


def moveVertices(lyrs, vertices_dict, dist):
	"""
	Edits the vertices within the layer to the snap location if within the distance
	
	:param lyr: layer being edited
	:param dist: allowed move distance
	:param vertices_dict: dictionary containing all required information 
	{origin name: [origin layer, origin fid, closest vertex name, closest vertex coords, distance to closest vertex]}
	:return: string of logged moves
	"""
	
	editedV = []
	node = None
	log = ''
	for lyr in lyrs:
		lyr.startEditing()
		for id, param in vertices_dict.items():
			if lyr == param[0]:
				if id not in editedV:
					if param[4] <= dist:
						if len(id.split('==')) > 1:
							name, node = id.split('==')
						else:
							name = id
						fid = param[1]
						id2 = param[2]
						name2, node2 = id2.split('==')
						v = param[3]
						if node is None or node == '0':
							lyr.moveVertex(v[0], v[1], fid, 0)
						else:
							for feature in lyr.getFeatures():  # QGIS 3 has the ability to select by FID rather than loop
								if feature.id() == fid:
									vertices = feature.geometry().asPolyline()
									lastVertex = len(vertices) - 1
							lyr.moveVertex(v[0], v[1], fid, lastVertex)
						editedV.append(id)
						editedV.append(id2)
						if node is None:
							if node2 == '0':
								log += 'Connected {0} to {1} upstream ({2:.4f}, {3:.4f})\n'.format(name, name2, v[0], v[1])
							else:
								log += 'Connected {0} to {1} downstream ({2:.4f}, {3:.4f})\n'.format(name, name2, v[0], v[1])
						elif node == '0':
							if node2 == '0':
								log += 'Connected {0} upstream to {1} upstream ({2:.4f}, {3:.4f})\n'.format(name, name2, v[0], v[1])
							else:
								log += 'Connected {0} upstream to {1} downstream ({2:.4f}, {3:.4f})\n'.format(name, name2, v[0], v[1])
						else:
							if node2 == '0':
								log += 'Connected {0} downstream to {1} upstream ({2:.4f}, {3:.4f})\n'.format(name, name2, v[0], v[1])
							else:
								log += 'Connected {0} downstream to {1} downstream ({2:.4f}, {3:.4f})\n'.format(name, name2, v[0], v[1])
		lyr.commitChanges()

	return log


def listToString(lst):
	"""
	
	:param lst: list of int
	:return: string
	"""
	
	s = ''
	if len(lst) > 0:
		for i, l in enumerate(lst):
			if i == 0:
				s += '{0}'.format(l)
			else:
				s += ' - {0}'.format(l)
	
	return s


def checkDnsNwk(dsLines, startLine, inLyrs, angleLimit):
	"""
	From a starting point, will list all downstream connections until there are none left. It will also print out inverts,
	pipe size, and flow area. It will flag decrease in conveyance and adverse gradients.
	
	:param dsLines: dict {origin name: [[dns nwk names], [us invert, ds invert]]}
	:param startline: string start id
	:param inLyrs: list of QgsVectorLayers
	:return: string log	
	"""

	log = 'ID,Type,Number,Width,Height,Area,Us Invert,Ds Invert,Min Angle into Downstream Pipe,Area Decrease,Adverse Gradient,Sharp Angle\n'
	keyPrev = None
	keys = startLine
	area_prev = 0
	dsInv_prev = 99999
	dns = True
	bn = []  # branched network names to be dealt with at the end
	while dns:
		features = []
		for lyr in inLyrs:
			fld = lyr.fields()[0]
			for key in keys:
				filter = '"{0}" = \'{1}\''.format(fld.name(), key)
				request = QgsFeatureRequest().setFilterExpression(filter)
				for f in lyr.getFeatures(request):
					features.append(f)
		if len(keys) == 1:  # one downstream channel
			typ = features[0].attributes()[1]
			if typ.lower() == 'r':
				no = int(features[0].attributes()[15])
				width = float(features[0].attributes()[13])
				height = float(features[0].attributes()[14])
				usInv = float(dsLines[keys[0]][1][0])
				dsInv =  float(dsLines[keys[0]][1][1])
				area = float(no) * width * height
				if len(dsLines[keys[0]][2]) > 0:
					angle = min(dsLines[keys[0]][2])
				else:
					angle = 0
				advSlope = ''
				if (dsInv > usInv and usInv != -99999.00) or (usInv > dsInv_prev and dsInv_prev != -99999.00):
					advSlope = 'T'
				decArea = ''
				if area < area_prev:
					decArea = 'T'
				sharpAngle = ''
				if angle < angleLimit and angle != 0:
					sharpAngle = 'T'
				log += '{0},{1},{2},{3:.2f},{4:.2f},{5:.2f},{6:.2f},{7:.2f},{8:.1f},{9},{10},{11}\n'.\
				   format(keys[0], typ, no, width, height, area, usInv, dsInv, angle, decArea, advSlope, sharpAngle)
			elif typ.lower() == 'c':
				no = int(features[0].attributes()[15])
				width = float(features[0].attributes()[13])
				height = 0
				usInv = float(dsLines[keys[0]][1][0])
				dsInv = float(dsLines[keys[0]][1][1])
				area = float(no) * (width / 2) ** 2 * 3.14
				if len(dsLines[keys[0]][2]) > 0:
					angle = min(dsLines[keys[0]][2])
				else:
					angle = 0
				advSlope = ''
				if (dsInv > usInv and usInv != -99999.00) or (usInv > dsInv_prev and dsInv_prev != -99999.00):
					advSlope = 'T'
				decArea = ''
				if area < area_prev:
					decArea = 'T'
				sharpAngle = ''
				if angle < angleLimit and angle != 0:
					sharpAngle = 'T'
				log += '{0},{1},{2},{3:.2f},{4:.2f},{5:.2f},{6:.2f},{7:.2f},{8:.1f},{9},{10},{11}\n'. \
					format(keys[0], typ, no, width, height, area, usInv, dsInv, angle, decArea, advSlope, sharpAngle)
			else:
				log += '{0},{1}\n'.format(keys[0], typ)
			if keys[0] in dsLines.keys():
				if len(dsLines[keys[0]][0]) == 0:
					dns = False
				else:
					keyPrev = keys[0]
					area_prev = area
					dsInv_prev = dsInv
					keys = dsLines[keys[0]][0]
			else:
				dns = False
		elif len(keys) > 1:  # consider what happens if there are 2 downstream channels
			# get channels accounting for X connectors
			nwks = []
			for key in keys:
				if 'connector' in key:
					key = dsLines[key][0][0]
				nwks.append(key)
			# get next downstream channels accounting for X connectors
			dns_nwks = []
			for nwk in nwks:
				if nwk in dsLines.keys():
					if len(dsLines[nwk][0]) == 0:
						dns_nwks.append('DOWNSTREAM NODE')
					else:
						dns_nwk = dsLines[nwk][0][0]
						if 'connector' in dns_nwk:
							dns_nwk = dsLines[dns_nwk][0][0]
						dns_nwks.append(dns_nwk)
				else:
					dns_nwks.append('DOWNSTREAM NODE')
			# check if dns nwk is the same
			# if it is the same dns nwk, then it is probably part of the same network branch
			# if it is different, then the network has probably split into a second branch
			branches = []  # split downstream channels into branches
			for i, dns_nwk in enumerate(dns_nwks):
				for i2, dns_nwk2 in enumerate(dns_nwks):
					already = False
					if i != i2:
						for b in branches:
							if i in b:
								already = True
						if not already:
							if dns_nwk == dns_nwk2:
								branches.append([i, i2])
							else:
								branches.append([i])
			for branch in branches:
				a = []
				for bi in branch:
					a.append(nwks[bi])
				bn.append(a)
			if len(branches) == 1:
				bn.pop()
				fld = lyr.fields()[0]
				features = []
				for lyr in inLyrs:
					for nwk in nwks:
						filter = '"{0}" = \'{1}\''.format(fld.name(), nwk)
						request = QgsFeatureRequest().setFilterExpression(filter)
						for f in lyr.getFeatures(request):
							features.append(f)
				typs = []
				nos = []
				widths = []
				heights = []
				usInvs = []
				dsInvs = []
				areas = []
				angles = []
				for nwk in nwks:
					for f in features:
						name = f.attributes()[0]
						if nwk == name:
							typ = f.attributes()[1]
							typs.append(typ)
							if typ.lower() == 'r':
								nos.append(int(f.attributes()[15]))
								widths.append(float(f.attributes()[13]))
								heights.append(float(f.attributes()[14]))
								usInv = float(dsLines[nwk][1][0])
								dsInv = float(dsLines[nwk][1][1])
								areas.append(
									float(f.attributes()[15]) * float(f.attributes()[13]) * float(f.attributes()[14]))
								if len(dsLines[nwk][2]) > 0:
									angles.append(min(dsLines[nwk][2]))
								else:
									angles.append(0)
							elif typ.lower() == 'c':
								nos.append(int(f.attributes()[15]))
								widths.append(float(f.attributes()[13]))
								heights.append(0)
								usInv = float(dsLines[nwk][1][0])
								dsInv = float(dsLines[nwk][1][1])
								areas.append(
									float(f.attributes()[15]) * (float(f.attributes()[13]) / 2) ** 2 * 3.14)
								if len(dsLines[nwk][2]) > 0:
									angles.append(min(dsLines[nwk][2]))
								else:
									angles.append(0)
				area = sum(areas)
				angle = min(angles)
				advSlope = ''
				if (min(dsInv) > min(usInv) and min(usInv) != -99999) or (
						min(usInv) > dsInv_prev and dsInv_prev != -99999):
					advSlope = 'T'
				decArea = ''
				if area < area_prev:
					decArea = 'T'
				sharpAngle = ''
				if angle < angleLimit:
					sharpAngle = 'T'
				if 'r' in typs or 'R' in typs or 'c' in typs or 'C' in typs:
					log += '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}\n'. \
						format(listToString(nwks), listToString(typs), listToString(nos), listToString(widths),
					           listToString(heights), area, listToString(usInvs), listToString(dsInvs), angle, decArea,
					           advSlope, sharpAngle)
				else:
					log += '{0},{1}\n'.format(listToString(nwks), listToString(typs))
				if nwks[0] in dsLines.keys():
					if len(dsLines[nwks[0]][0]) == 0:
						dns = False
					else:
						keyPrev = keys[0]
						area_prev = area
						dsInv_prev = min(dsInvs)
						keys = dsLines[nwks[0]][0]
				else:
					dns = False
			elif len(branches) > 1:
				log += '-- Branch split at {0} into {1} branches - '.format(keyPrev, len(branches))
				for i, b in enumerate(bn):
					if len(b) < 2:
						if i == 0:
							log += '{0}'.format(b[0])
						elif i < len(bn) - 1:
							log += ', {0}'.format(b[0])
						else:
							log += ', {0}\n'.format(b[0])
					else:
						a = '('
						for j, br in enumerate(b):
							if j < len(br) - 1:
								a += '{0}'.format(br)
							else:
								a += '{0})'.foramt(br)
						if i == 0:
							log += '{0}'.format(a)
						elif i < len(bn) - 1:
							log += ', {0}'.format(a)
						else:
							log += ', {0}\n'.format(a)
				if nwks[0] in dsLines.keys():
					keys = dsLines[nwks[0]][0]
				dns = False

	return log, bn
	