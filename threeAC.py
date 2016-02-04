class regmemDescriptor():
    def __init__(self,registers,variables):
        self.registerList = dict() # stores content of registers i.e. variables
        self.variableList = dict() # stores memory content i.e. registers, memory location, etc
        self.resetRegisters()
        self.freeRegisters =[]
        self.busyRegisters=[]

        # for reg in registers:
        #     self.table[reg]=None
        for variable in variables:
            self.variableList[variable] = {
							'memory'	: None,
							'register'	: None,
                            'store'     : None
                            }

    def getRegVal(self,reg):
        return self.register[reg]

    def setRegVar(self,reg,value):
        self.register[reg]=value
        self.variable[value]=reg

    def getRegister(self, temp):
        if temp in self.registerList.values():
            register = self.variableList[temp]
        else:
            if len(self.freeRegisters) != 0:
                register = self.freeRegisters.pop()
                # if self.variablelist[temp]['memory'] != None and self.variablelist[temp]['store']:
                    # (level, offset) = self.variablelist[temp]['memory']
                    # print (level, offset)
                    # self.putAbsoluteAddressInRegister(level, offset)
                    # self.addLineToCode(['lw', register, '0($s7)', ''])

            else:
            	register = self.busyRegisters.pop(0)
            	tempReg = self.registerList[register]
            	self.variablelist[tempReg]['register'] = None
            	self.registerList[register] = temp

            	if self.variableList[tempReg]['memory'] != None:
                    # (level, offset) = self.variablelist[tempReg]['memory']
                    # self.putAbsoluteAddressInRegister(level, offset)
                    # self.addLineToCode(['sw', register, '0($s7)', ''])
                    self.variablelist[tempReg]['store'] = True

            	# if self.variablelist[temp]['memory'] != None:
                    # (level, offset) = self.variablelist[temp]['memory']
                    # self.putAbsoluteAddressInRegister(level, offset)
                    # self.addLineToCode(['lw', register, '0($s7)', ''])

        	self.variablelist[temp]['register'] = register
        	self.busyRegisters.append(register)
        	self.registerList[register] = temp
        self.busyRegisters.append(register)
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
        self.registerList = {'$eax' : None, '$ebx' : None, '$ecx' : None, '$edx' : None, '$esi' : None, '$edi' : None}
        self.freeRegisters=[]
        for register in self.registerList.keys():
			self.freeRegisters.append(register)
        self.busyRegisters= []
