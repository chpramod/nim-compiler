class threeAC:
	def __init__(self):
		self.code = []
		self.labelCount = -1
		self.labelPrefix = 'l'
		self.tempCount = -1
		self.tempPrefix = 't'
	def emit(self,op,dest,src1,src2):
		self.code.append([op,dest,src1,src2])

	def createLabel(self):
		self.labelCount += 1
		return self.labelPrefix+str(self.labelCount)
	def printCode(self):
		for line in self.code:
			print line
	def createTemp(self):
		self.tempCount += 1
		return self.tempPrefix+str(self.tempCount)