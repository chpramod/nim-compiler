import pprint

class symbolTable():
    def __init__(self,variables,TACline,nextTable):
        self.lineno = int(TACline[0])
        self.table={}
        if(nextTable!=None):
            for variable in variables:
                self.table[variable]=dict()
            for variable in variables: # Since source variables are used not destination variables
                if ((TACline[1] not in ['>>','<<']) and (variable in [TACline[index] for index in range(3,len(TACline))]) or (TACline[1] in ['>>','<<']) and (variable in [TACline[index] for index in range(2,len(TACline))])):
                    self.table[variable]['curruse'] = 1 # Use of variable in current line of code
                else:
                    self.table[variable]['curruse'] = 0
                self.table[variable]['nextuse'] = nextTable.table[variable]['nextuse'] if nextTable.table[variable]['curruse'] == 0 else nextTable.lineno
            # Not sure about this part
            # if(self.table[variable][nextuse] < TACline[0]):
            #     self.table[variable][status] = 0 # 0 = Dead, 1 = Live
            # else:
            #     self.table[variable][status] = 1 # 0 = Dead, 1 = Live
        else:
            for variable in variables:
                self.table[variable]=dict()
            for variable in variables: # Since source variables are used not destination variables
                if ((TACline[1] not in ['>>','<<']) and (variable in [TACline[index] for index in range(3,len(TACline))]) or (TACline[1] in ['>>','<<']) and (variable in [TACline[index] for index in range(2,len(TACline))])):
                    self.table[variable]['curruse'] = 1 # Use of variable in current line of code
                else:
                    self.table[variable]['curruse'] = 0
                self.table[variable]['nextuse'] = -1
        # print(self.lineno)
        # pprint.pprint(self.table)
    def printTable(self):
        print self.lineno
        pprint.pprint(self.table)
