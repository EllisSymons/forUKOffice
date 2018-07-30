# coding=utf-8
import os
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *


def plotterMenu(bridge_editor, pos):
	"""
	graph right click menu
	
	:param bridge_editor: tuflowqgis_bridge_editor class object
	:param pos: position on widget
	:return:
	"""
	
	menu = QMenu(bridge_editor.bridge)
	exportCsv_action = QAction("Export Plot Data to Csv", menu)
	exportCsv_action.triggered.connect(lambda: export_csv(bridge_editor))
	menu.addAction(exportCsv_action)
	menu.popup(bridge_editor.bridge.plotWdg.mapToGlobal(pos))


def xSectionTableMenu(bridge_editor, pos):
	"""
	Table right click menu
	
	:param bridge_editor: tuflowqgis_bridge_editor class object
	:param pos: QPoint & pos
	:return:
	"""
	
	menu = QMenu(bridge_editor.bridge)
	insertRowBefore_action = QAction("Insert Row (before)", menu)
	insertRowAfter_action = QAction("Insert Row (after)", menu)
	deleteRow_action = QAction("Delete Row", menu)
	insertRowBefore_action.triggered.connect(lambda: insertRowBefore(bridge_editor, bridge_editor.bridge.xSectionTable))
	insertRowAfter_action.triggered.connect(lambda: insertRowAfter(bridge_editor, bridge_editor.bridge.xSectionTable))
	deleteRow_action.triggered.connect(lambda: deleteRow(bridge_editor, bridge_editor.bridge.xSectionTable))
	menu.addAction(insertRowBefore_action)
	menu.addAction(insertRowAfter_action)
	menu.addAction(deleteRow_action)
	menu.popup(bridge_editor.bridge.pierTable.mapToGlobal(pos))


def deckTableMenu(bridge_editor, pos):
	"""
	Table right click menu
	
	:param bridge_editor: tuflowqgis_bridge_editor class object
	:param pos: QPoint & pos
	:return:
	"""
	
	menu = QMenu(bridge_editor.bridge)
	insertRowBefore_action = QAction("Insert Row (before)", menu)
	insertRowAfter_action = QAction("Insert Row (after)", menu)
	deleteRow_action = QAction("Delete Row", menu)
	insertRowBefore_action.triggered.connect(lambda: insertRowBefore(bridge_editor, bridge_editor.bridge.deckTable))
	insertRowAfter_action.triggered.connect(lambda: insertRowAfter(bridge_editor, bridge_editor.bridge.deckTable))
	deleteRow_action.triggered.connect(lambda: deleteRow(bridge_editor, bridge_editor.bridge.deckTable))
	menu.addAction(insertRowBefore_action)
	menu.addAction(insertRowAfter_action)
	menu.addAction(deleteRow_action)
	menu.popup(bridge_editor.bridge.pierTable.mapToGlobal(pos))


def pierTableMenu(bridge_editor, pos):
	"""
	Table right click menu

	:param bridge_editor: tuflowqgis_bridge_editor class object
	:param pos: QPoint & pos
	:return:
	"""
	
	menu = QMenu(bridge_editor.bridge)
	insertRowBefore_action = QAction("Insert Row (before)", menu)
	insertRowAfter_action = QAction("Insert Row (after)", menu)
	deleteRow_action = QAction("Delete Row", menu)
	insertRowBefore_action.triggered.connect(lambda: insertRowBefore(bridge_editor, bridge_editor.bridge.pierTable))
	insertRowAfter_action.triggered.connect(lambda: insertRowAfter(bridge_editor, bridge_editor.bridge.pierTable))
	deleteRow_action.triggered.connect(lambda: deleteRow(bridge_editor, bridge_editor.bridge.pierTable))
	menu.addAction(insertRowBefore_action)
	menu.addAction(insertRowAfter_action)
	menu.addAction(deleteRow_action)
	menu.popup(bridge_editor.bridge.pierTable.mapToGlobal(pos))


def insertRowBefore(bridge_editor, table):
	"""
	Insert row in QTableWidget before the current selection

	:param bridge_editor: tuflowqgis_bridge_editor class object
	:param table: QTableWidget
	:return:
	"""
	
	# Get selected row
	currentRow = table.currentRow()
	if currentRow is None:
		bridge_editor.bridge.statusLog.insertItem(0, 'Error: No row selected')
		bridge_editor.bridge.statusLabel.setText('Status: Error')
		return
	# store data
	x = []  # list of strings
	y = []  # list of strings
	for i in range(table.rowCount()):
		x.append(table.item(i, 0).text())
		if table != bridge_editor.bridge.pierTable:
			y.append(table.item(i, 1).text())
	# add row and populate data
	table.setRowCount(len(x) + 1)
	if table == bridge_editor.bridge.pierTable:  # populate pier numbering
		headers = ['Pier {0}'.format(p) for p in range(1, table.rowCount() + 1)]
		table.setVerticalHeaderLabels(headers)
	for i in range(table.rowCount()):
		if i < currentRow:
			table.setItem(i, 0, QTableWidgetItem(x[i]))
			if table != bridge_editor.bridge.pierTable:
				table.setItem(i, 1, QTableWidgetItem(y[i]))
		elif i == currentRow:
			table.setItem(i, 0, QTableWidgetItem('0'))
			if table != bridge_editor.bridge.pierTable:
				table.setItem(i, 1, QTableWidgetItem('0'))
		elif i > currentRow:
			table.setItem(i, 0, QTableWidgetItem(x[i - 1]))
			if table != bridge_editor.bridge.pierTable:
				table.setItem(i, 1, QTableWidgetItem(y[i - 1]))
	# update class properties for XSection data
	if table == bridge_editor.bridge.xSectionTable:
		bridge_editor.updateXsectionData()
	# Update spinbox
	dict = {bridge_editor.bridge.xSectionTable: bridge_editor.bridge.xSectionRowCount, bridge_editor.bridge.deckTable: bridge_editor.bridge.deckRowCount,
	        bridge_editor.bridge.pierTable: bridge_editor.bridge.pierRowCount}
	spinBox = dict[table]
	spinBox.setValue(table.rowCount())


def insertRowAfter(bridge_editor, table):
	"""
	Insert row in QTableWidget after the current selection

	:param bridge_editor: tuflowqgis_bridge_editor class object
	:param table: QTableWidget
	:return:
	"""
	
	# Get selected row
	currentRow = table.currentRow() + 1  # add one so it is inserted after
	if currentRow is None:
		bridge_editor.bridge.statusLog.insertItem(0, 'Error: No row selected')
		bridge_editor.bridge.statusLabel.setText('Status: Error')
		return
	# store data
	x = []  # list of strings
	y = []  # list of strings
	for i in range(table.rowCount()):
		x.append(table.item(i, 0).text())
		if table != bridge_editor.bridge.pierTable:
			y.append(table.item(i, 1).text())
	# add row and populate data
	table.setRowCount(len(x) + 1)
	if table == bridge_editor.bridge.pierTable:  # populate pier numbering
		headers = ['Pier {0}'.format(p) for p in range(1, table.rowCount() + 1)]
		table.setVerticalHeaderLabels(headers)
	for i in range(table.rowCount()):
		if i < currentRow:
			table.setItem(i, 0, QTableWidgetItem(x[i]))
			if table != bridge_editor.bridge.pierTable:
				table.setItem(i, 1, QTableWidgetItem(y[i]))
		elif i == currentRow:
			table.setItem(i, 0, QTableWidgetItem('0'))
			if table != bridge_editor.bridge.pierTable:
				table.setItem(i, 1, QTableWidgetItem('0'))
		elif i > currentRow:
			table.setItem(i, 0, QTableWidgetItem(x[i - 1]))
			if table != bridge_editor.bridge.pierTable:
				table.setItem(i, 1, QTableWidgetItem(y[i - 1]))
	# update class properties for XSection data
	if table == bridge_editor.bridge.xSectionTable:
		bridge_editor.updateXsectionData()
	# Update spinbox
	dict = {bridge_editor.bridge.xSectionTable: bridge_editor.bridge.xSectionRowCount, bridge_editor.bridge.deckTable: bridge_editor.bridge.deckRowCount,
	        bridge_editor.bridge.pierTable: bridge_editor.bridge.pierRowCount}
	spinBox = dict[table]
	spinBox.setValue(table.rowCount())


def deleteRow(bridge_editor, table):
	"""
	Delete selected row

	:param bridge_editor: tuflowqgis_bridge_editor class object
	:param table: QTableWidget
	:return:
	"""
	
	# get selected row
	currentRow = table.currentRow()
	if currentRow is None:
		bridge_editor.bridge.statusLog.insertItem(0, 'Error: No row selected')
		bridge_editor.bridge.statusLabel.setText('Status: Error')
		return
	# store data
	x = []  # list of strings
	y = []  # list of strings
	for i in range(table.rowCount()):
		x.append(table.item(i, 0).text())
		if table != bridge_editor.bridge.pierTable:
			y.append(table.item(i, 1).text())
	# remove row and populate data
	table.setRowCount(len(x) - 1)
	if table == bridge_editor.bridge.pierTable:  # populate pier numbering
		headers = ['Pier {0}'.format(p) for p in range(1, table.rowCount() - 1)]
		table.setVerticalHeaderLabels(headers)
	x.pop(currentRow)
	if table != bridge_editor.bridge.pierTable:
		y.pop(currentRow)
	for i in range(table.rowCount()):
		table.setItem(i, 0, QTableWidgetItem(x[i]))
		if table != bridge_editor.bridge.pierTable:
			table.setItem(i, 1, QTableWidgetItem(y[i]))
	# update class properties for XSection data
	if table == bridge_editor.bridge.xSectionTable:
		bridge_editor.updateXsectionData()
	# Update spinbox
	dict = {bridge_editor.bridge.xSectionTable: bridge_editor.bridge.xSectionRowCount, bridge_editor.bridge.deckTable: bridge_editor.bridge.deckRowCount,
	        bridge_editor.bridge.pierTable: bridge_editor.bridge.pierRowCount}
	spinBox = dict[table]
	spinBox.setValue(table.rowCount())


def tableRowCountChanged(bridge_editor, spinBox, table):
	"""
	Updates QTableWidget rows based on spinbox

	:param bridge_editor: tuflowqgis_bridge_editor class object
	:param spinBox: QSpinBox
	:param table: QTableWidget
	:return:
	"""
	
	# get number of rows
	rowCount = spinBox.value()
	# set number of rows - by default the last row is added and deleted
	table.setRowCount(rowCount)
	if table == bridge_editor.bridge.pierTable:
		headers = headers = ['Pier {0}'.format(p) for p in range(1, table.rowCount() + 1)]
		table.setVerticalHeaderLabels(headers)


def export_csv(bridge_editor):
	"""
	Export XS to csv

	:param bridge_editor: tuflowqgis_bridge_editor class object
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
		maxLen = max(maxLen, len(bridge_editor.bridge.subplot.lines[i].get_data()[0]))
	# Get data
	for i, resultFile in enumerate(resultFiles):
		if i == 0:
			data = bridge_editor.bridge.subplot.lines[c[i]].get_data()[0]  # write X axis first
			data = numpy.reshape(data, [len(data), 1])
			if len(data) < maxLen:
				diff = maxLen - len(data)
				fill = numpy.zeros([diff, 1]) * numpy.nan
				data = numpy.append(data, fill, axis=0)
		else:
			dataX = bridge_editor.bridge.subplot.lines[c[i]].get_data()[0]  # Write X axis again for new results
			dataX = numpy.reshape(dataX, [len(dataX), 1])
			if len(dataX) < maxLen:
				diff = maxLen - len(dataX)
				fill = numpy.zeros([diff, 1]) * numpy.nan
				dataX = numpy.append(dataX, fill, axis=0)
			data = numpy.append(data, dataX, axis=1)
		if i < len(c) - 1:  # isn't last result file
			for line in bridge_editor.bridge.subplot.lines[c[i]:c[i + 1]]:
				dataY = line.get_data()[1]
				dataY = numpy.reshape(dataY, [len(dataY), 1])
				if len(dataY) < maxLen:
					diff = maxLen - len(dataY)
					fill = numpy.zeros([diff, 1]) * numpy.nan
					dataY = numpy.append(dataY, fill, axis=0)
				data = numpy.append(data, dataY, axis=1)
		else:  # is last result file
			for line in bridge_editor.bridge.subplot.lines[c[i]:]:
				dataY = line.get_data()[1]
				dataY = numpy.reshape(dataY, [len(dataY), 1])
				if len(dataY) < maxLen:
					diff = maxLen - len(dataY)
					fill = numpy.zeros([diff, 1]) * numpy.nan
					dataY = numpy.append(dataY, fill, axis=0)
				data = numpy.append(data, dataY, axis=1)
	# Save data out
	saveFile = QFileDialog.getSaveFileName(bridge_editor.bridge, 'Save File', fpath)
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
			bridge_editor.bridge.statusLog.insertItem(0, 'Error: Opening File for editing')
			bridge_editor.bridge.statusLabel.setText('Status: Error')
			return
	bridge_editor.bridge.statusLog.insertItem(0, 'Successfully exported csv')
	bridge_editor.bridge.statusLabel.setText('Status: Successful')