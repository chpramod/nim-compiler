import pprint
twoAddrCodes = ['incr','decr','print','>>','<<']
class symbolTable():
    def __init__(self,variables,TACline,nextTable):
        self.op = TACline[1]
        if(len(TACline)>2):
            self.dest = TACline[2]
        else:
            self.dest = None
        self.lineno = int(TACline[0])
        self.table={}
        self.prevTable=None
        if(nextTable!=None):
            nextTable.prevTable=self
            for variable in variables:
                self.table[variable]=dict()
            for variable in variables: # Since source variables are used not destination variables
                if ((TACline[1] not in twoAddrCodes) and (variable in [TACline[index] for index in range(3,len(TACline))]) or (TACline[1] in twoAddrCodes) and (variable in [TACline[index] for index in range(2,len(TACline))])):
                    self.table[variable]['curruse'] = 1 # Use of variable in current line of code
                else:
                    self.table[variable]['curruse'] = 0
                self.table[variable]['nextuse'] = nextTable.table[variable]['nextuse'] if nextTable.table[variable]['curruse'] == 0 else nextTable.lineno
                self.table[variable]['nextassign'] = nextTable.lineno if nextTable.dest == variable and nextTable.table[variable]['curruse'] == 0 else nextTable.table[variable]['nextassign']
            if nextTable.op=='=':
                self.table[nextTable.dest]['nextuse'] = -1
            # Not sure about this part
            # if(self.table[variable][nextuse] < TACline[0]):
            #     self.table[variable][status] = 0 # 0 = Dead, 1 = Live
            # else:
            #     self.table[variable][status] = 1 # 0 = Dead, 1 = Live
        else:
            for variable in variables:
                self.table[variable]=dict()
            for variable in variables: # Since source variables are used not destination variables
                if ((TACline[1] not in twoAddrCodes) and (variable in [TACline[index] for index in range(3,len(TACline))]) or (TACline[1] in twoAddrCodes) and (variable in [TACline[index] for index in range(2,len(TACline))])):
                    self.table[variable]['curruse'] = 1 # Use of variable in current line of code
                else:
                    self.table[variable]['curruse'] = 0
                self.table[variable]['nextuse'] = -1
                self.table[variable]['nextassign'] = -1
        # print(self.lineno)
        # pprint.pprint(self.table)
    def printTable(self):
        print self.lineno
        pprint.pprint(self.table)
