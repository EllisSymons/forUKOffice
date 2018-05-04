# coding=utf-8
import sys
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
		#pydevd.settrace('localhost', port=53100, stdoutToServer=True, stderrToServer=True)
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
		self.network = startLines
		self.inLyrs = inLyrs
		self.angleLimit = angleLimit
		self.processed_nwks = []
		self.log = ''
		self.names = []
		self.branch_names = []
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
		self.dnsConnectionPipe = []
		self.adverseGradient = []
		self.decreaseFlowArea = []
		self.sharpAngle = []
		
	def getDownstreamConnectivity(self):
		"""
		Determines the 1D network branch and gets the pipe data for it.
		
		:return: void
		"""
		area_prev = 0
		dsInv_prev = 99999
		x = []
		bed = []
		pipes = []
		adverseGradient = False
		decreaseFlowArea = False
		sharpAngle = False
		bn = []
		# Determine if there are pipes downstream of starting locations
		for network in self.network:
			if len(self.dsLines[network]) > 0:
				dns = True  # there are downstream pipes available
				break
			else:
				dns = False
		while dns:
			# Get QgsFeature layers for start lines
			features = []
			for lyr in self.inLyrs:
				fld = lyr.fields()[0]
				for network in self.network:
					filter = '"{0}" = \'{1}\''.format(fld.name(), network)
					request = QgsFeatureRequest().setFilterExpression(filter)
					for f in lyr.getFeatures(request):
						features.append(f)
			# Get data for starting lines
			if len(self.network) == 1:  # dealing with one channel
				self.branchExists = True
				if self.network[0] in self.processed_nwks:
					self.dnsConnectionPipe.append(self.network[0])
					dns = False
					break
#
				if self.network[0] in self.dsLines.keys():
					if len(self.dsLines[self.network[0]][0]) == 0:
						self.processed_nwks.append(self.network[0])
						dns = False
					else:
						self.processed_nwks.append(self.network[0])
						keyPrev = self.network[0]
						area_prev = area
						dsInv_prev = dsInv
						self.network = self.dsLines[self.network[0]][0]
				else:
					self.processed_nwks.append(self.network[0])
					dns = False
			elif len(self.network) > 1:  # consider what happens if there are 2 downstream channels
				# get channels accounting for X connectors
				nwks = []
				for network in self.networks:
					if 'connector' in network:
						network = self.dsLines[network][0][0]
					nwks.append(network)
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
							name.append(id)
							if nwk == id:
								l = f.attributes()[4]
								if len(x) == 0:
									x.append(0)
								if length > 0:
									x.append(length)
								else:
									x.append(getLength(f))
								t = f.attributes()[1]
								typ.append(t)
								
								
								
								if typ.lower() == 'r':
									nos.append(int(f.attributes()[15]))
									widths.append(float(f.attributes()[13]))
									heights.append(float(f.attributes()[14]))
									usInv = float(dsLines[nwk][1][0])
									dsInv = float(dsLines[nwk][1][1])
									if not params:
										bed.append(usInv)
										bed.append(dsInv)
										pipes.append(f.attributes()[14])
										params = True
									areas.append(
										float(f.attributes()[15]) * float(f.attributes()[13]) * float(
											f.attributes()[14]))
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
									if not params:
										bed.append(usInv)
										bed.append(dsInv)
										pipes.append(f.attributes()[13])
										params = True
									bed.append(usInv)
									bed.append(dsInv)
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
						           listToString(heights), area, listToString(usInvs), listToString(dsInvs), angle,
						           decArea,
						           advSlope, sharpAngle)
					else:
						log += '{0},{1}\n'.format(listToString(nwks), listToString(typs))
					if nwks[0] in dsLines.keys():
						if len(dsLines[nwks[0]][0]) == 0:
							used_nwks.append(keys[0])
							dns = False
						else:
							used_nwks.append(keys[0])
							keyPrev = keys[0]
							area_prev = area
							dsInv_prev = min(dsInvs)
							keys = dsLines[nwks[0]][0]
					else:
						used_nwks.append(keys[0])
						ups_pipe = keys[0]
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
									a += '{0})'.format(br)
							if i == 0:
								log += '{0}'.format(a)
							elif i < len(bn) - 1:
								log += ', {0}'.format(a)
							else:
								log += ', {0}\n'.format(a)
					if nwks[0] in dsLines.keys():
						keys = dsLines[nwks[0]][0]
					dns_pipe = nwks
					dns = False
	
	def getBranches(self):
		"""
		Gets the downstream connectivity using a list of starting line names
		
		:return: void
		"""
		while len(self.startLine) > 0:
			for startLine in self.startLine:
				self.branchExists = False
				self.getDownstreamConnectivity()
				if self.branchExists:
					self.branchNames.append('Branch {0}'.format(self.branchCounter))
					self.branchCounter += 1