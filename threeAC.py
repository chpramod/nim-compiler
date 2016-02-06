from pprint import pprint
class regmemDescriptor():
    def __init__(self,registers,variables,fp):
        self.registerList = {} # stores content of registers i.e. variables
        self.variableList = {} # stores memory content i.e. registers, memory location, etc
        self.resetRegisters()
        self.currLine=[]
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
        # pprint(self.registerList)
        #self.ST.printTable()
        #print self.registerList.values()
        if temp in self.registerList.values():
            register = self.variableList[temp]['register']
            #print register
        else:
            if len(self.freeRegisters) != 0:
                #print self.ST.table
                #print self.ST
                register = self.freeRegisters.pop()
                # if self.variableList[temp]['register']!=None:
                self.fp.write("\tMOVL %s, %s\n" %(temp[1:],register))
                # if self.variablelist[temp]['memory'] != None and self.variablelist[temp]['store']:
                    # (level, offset) = self.variablelist[temp]['memory']
                    # print (level, offset)
                    # self.putAbsoluteAddressInRegister(level, offset)
                    # self.addLineToCode(['lw', register, '0($s7)', ''])

            else:
                register = None
                maxx=-2
                #print temp,self.variableList,self.freeRegisters
                #self.ST.printTable()
                for var in self.ST.table:
                    # print self.ST.lineno,var
                    # if self.variableList[var]['register']!=None and var in self.currLine:
                    #     print "HII\t"+self.ST.lineno+var
                    if self.variableList[var]['register']!=None and var not in self.currLine:
                    # if self.variableList[var]['register']!=None:
                        if self.ST.table[var]['nextuse'] > maxx:
                            #print "#############" ,var, self.ST.table[var]['nextuse'], maxx
                            register = self.variableList[var]['register']
                            maxx=max(self.ST.table[var]['nextuse'],maxx)
                # register = self.busyRegisters.pop(0)
                tempReg = self.registerList[register]
                self.fp.write("\tMOVL %s, %s\n" %(register,tempReg[1:]))
                self.variableList[tempReg]['register'] = None
                self.registerList[register] = temp
                self.fp.write("\tMOVL %s, %s\n" %(temp[1:],register))

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
        print self.ST.lineno,self.currLine,temp,register
        return register

    # def setReg(self,reg,value):
    #     self.register[reg] = value

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
        self.freeRegisters = self.registerList.keys()
        self.busyRegisters= []

    # def freeRegister(self,reg):
    #     if reg in busyRegisters:
    #         self.busyRegisters.remove(self)
    #         self.freeRegisters.append(self)
    #     self.fp.write("\tMOVL %s, %s\n" %(self.registerList[reg],reg))
    #     self.variableList[self.registerList[reg]]=None
    #     self.registerList[reg]=None

    def freeRegister(self):
        for var in self.variableList:
            if self.variableList[var]['register']!=None:
                if self.ST.table[var]['nextuse']==-1 and self.variableList[var]['register'] not in self.freeRegisters:
                    self.freeReg(self.variableList[var]['register'])

    def freeAll(self,flag=False):
        for reg in self.registerList:
            self.freeReg(reg,flag)

    def freeReg(self,reg,flag=False):
        if reg not in self.freeRegisters:
            self.freeRegisters.append(reg)
            for var in self.variableList:
                if self.variableList[var]['register']==reg:
                    self.variableList[var]['register']=None
                    self.fp.write("\tMOVL %s, %s\n" %(reg,var[1:]))
                    break
        if flag==True:
            self.fp.write("\tXORL %s, %s\n" %(reg,reg))
        self.registerList[reg]=None

    def setReg(self,var,reg):
        self.freeReg(reg)
        self.freeRegisters.remove(reg)
        if self.variableList[var]['register']!=None:
            self.freeReg(self.variableList[var]['register'])
        self.variableList[var]['register']=reg
        self.fp.write("\tMOVL %s, %s\n" %(var[1:],reg))
        self.registerList[reg]=var

    def setVarReg(self,reg,var):
        if self.variableList[var]['register']!=None:
            self.registerList[self.variableList[var]['register']] = None
            self.freeRegisters.append(self.variableList[var]['register'])
        self.variableList[var]['register']=reg
        if reg in self.freeRegisters:
            self.freeRegisters.remove(reg)
        self.registerList[reg]=var

    def protectRegs(self,line):
        self.currLine=[]
        for i in line:
            if i in self.variableList.keys():
                self.currLine.append(i)

    def setST(self,ST):
        self.ST = ST
