class St:
  #initialise
    def __init__(self):
        self.St={
        'global':{
            'name':'global',
            #currently only considered for blocks
            #'type'='block'
            'parent':'none',
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
        self,curScope=nameBlock

    def endBlock(self):
        self.curScope=self.St[self.curScope]['parent']

    def getNewBlockName(self):
        self.curBlockNo+=1
        return 'b'+str(self.curBlockNo)
