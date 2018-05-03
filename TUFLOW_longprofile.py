# coding=utf-8

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
		
		for item in pipes:
			self.pipes.append(item)
		
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
