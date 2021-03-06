class St:
  #initialise
    def __init__(self):
        self.St={
        'global':{
            'name':'global',
            #currently only considered for blocks
            #'type'='block'
            'parent':None,
            'identifiers':{}
        }
        }
        self.curScope='global'
        self.curBlockNo=0

    def addBlock(self):
        nameBlock=self.getNewBlockName()
        self.St[nameBlock]={
            'name':'nameBlock',
            'parent':self.curScope,
            'identifiers':{}
        }
        self.curScope=nameBlock

    def endBlock(self):
        self.curScope=self.St[self.curScope]['parent']

    def getNewBlockName(self):
        self.curBlockNo+=1
        return 'b'+str(self.curBlockNo)

    def getCurrentScope(self):
        return self.curScope

    def addIdenInScope(self, scope,idenName, place, idenType,idenhasVal):
        self.St[scope]['identifiers'][idenName]={
            'place':place,
            'type':idenType,
            'hasVal': idenhasVal
        }

    def addIden(self, idenName, place, idenType,idenhasVal,size):
        self.St[self.curScope]['identifiers'][idenName]={
            'place':place,
            'type':idenType,
            'hasVal': idenhasVal,
            'size':size
        }

    def getIden(self, idenName):
        idenScope = self.getIdenScope(idenName)
        if idenScope!=None:
            #returns all attributes of identifier
            return self.St[idenScope]['identifiers'][idenName].get(idenName)

        else:
            return None

    def getIdenScope(self, idenName):
        scope=self.curScope
        while scope!=None:
            if idenName in self.St[scope]['identifiers']:
                return scope
            scope=self.St[scope]['parent']

        return None

    def getIdenAttr(self, idenName, attrName):
        idenScope = self.getIdenScope(idenName)
        if idenScope!=None:
            return self.St[idenScope]['identifiers'][idenName].get(attrName)
        else:
            print "attribute not set"
            return None

    def setidenAttr(self, idenName, attrName, attrVal):
        idenScope = self.getIdenScope(idenName)
        if idenScope!=None:
            self.St[idenScope]['identifiers'][idenName][attrName]=attrVal
