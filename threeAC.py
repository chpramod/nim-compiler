class ThreeAC:
	def __init__(self):
		self.code = []
		self.labelCount = -1
		self.labelPrefix = 'l'
		self.tempCount = -1
		self.tempPrefix = '$t'

	def emit(self,op,dest,src1,src2):
		self.code.append([op,dest,src1,src2])

	def emitif(self,ifgoto,op,src1,src2,destlabel):
		self.code.append([ifgoto,op,src1,src2,destlabel])

	def newLabel(self):
		self.labelCount += 1
		return self.labelPrefix+str(self.labelCount)

	def printCode(self):
		f1 = open("testinput.txt","w")
		for line in self.code:
			# print line
			# print "len (line)", len(line)
			# print "line[1]", line[1]

			emitString = ""
			for i in range(len(line)) :
				if line[i] != "" :
					if i == 0 :
						emitString = emitString  + str(line[i])
					else :
						emitString = emitString + ", " + str(line[i])

			print emitString
			f1.write(emitString + '\n')



		f1.close

			# if len(line) == 4 :
			# 	print line[0]+ ", " + line[1] + ", " + line[2] + ", " +line[3]
			# elif len(line) == 5 :
			# 	print line[0] + ", " + line[1]+ ", " +line[2]+ ", " +line[3]+ ", " +line[4]



	def createTemp(self):
		self.tempCount += 1
		return self.tempPrefix+str(self.tempCount)
