class regmemDescriptor():
    def __init__(self,registers,variables):
        self.register = dict() # stores content of registers i.e. variables
        self.variable = dict() # stores memory content i.e. registers, memory location, etc

        for reg in self.register:
            self.table[reg]=None
        for location in self.variable:
            self.variable[location]=None

    def getRegVal(self,reg):
        return self.register[reg]

    def setRegVar(self,reg,value):
        self.register[reg]=value
        self.variable[value]=reg

    def getReg(self,location):
        return self.variable[location]

    def setReg(self,reg,value):
        return self.register[location] = value

    def getLoc(self,var):
        return self.variable[var]

    def setLoc(self,var,value):
        self.variable[var] = value

    def setMem(self,location,value):
        self.variable[location]=value

    def emptyReg(self):
        for i in self.register:
            if(self.register[i]==None) return i
        return None
