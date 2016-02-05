class regmemDescriptor():
    def __init__(self,registers,variables,fp):
        self.registerList = {} # stores content of registers i.e. variables
        self.variableList = {} # stores memory content i.e. registers, memory location, etc
        self.resetRegisters()
        #self.freeRegisters =[]
        #self.busyRegisters=[]
        self.fp = fp
        self.ST=None
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
        self.ST.printTable()
        #print self.registerList.values()
        if temp in self.registerList.values():
            register = self.variableList[temp]['register']
            #print register
        else:
            if len(self.freeRegisters) != 0:
                register = self.freeRegisters.pop()
                self.fp.write("\tMOVL $(%s), %s\n" %(temp[1:],register))
                # if self.variablelist[temp]['memory'] != None and self.variablelist[temp]['store']:
                    # (level, offset) = self.variablelist[temp]['memory']
                    # print (level, offset)
                    # self.putAbsoluteAddressInRegister(level, offset)
                    # self.addLineToCode(['lw', register, '0($s7)', ''])

            else:
                register = None
                maxx=0
                for var in self.ST:
                    if self.variableList[var]['register']!=None:
                        if self.ST[var]['nextuse'] > maxx:
                            register = self.variableList[var]['register']
                        maxx=max(self.ST[var]['nextuse'],maxx)
            	# register = self.busyRegisters.pop(0)
            	tempReg = self.registerList[register]
                self.fp.write("\tMOVL %s, $(%s)\n" %(register,tempReg[1:]))
            	self.variableList[tempReg]['register'] = None
            	self.registerList[register] = temp
                self.fp.write("\tMOVL $(%s), %s\n" %(temp[1:],register))

            	# if self.variableList[tempReg]['memory'] != None:
                    # (level, offset) = self.variablelist[tempReg]['memory']
                    # self.putAbsoluteAddressInRegister(level, offset)
                    # self.addLineToCode(['sw', register, '0($s7)', ''])
                    # self.variableList[tempReg]['store'] = True

            	# if self.variablelist[temp]['memory'] != None:
                    # (level, offset) = self.variablelist[temp]['memory']
                    # self.putAbsoluteAddressInRegister(level, offset)
                    # self.addLineToCode(['lw', register, '0($s7)', ''])
            self.variableList[temp]['register'] = register
            # self.busyRegisters.append(register)
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
        self.registerList = {'%eax' : None, '%ebx' : None, '%ecx' : None, '%edx' : None, '%esi' : None, '%edi' : None}
        self.freeRegisters=[]
        for register in self.registerList.keys():
			self.freeRegisters.append(register)
        self.busyRegisters= []

    def freeRegister(self,reg):
        if reg in busyRegisters:
            self.busyRegisters.remove(self)
            self.freeRegisters.append(self)
        self.fp.write("\tMOVL %s, %s\n" %(self.registerList[reg],reg))
        self.variableList[self.registerList[reg]]=None
        self.registerList[reg]=None

    def setST(self,ST):
        self.ST = ST
