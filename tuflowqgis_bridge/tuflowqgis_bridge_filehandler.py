# coding=utf-8
from PyQt4.QtGui import *
import os
from tuflow.tuflowqgis_library import tuflowqgis_find_layer
from tuflowqgis_bridge_editor import *


def convertListToString(input_list):
	text = ''
	try:
		if type(input_list[0]) == list:  # 2D list
			for i, lst in enumerate(input_list):
				for j, x in enumerate(lst):
					if j == 0:
						text += '{0}'.format(x)
					else:
						text += ', {0}'.format(x)
				if i == 0:
					text += ' | '
		else:
			for j, x in enumerate(input_list):
				if j == 0:
					text += '{0}'.format(x)
				else:
					text += ', {0}'.format(x)
	except:
		pass
	return text


def convertStringToList(input_string):
	subvalue = input_string.strip("'").strip('"')
	subvalue = input_string.split('|')
	if len(subvalue) == 2:
		x = subvalue[0].strip().split(',')
		y = subvalue[1].strip().split(',')
		try:
			x_strip = []
			y_strip = []
			for i in x:
				x_strip.append(str(float(i)))  # should all be numbers, this checks and also strips
			for i in y:
				y_strip.append(str(float(i)))
			return [x_strip, y_strip]
		except:
			return [[], []]
	else:
		x = subvalue[0].strip().split(',')
		x_strip = []
		try:
			for i in x:
				x_strip.append(str(float(i)))
			return x_strip
		except:
			return []


def saveFile(bridge_gui):
	openFiles = []
	for key, bridge in bridge_gui.bridges.items():
		text = []
		lyrName, fid = key.split(',')
		lyr = tuflowqgis_find_layer(lyrName)
		lyrSource = lyr.dataProvider().dataSourceUri().split('|')[0]
		newFile = '{0}.tuflowbridge'.format(os.path.splitext(lyrSource)[0])
		try:
			if newFile not in openFiles:
				writeNewFile = open(newFile, 'w')
				openFiles.append(newFile)
			else:
				writeNewFile = open(newFile, 'a')
		except IOError:
			QMessageBox.critical(bridge_gui.iface.mainWindow(), 'Error',
			                     'Cannot open file for editing- check it is not open elsewhere\n{0}'.format(
				                     newFile))
			return
		except:
			QMessageBox.critical(bridge_gui.iface.mainWindow(), 'Error',
			                     'Trouble writing tuflow bridge file\n{0}'.format(newFile))
			return
		text.append('Key == {0}'.format(key))
		text.append('Bridge Name == {0}'.format(bridge.saved_bridgeName))
		text.append('Deck Obvert == {0}'.format(bridge.saved_deckElevationBottom))
		text.append('Deck Thickness == {0}'.format(bridge.saved_deckThickness))
		text.append('Hand Rail Depth == {0}'.format(bridge.saved_handRailDepth))
		text.append('Hand Rail FLC == {0}'.format(bridge.saved_handRailFlc))
		text.append('Hand Rail Blockage == {0}'.format(bridge.saved_handRailBlockage))
		text.append('Deck Drowned == {0}'.format(bridge.saved_rbDrowned))
		text.append('Pier Number == {0}'.format(bridge.saved_pierNo))
		text.append('Pier Width == {0}'.format(bridge.saved_pierWidth))
		text.append('Pier Start == {0}'.format(bridge.saved_pierWidthLeft))
		text.append('Pier Gap == {0}'.format(bridge.saved_pierGap))
		text.append('Pier Shape == {0}'.format(bridge.saved_pierShape))
		text.append('Z Line Width == {0}'.format(bridge.saved_zLineWidth))
		text.append('Enforce In Terrain == {0}'.format(bridge.saved_enforceInTerrain))
		text.append('Cross Section Table Row Count == {0}'.format(bridge.saved_xSectionRowCount))
		text.append('Cross Section Table == {0}'.format(convertListToString(bridge.saved_xSectionTable)))
		text.append('Bridge Deck Table Row Count == {0}'.format(bridge.saved_deckRowCount))
		text.append('Bridge Deck Table == {0}'.format(convertListToString(bridge.saved_deckTable)))
		text.append('Bridge Pier Table Row Count == {0}'.format(bridge.saved_pierRowCount))
		text.append('Bridge Pier Table == {0}'.format(convertListToString(bridge.saved_pierTable)))
		text.append('\n')
		writeNewFile.write('\n'.join(text))
		writeNewFile.close()


def loadFile(bridge_gui, file):
	bridge_gui.bridges = {}
	with open(file, 'r') as fo:
		for line in fo:
			try:
				key, value = line.split('==')
			except:
				continue
			key = key.strip()
			value = value.strip()
			if key == 'Key':
				bridge_editor = bridgeEditor(bridge_gui, bridge_gui.iface)
				for subline in fo:
					tell = fo.tell()
					if subline == '\n':
						break
					try:
						parameter, subvalue = subline.split('==')
					except:
						continue
					parameter = parameter.strip()
					subvalue = subvalue.strip()
					if parameter == 'Bridge Name':
						bridge_editor.saved_bridgeName = subvalue
					elif parameter == 'Deck Obvert':
						bridge_editor.saved_deckElevationBottom = float(subvalue)
					elif parameter == 'Deck Thickness':
						bridge_editor.saved_deckThickness = float(subvalue)
					elif parameter == 'Hand Rail Depth':
						bridge_editor.saved_handRailDepth = float(subvalue)
					elif parameter == 'Hand Rail FLC':
						bridge_editor.saved_handRailFlc = float(subvalue)
					elif parameter == 'Hand Rail Blockage':
						bridge_editor.saved_handRailBlockage = float(subvalue)
					elif parameter == 'Deck Drowned':
						bridge_editor.saved_rbDrowned = True if subvalue == 'True' else False
					elif parameter == 'Pier Number':
						bridge_editor.saved_pierNo = float(subvalue)
					elif parameter == 'Pier Width':
						bridge_editor.saved_pierWidth = float(subvalue)
					elif parameter == 'Pier Start':
						bridge_editor.saved_pierWidthLeft = float(subvalue)
					elif parameter == 'Pier Gap':
						bridge_editor.saved_pierGap = float(subvalue)
					elif parameter == 'Pier Shape':
						bridge_editor.saved_pierShape = int(subvalue)
					elif parameter == 'Z Line Width':
						bridge_editor.saved_zLineWidth = float(subvalue)
					elif parameter == 'Enforce In Terrain':
						bridge_editor.saved_enforceInTerrain = True if subvalue == 'True' else False
					elif parameter == 'Cross Section Table Row Count':
						bridge_editor.saved_xSectionRowCount = float(subvalue)
					elif parameter == 'Cross Section Table':
						bridge_editor.saved_xSectionTable = convertStringToList(subvalue)
					elif parameter == 'Bridge Deck Table Row Count':
						bridge_editor.saved_deckRowCount = float(subvalue)
					elif parameter == 'Bridge Deck Table':
						bridge_editor.saved_deckTable = convertStringToList(subvalue)
					elif parameter == 'Bridge Pier Table Row Count':
						bridge_editor.saved_pierRowCount = float(subvalue)
					elif parameter == 'Bridge Pier Table':
						bridge_editor.saved_pierTable = convertStringToList(subvalue)
					elif parameter == 'Key':
						fo.seek(1)  # gone to far. Need to rewind to just after the first line
						break
				bridge_editor.connected = False
				bridge_editor.gui = None
				bridge_gui.bridges[value] = bridge_editor
				