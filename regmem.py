from pprint import pprint
nonDirtyOp = ['print','push']
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
                            'dirty'     : False
                            }


# returns a register for variable temp
    def getRegister(self, temp):
        # pprint(self.registerList)
        # self.ST.printTable()
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
                if self.ST.table[temp]['curruse']==1:
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
                if self.variableList[tempReg]['dirty']==True:
                    self.fp.write("\tMOVL %s, %s\n" %(register,tempReg[1:]))
                self.variableList[tempReg]['dirty']=False
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
        # print self.ST.lineno,self.currLine,temp,register
        return register



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

# free any register currently associated with a variable which has no next use
    def freeRegister(self):
        # pprint (self.variableList)
        if self.ST.dest in self.variableList.keys() and self.ST.op not in nonDirtyOp:
            if self.variableList[self.ST.dest]['register']!=None:
                self.variableList[self.ST.dest]['dirty']=True
        # pprint(self.variableList)
        for var in self.variableList:
            # print self.freeRegisters
            if self.variableList[var]['register']!=None:
                if self.ST.table[var]['nextuse']==-1 and self.ST.table[var]['nextassign']==-1 and self.variableList[var]['register'] not in self.freeRegisters:
                    self.freeReg(self.variableList[var]['register'])
        # pprint(self.variableList)

#free all reg's and also reset both variablelist and registerList
    def freeAll(self,flag=False):
        for reg in self.registerList:
            self.freeReg(reg,flag)


# remove reg from associated variable's variableList and also make current register's variable to none
# if flag is set TRUE also makes register's value =0
    def freeReg(self,reg,flag=False):
        # print "inside freeReg", reg
        if reg not in self.freeRegisters:
            # print "inside freereg if1"
            self.freeRegisters.append(reg)
            # print "variablelist", self.variableList
            for var in self.variableList:
                if self.variableList[var]['register']==reg:
                    self.variableList[var]['register']=None
                    if self.variableList[var]['dirty']==True:
                        self.fp.write("\tMOVL %s, %s\n" %(reg,var[1:]))
                    self.variableList[var]['dirty']=False
                    break
        if flag==True:
            self.fp.write("\tXORL %s, %s\n" %(reg,reg))
        self.registerList[reg]=None


# assigns reg to var and stores current value of var in reg
    def setReg(self,var,reg):
        # print "inside setReg", var, reg
        # print self.variableList
        self.freeReg(reg)
        self.freeRegisters.remove(reg)
        if self.variableList[var]['register']!=None:
            # print "inside if",self.variableList[var]['register']
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
    def pushToMem(self,var):
        if var in self.variableList.keys():
            if self.variableList[var]['dirty']==True:
                self.fp.write("\tMOVL %s, %s\n" %(self.variableList[var]['register'],var[1:]))
                self.variableList[var]['dirty']==False

    def setST(self,ST):
        self.ST = ST
