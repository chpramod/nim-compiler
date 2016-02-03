class regmemDescriptor():
    def __init__(self,registers,variables):
        self.registerList = dict() # stores content of registers i.e. variables
        self.variableList = dict() # stores memory content i.e. registers, memory location, etc
        self.resetRegisters()
        self.freeReg = registers
        self.busyReg = []
        # for reg in registers:
        #     self.table[reg]=None
        for variable in variables:
            self.variablelist[variable] = {
							#'memory'	: None,
							'register'	: None,
                            }

    def getRegVal(self,reg):
        return self.register[reg]

    def setRegVar(self,reg,value):
        self.register[reg]=value
        self.variable[value]=reg

    def getRegister(self, temp):
		if temp in self.registerList.values():	#if variable is already in a register
			register = self.variableList(temp)
		else:
			if len(self.freeReg) == 0:			#if we need to spill a register
				register = self.busyReg.pop(0)
				tempReg = self.registerList[register]
				self.variablelist[tempReg]['register'] = None
				self.registerList[register] = temp
				print '\t'+'mov', tempReg, register     #followed the mov,dest,src convention
				print '\t'+'mov', register, temp
			else:									#if we have a free register
				register = self.freeReg.pop()
				print '\t'+'mov', register, temp  

			self.variablelist[temp]['register'] = register
			self.busyReg.append(register)
			self.registerList[register] = temp

		return register

    def setReg(self,reg,value):
        self.register[reg] = value

    # def getLoc(self,var):
    #     return self.variable[var]

    def setLoc(self,var,value):
        self.variable[var] = value

    def setMem(self,location,value):
        self.variable[location]=value

    def emptyReg(self):
        for i in self.register:
            if(self.register[i]==None): return i
        return None

    def resetRegisters(self):
		self.registerList = {
			'$eax' : None, '$ebx' : None, '$ecx' : None, '$edx' : None, '$esi' : None, '$edi' : None}
        self.freeReg = []
		for register in self.registerList.keys():
			self.freeRegisters.append(register)
		self.busyReg = []
