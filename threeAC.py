class regmemDescriptor():
    def __init__(self,registers,variables):
        self.registerList = dict() # stores content of registers i.e. variables
        self.variableList = dict() # stores memory content i.e. registers, memory location, etc
        self.resetRegisters()

        # for reg in registers:
        #     self.table[reg]=None
        for variable in variables:
            self.variablelist[variable] = {
							'memory'	: None,
							'register'	: None,
                            }

    def getRegVal(self,reg):
        return self.register[reg]

    def setRegVar(self,reg,value):
        self.register[reg]=value
        self.variable[value]=reg

    def getRegister(self, temp):
		if temp in self.registerList.values():
			register = self.variableList(temp)
		else:
			if len(self.freeReg) == 0:
				register = self.busyReg.pop(0)
				tempReg = self.registerList[register]
				self.variablelist[tempReg]['register'] = None
				self.registerList[register] = temp

				if self.variableList[tempReg]['memory'] != None:
					(level, offset) = self.ST.addressDescriptor[tempReg]['memory']
					self.putAbsoluteAddressInRegister(level, offset)
					self.addLineToCode(['sw', register, '0($s7)', ''])
					self.ST.addressDescriptor[tempReg]['store'] = True

				if self.ST.addressDescriptor[temp]['memory'] != None:
					(level, offset) = self.ST.addressDescriptor[temp]['memory']
					self.putAbsoluteAddressInRegister(level, offset)
					self.addLineToCode(['lw', register, '0($s7)', ''])
			else:
				register = self.freeRegisters.pop()
				if self.ST.addressDescriptor[temp]['memory'] != None and self.ST.addressDescriptor[temp]['store']:
					(level, offset) = self.ST.addressDescriptor[temp]['memory']
					# print (level, offset)
					self.putAbsoluteAddressInRegister(level, offset)
					self.addLineToCode(['lw', register, '0($s7)', ''])

			self.ST.addressDescriptor[temp]['register'] = register
			self.busyRegisters.append(register)
			self.registerDescriptor[register] = temp

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
