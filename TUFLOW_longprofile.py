# coding=utf-8
import sys
import numpy as np
from tuflowqgis_library import *
#sys.path.append(r'C:\Program Files\JetBrains\PyCharm 2018.1\debug-eggs')
#sys.path.append(r'C:\Program Files\JetBrains\PyCharm 2018.1\helpers\pydev')
#import pydevd

class LongProfile():
	"""
	Class to keep plot data for long profile in TUPLOT
	
	"""
	
	def __init__(self):
		self.x = []
		self.bed = []
		self.pipes = []
		self.ground = []
		self.branches = []
		self.dnsPipe = []
		
	def addX(self, x):
		"""
		Add X values for plot.
		
		:param x: list
		:return: void
		"""
		
		for item in x:
			xAccum = []
			for i, a in enumerate(item):
				if i == 0:
					xAccum.append(a)
				elif i + 1 == len(item):
					xAccum.append(xAccum[i - 1] + a)
				else:
					xAccum.append(xAccum[i - 1] + a)
					xAccum.append(xAccum[i - 1] + a)
			self.x.append(xAccum)
		
	def addBed(self, bed):
		"""
		Add Y axis values for bed
		
		:param bed: list
		:return: void
		"""
		
		for item in bed:
			self.bed.append(item)
	
	def addPipes(self, pipes):
		"""
		Add pipe data
		
		:param pipes: list[list]
		:return: void
		"""

		for i, branch in enumerate(pipes):
			a = []
			b = []
			patch = []
			for j, pipe in enumerate(branch):
				index = j * 2
				a.append(self.x[i][index])
				a.append(self.x[i][index+1])
				a.append(self.x[i][index + 1])
				a.append(self.x[i][index])
				b.append(self.bed[i][index])
				b.append(self.bed[i][index+1])
				b.append(self.bed[i][index + 1] + pipe)
				b.append(self.bed[i][index] + pipe)
				vert = list(zip(a, b))
				patch.append(vert)
			self.pipes.append(patch)
		
	def addGround(self, ground):
		"""
		Add ground data
		
		:param ground: list
		:return: void
		"""
		
		for item in ground:
			self.ground.append(item)
		
	def addBranches(self, branches):
		"""
		Add branch names for long profile
		
		:param branches: list
		:return: void
		"""
		
		for item in branches:
			self.branches.append(item)
			
	def addDnsPipe(self, dnsPipe):
		"""
		Add downstream pipe for the branch
		
		:param dnsPipe: list
		:return: void
		"""
		
		for item in dnsPipe:
			self.dnsPipe.append(item)
			
	def organiseData(self):
		"""
		Organises the data so that they can be plotted relative to one another - Branches flow onto one another.
		
		:return:
		"""
		
		
class DownstreamConnectivity():
	"""
	Class for storing downstream connectivity information
	"""
	
	def __init__(self, dsLines, startLines, inLyrs, angleLimit):
		self.dsLines = dsLines
		self.startLines = startLines
		self.inLyrs = inLyrs
		self.angleLimit = angleLimit
		self.processed_nwks = []
		self.log = ''
		self.type = []
		self.name = []
		self.branchName = []
		self.usInvert = []
		self.dsInvert = []
		self.angle = []
		self.length = []
		self.no = []
		self.width = []
		self.height = []
		self.area = []
		self.branchCounter = 1
		self.branchExists = False
		self.branchDnsConnectionPipe = []
		self.joiningOutlet = []  # only necessary if another pipe is joining at the outlet
		self.upsBranches = []
		self.dnsBranches = []
		self.paths = []
		self.pathsNwks = []
		self.pathsLen = []
		self.pathsX = []
		self.pathsInvert = []
		self.pathsPipe = []
		self.pathsGround = []
		self.ground = []
		self.adverseGradient = []
		self.decreaseFlowArea = []
		self.sharpAngle = []
		self.network = []
		self.bName = []
		self.bUsInvert = []
		self.bDsInvert = []
		self.bAngle = []
		self.bLength = []
		self.bNo = []
		self.bWidth = []
		self.bHeight = []
		self.bArea = []
		self.bDnsConnectionPipe = []
		self.bAdverseGradient = []
		self.bDecreaseFlowArea = []
		self.bSharpAngle = []
		
	def getDownstreamConnectivity(self, network):
		"""
		Determines the 1D network branch and gets the pipe data for it.
		
		:return: void
		"""
		
		self.bType = []
		self.bName = []
		self.bUsInvert = []
		self.bDsInvert = []
		self.bAngle = []
		self.bLength = []
		self.bNo = []
		self.bWidth = []
		self.bHeight = []
		self.bArea = []
		self.bDnsConnectionPipe = []
		self.bAdverseGradient = []
		self.bDecreaseFlowArea = []
		self.bSharpAngle = []
		self.first_sel = True
		area_prev = 0
		dsInv_prev = 99999
		bn = []
		# Determine if there are pipes downstream of starting locations
		if type(network) == list:
			for nwk in network:
				if len(self.dsLines[nwk]) > 0:
					dns = True  # there are downstream pipes available
					break
				else:
					dns = False
		else:
			if len(self.dsLines[network]) > 0:
				network = [network]
				dns = True  # there are downstream pipes available
			else:
				dns = False
		while dns:
			# Get QgsFeature layers for start lines
			adverseGradient = False
			decreaseFlowArea = False
			sharpAngle = False
			features = []
			for lyr in self.inLyrs:
				fld = lyr.fields()[0]
				for nwk in network:
					filter = '"{0}" = \'{1}\''.format(fld.name(), nwk)
					request = QgsFeatureRequest().setFilterExpression(filter)
					for f in lyr.getFeatures(request):
						features.append(f)
			# Get data for starting lines
			if len(network) == 1:  # dealing with one channel
				self.first_sel = False
				self.branchExists = True
				if network[0] in self.processed_nwks:
					self.branchDnsConnectionPipe.append([network[0]])
					self.joiningOutlet.append('JOINING EXISTING BRANCH')
					dns = False
					break
				typ = features[0].attributes()[1]
				length = features[0].attributes()[4]
				if length <= 0:
					length = getLength(features[0])
				name = network[0]
				no = features[0].attributes()[15]
				width = features[0].attributes()[13]
				height = features[0].attributes()[14]
				usInv = self.dsLines[network[0]][1][0]
				dsInv = self.dsLines[network[0]][1][1]
				if network[0] in self.dsLines.keys():
					if len(self.dsLines[network[0]][2]) > 0:
						angle = min(self.dsLines[network[0]][2])
					else:
						angle = 0
				else:
					angle = 0
				if typ.lower() == 'r':
					area = float(no) * width * height
				elif typ.lower() == 'c':
					area = float(no) * (width / 2) ** 2 * 3.14
				else:
					area = 0
				if (dsInv > usInv and usInv != -99999.00) or (usInv > dsInv_prev and dsInv_prev != -99999.00):
					adverseGradient = True
				if area < area_prev and area != 0:
					decreaseFlowArea = True
				if angle < self.angleLimit and angle != 0:
					sharpAngle = True
				self.bType.append(typ)
				self.bLength.append(length)
				self.bName.append(name)
				self.bNo.append(no)
				self.bWidth.append(width)
				self.bHeight.append(height)
				self.bUsInvert.append(usInv)
				self.bDsInvert.append(dsInv)
				self.bAngle.append(angle)
				self.bArea.append(area)
				self.bAdverseGradient.append(adverseGradient)
				self.bDecreaseFlowArea.append(decreaseFlowArea)
				self.bSharpAngle.append(sharpAngle)
				if network[0] in self.dsLines.keys():
					if len(self.dsLines[network[0]][0]) == 0:
						self.joiningOutlet.append(self.dsLines[network[0]][3])
						self.branchDnsConnectionPipe.append('OUTLET')
						self.processed_nwks.append(network[0])
						dns = False
					else:
						self.processed_nwks.append(network[0])
						area_prev = area
						dsInv_prev = dsInv
						network = self.dsLines[network[0]][0]
				else:
					self.joiningOutlet.append(self.dsLines[network[0]][3])
					self.branchDnsConnectionPipe.append('OUTLET')
					self.processed_nwks.append(network[0])
					dns = False
			elif len(network) > 1:  # consider what happens if there are 2 downstream channels
				# get channels accounting for X connectors
				nwks = []
				for nwk in network:
					if 'connector' in network:
						nwk = self.dsLines[nwk][0][0]
					nwks.append(nwk)
				# get next downstream channels accounting for X connectors
				dns_nwks = []
				for nwk in nwks:
					if nwk in self.dsLines.keys():
						if len(self.dsLines[nwk][0]) == 0:
							dns_nwks.append('DOWNSTREAM NODE')
						else:
							dns_nwk = self.dsLines[nwk][0][0]
							if 'connector' in dns_nwk:
								dns_nwk = self.dsLines[dns_nwk][0][0]
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
					features = []
					for lyr in self.inLyrs:
						for nwk in nwks:
							fld = lyr.fields()[0]
							filter = '"{0}" = \'{1}\''.format(fld.name(), nwk)
							request = QgsFeatureRequest().setFilterExpression(filter)
							for f in lyr.getFeatures(request):
								features.append(f)
					name = []
					typ = []
					no = []
					width = []
					height = []
					usInv = []
					dsInv = []
					area = []
					angle = []
					length = []
					for nwk in nwks:
						for f in features:
							id = f.attributes()[0]
							if nwk == id:
								self.first_sel = False
								self.branchExists = True
								if network[0] in self.processed_nwks:
									self.branchDnsConnectionPipe.append(network)
									self.joiningOutlet.append('JOINING EXISTING BRANCH')
									dns = False
									break
								typ = features[0].attributes()[1]
								length = features[0].attributes()[4]
								if l <= 0:
									l = getLength(features[0])
								na = id
								n = features[0].attributes()[15]
								w = features[0].attributes()[13]
								h = features[0].attributes()[14]
								uI = self.dsLines[nwk][1][0]
								dI = self.dsLines[nwk[0]][1][1]
								if nwk in self.dsLines.keys():
									if len(self.dsLines[nwk][2]) > 0:
										ang = min(self.dsLines[nwk][2])
								else:
									ang = 0
								if t.lower() == 'r':
									a = float(no) * width * height
								elif typ.lower() == 'c':
									a = float(n) * (w / 2) ** 2 * 3.14
								else:
									a = 0
								if (dI > uI and uI != -99999.00) or (uI > dsInv_prev and dsInv_prev != -99999.00):
									adG = True
								if a < area_prev and a != 0:
									decFA = True
								if ang < self.angleLimit and ang != 0:
									sA = True
								name.append(na)
								typ.append(t)
								no.append(n)
								width.append(w)
								height.append(h)
								usInv.append(uI)
								dsInv.append(dI)
								area.append(a)
								angle.append(ang)
								length.append(l)
					self.bType.append(typ)
					self.bLength.append(length)
					self.bName.append(name)
					self.bNo.append(no)
					self.bWidth.append(width)
					self.bHeight.append(height)
					self.bUsInvert.append(usInv)
					self.bDsInvert.append(dsInv)
					self.bAngle.append(angle)
					self.bArea.append(area)
					self.bAdverseGradient.append(adverseGradient)
					self.bDecreaseFlowArea.append(decreaseFlowArea)
					self.bSharpAngle.append(sharpAngle)
					if nwks[0] in self.dsLines.keys():
						if len(self.dsLines[nwks][0]) == 0:
							self.joiningOutlet.append(self.dsLines[nwks[0]][3])
							self.branchDnsConnectionPipe.append([])
							for nwk in nwks:
								self.processed_nwks.append(nwk)
							dns = False
						else:
							for nwk in nwks:
								self.processed_nwks.append(nwk)
							area_prev = sum(area)
							dsInv_prev = min(dsInv)
							network = self.dsLines[nwks[0]][0]
					else:
						self.joiningOutlet.append(self.dsLines[nwks[0]][3])
						self.branchDnsConnectionPipe.append([])
						for nwk in nwks:
							self.processed_nwks.append(nwk)
						dns = False
				elif len(branches) > 1:
					if not self.first_sel:
						self.joiningOutlet.append('BRANCHED')
						self.branchDnsConnectionPipe.append(nwks)
					for nwk in nwks:
						if nwk in self.processed_nwks:
							nwks.remove(nwk)
					for nwk in nwks:
						self.network.append(nwk)
					dns = False
	
	def getBranches(self):
		"""
		Gets the downstream connectivity using a list of starting line names
		
		:return: void
		"""

		self.getDownstreamConnectivity(self.startLines)
		if self.branchExists:
			self.branchName.append('Branch {0}'.format(self.branchCounter))
			self.branchCounter += 1
			self.type.append(self.bType)
			self.length.append(self.bLength)
			self.name.append(self.bName)
			self.no.append(self.bNo)
			self.width.append(self.bWidth)
			self.height.append(self.bHeight)
			self.usInvert.append(self.bUsInvert)
			self.dsInvert.append(self.bDsInvert)
			self.angle.append(self.bAngle)
			self.area.append(self.bArea)
			self.adverseGradient.append(self.bAdverseGradient)
			self.decreaseFlowArea.append(self.bDecreaseFlowArea)
			self.sharpAngle.append(self.bSharpAngle)
		while len(self.network) > 0:
			nwk = self.network[0]
			self.branchExists = False
			self.getDownstreamConnectivity(nwk)
			if self.branchExists:
				self.branchName.append('Branch {0}'.format(self.branchCounter))
				self.branchCounter += 1
				self.type.append(self.bType)
				self.length.append(self.bLength)
				self.name.append(self.bName)
				self.no.append(self.bNo)
				self.width.append(self.bWidth)
				self.height.append(self.bHeight)
				self.usInvert.append(self.bUsInvert)
				self.dsInvert.append(self.bDsInvert)
				self.angle.append(self.bAngle)
				self.area.append(self.bArea)
				self.adverseGradient.append(self.bAdverseGradient)
				self.decreaseFlowArea.append(self.bDecreaseFlowArea)
				self.sharpAngle.append(self.bSharpAngle)
			self.network.remove(nwk)
			
	def reportLog(self):
		"""
		log branch results
		
		:return:
		"""

		for i, branch in enumerate(self.branchName):
			self.log += '\n# {0}\n\n'.format(branch)
			for j, name in enumerate(self.name[i]):
				advG = ''
				decA = ''
				sharpA = ''
				if self.adverseGradient[i][j]:
					advG = ' -- Adverse Gradient'
				if self.decreaseFlowArea[i][j]:
					decA = ' -- Decrease in Area'
				if self.sharpAngle[i][j]:
					sharpA = ' -- Sharp Outflow Angle'
				self.log += '{0}{1}{2}{3}\n'.format(name, advG, decA, sharpA)
				
	def getBranchConnectivity(self):
		"""
		Populates the upstream and downstream branch attribute type for each branch
		
		:return:
		"""
		
		for i, branch in enumerate(self.branchName):
			if self.branchDnsConnectionPipe[i] == 'OUTLET':
				self.dnsBranches.append([None])
			else:
				branches = []
				for branchDnsConnection in self.branchDnsConnectionPipe[i]:
					for j, name in enumerate(self.name):
						if branchDnsConnection in name:
							branches.append(self.branchName[j])
				self.dnsBranches.append(branches)
			ups = True
			branches = []
			for j, branchDnsConnection in enumerate(self.branchDnsConnectionPipe):
				if self.name[i][0] in branchDnsConnection:
					branches.append(self.branchName[j])
					ups = False
			if ups:
				self.upsBranches.append([None])
			else:
				self.upsBranches.append(branches)
				
	def getAllPathsByBranch(self):
		"""
		Gets all the path combinations by branch
		
		:return:
		"""

		upsBranches = []  # get a list of the most upstream branches
		for i, branch in enumerate(self.branchName):
			if self.upsBranches[i] == [None]:
				upsBranches.append(branch)
		
		pathCounter = 0
		todos = upsBranches  # todos are paths to be considered
		todosPath = [None] * len(upsBranches)  # todosPaths are the path numbers where todos came from
		todosSplit = [None] * len(upsBranches)  # todosSplits are where on the path the split occurred
		while todos:
			counter = 0
			dns = False
			todo = todos[0]
			todoPath = todosPath[0]
			todoSplit = todosSplit[0]
			if todoPath is None:
				path = []
			else:
				path = self.paths[todoPath][:todoSplit+1]
			while not dns:
				index = self.branchName.index(todo)
				next = self.dnsBranches[index]
				if len(next) > 1:
					todos += next[1:]
					todosPath.append(pathCounter)
					todosSplit.append(counter)
				next = next[0]
				if next is None:
					dns = True
				path.append(todo)
				todo = next
				counter += 1
			pathCounter += 1
			self.paths.append(path)
			todos = todos[1:]
			todosPath = todosPath[1:]
			todosSplit = todosSplit[1:]
			
	def getAllPathsByNwk(self):
		"""
		Get all paths listed by nwk name
		
		:return:
		"""

		for path in self.paths:
			pathsNwks = []
			pathsLen = []
			for i, branch in enumerate(path):
				if i + 1 < len(path):
					dnsB = path[i+1]
				else:
					dnsB = None
				connNwk = False  # Connection pipe - the pipe that the branch connects to in the downstream branch
				if i == 0:
					connNwkName = None
					connNwk = True  # most upstream and therefore no connection pipe
				bInd = self.branchName.index(branch)  # Branch index
				for j, nwk in enumerate(self.name[bInd]):
					if nwk == connNwkName:
						connNwk = True
					if connNwk:
						pathsNwks.append(nwk)
						pathsLen.append(self.length[bInd][j])
					if j + 1 == len(self.name[bInd]):
						connNwkNames = self.branchDnsConnectionPipe[bInd]
						if dnsB is not None:
							bdInd = self.branchName.index(dnsB)
						if connNwkNames is not 'OUTLET':
							for c in connNwkNames:
								if c in self.name[bdInd]:
									connNwkName = c
									break
			self.pathsNwks.append(pathsNwks)
			self.pathsLen.append(sum(pathsLen))
	
	def addX(self, ind, start):
		"""
		Create X values path for plotting.

		:param ind: path index
		:param start: start value for the path
		:return: populates x plotting values
		"""
		
		x = [start]
		length = start
		path = self.pathsNwks[ind]
		
		for i, nwk in enumerate(path):
			found = False
			for j, name in enumerate(self.name):
				for k, nwk2 in enumerate(name):
					if nwk == nwk2:
						found = True
						break
				if found:
					break
			length += self.length[j][k]
			if i + 1 == len(path):
				x.append(length)
			else:
				x.append(length)
				x.append(length)
		self.pathsX.insert(ind, x)
		
	def addInv(self, ind):
		"""
		Create Y values for the nwk inverts
		
		:param ind: path index
		:return: populates y invert plotting values
		"""
		
		invert = []
		path = self.pathsNwks[ind]
		for i, nwk in enumerate(path):
			found = False
			for j, name in enumerate(self.name):
				for k, nwk2 in enumerate(name):
					if nwk == nwk2:
						found = True
						break
				if found:
					break
			if self.usInvert[j][k] == -99999:
				invert.append(np.nan)
			else:
				invert.append(self.usInvert[j][k])
			if self.dsInvert[j][k] == -99999:
				invert.append(np.nan)
			else:
				invert.append(self.dsInvert[j][k])
		self.pathsInvert.insert(ind, invert)
	
	def addGround(self, ind):
		"""
		Create Y values for the ground levels

		:param ind: path index
		:return: populates y ground plotting values
		"""
		
		ground = []
		path = self.pathsNwks[ind]
		for i, nwk in enumerate(path):
			found = False
			for j, name in enumerate(self.name):
				for k, nwk2 in enumerate(name):
					if nwk == nwk2:
						found = True
						break
				if found:
					break
			ground.append(self.ground[j][k])
			ground.append(self.ground[j][k])
		self.pathsGround.insert(ind, ground)
		
	def addPipes(self, ind, xInd):
		"""
		Create patch object for pipes for plotting
		
		:param ind: path index
		:param xInd: index of X values
		:return: populates pipe plotting values
		"""

		pipes = []
		path = self.pathsNwks[ind]
		for i, nwk in enumerate(path):
			pipe = False
			found = False
			for j, name in enumerate(self.name):
				for k, nwk2 in enumerate(name):
					if nwk == nwk2:
						found = True
						break
				if found:
					break
			if self.type[j][k].lower() == 'c':
				y = self.width[j][k]
				pipe = True
			elif self.type[j][k].lower() == 'r':
				y = self.height[j][k]
				pipe = True
			if self.pathsInvert[xInd][i*2] == -99999 or self.pathsInvert[xInd][i*2+1] == -99999:
				pipe = False
			if pipe:
				xStart = self.pathsX[xInd][i*2]
				xEnd = self.pathsX[xInd][i*2+1]
				yStartInv = self.pathsInvert[xInd][i*2]
				yStartObv = yStartInv + y
				yEndInv = self.pathsInvert[xInd][i*2+1]
				yEndObv = yEndInv + y
				xPatch = [xStart, xEnd, xEnd, xStart]
				yPatch = [yStartInv, yEndInv, yEndObv, yStartObv]
				pipes.append(zip(xPatch, yPatch))
		self.pathsPipe.append(pipes)
		
	def getPlotFormat(self):
		"""
		Arrays data into plottable format
		
		:return:
		"""

		self.getBranchConnectivity()
		self.getAllPathsByBranch()
		self.getAllPathsByNwk()
		
		maxPathLen = max(self.pathsLen)
		maxPLInd = self.pathsLen.index(maxPathLen)
		
		self.addX(maxPLInd, 0)
		self.addInv(maxPLInd)
		if len(self.ground) > 0:
			self.addGround(maxPLInd)
		self.addPipes(maxPLInd, 0)

		
		
		
		
		
								
		
		