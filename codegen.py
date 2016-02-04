#!/usr/bin/python

#this program will convert 3-addr code to x86 assembly code
import sys
import pprint
from symbolTable import *
from threeAC import *

jumpLabels=["goto","ifgoto","call","label","ret"]
reservedLabels = jumpLabels
reservedLabels.append("print")

register_list = ["$eax","$ebx","$ecx","$edx","$esi","$edi"]
variables = []

def generateAssCode(code):
	global register_list,variables
	fp = open("AssCode.s",'w')
	leaders=[]
	TAC = []
	SymbolTable = dict()
	totalLines=0
	with code as f:
		for line in f:
			totalLines+=1
			line=line.rstrip('\n')
			splitLine=line.split(', ')
			TAC.append(splitLine)
			if splitLine[0]=='1':
				leaders.append(int(splitLine[0]))
			elif splitLine[1] in jumpLabels:
				if splitLine[1]=='goto':
					leaders.append(int(splitLine[0])+1)
					leaders.append(int(splitLine[2]))              #for statements like 4, goto, 2
				elif splitLine[1]=='ifgoto':
					leaders.append(int(splitLine[0])+1)
					leaders.append(int(splitLine[5]))              #for statements like 4, ifgoto, leq, a, 50, 2
				elif splitLine[1]=='label':
					leaders.append(int(splitLine[0]))
				elif splitLine[1]=='ret':                          #not sure of we need to do this for the 'ret' oper.
					leaders.append(int(splitLine[0])+1)
				elif splitLine[1]=='call':
					#the following code is flawed, need a solution!
					# with code as f1:
					# 	for lineIter in f1:
					# 		lineIter=lineIter.rstrip('\n')
					# 		splitLineIter=lineIter.split(', ')
					# 		if splitLineIter[1]=='label' and splitLineIter[2]==splitLine[2]:
					# 			leaders.append(int(splitLineIter[0]))
					leaders.append(int(splitLine[0])+1)
	#following lines improve leaders array
	leaders.sort()
	extra=totalLines+1
	if extra in	leaders: 
		leaders.remove(extra)         #removes an entry which is added after reading last line
	if len(leaders) == 0:                #following lines remove duplicates
			return 0

	p = 0
	for i in range(0,len(leaders)):
		if leaders[i] != leaders[p]:
			leaders[i], leaders[p+1] = leaders[p+1], leaders[i]
			p += 1
	p+=1
	p=len(leaders)-p
	del leaders[-p:]
	# pprint.pprint(leaders)
	# for k in range(1,len(leaders)-p):
	# 	print leaders[len(leaders)-k]
	# 	leaders.remove(leaders[len(leaders)-k])
	# pprint.pprint(TAC)
	basicBlocks,variables = BasicBlocks(TAC, leaders)
	regmem = regmemDescriptor(register_list,variables,fp)
	# pprint.pprint(basicBlocks)
	GenerateSymbolTable(basicBlocks,SymbolTable,variables)
	#pprint.pprint(SymbolTable)
	# for i in SymbolTable:
	# 	for j in SymbolTable[i]:
	# 		SymbolTable[i][j].printTable()
	# pprint.pprint(variables)

	#printing starts here
	fp.write("section .text\n")
	fp.write("\tglobal _start\n")
	for basicBlock in basicBlocks:
		if basicBlocks.index(basicBlock)==0:
			fp.write("_start:\n")
		elif basicBlock[0][1]=='label':
			fp.write("%s:\n" % basicBlock[0][2])
		else:
			fp.write("label%d:\n" % basicBlock[0][0])

		for line in basicBlock:
			if line[1]=='=':
				fp.write("\tmovl $(%d), %s\n" %(line[3],regmem.getRegister(line[2])))
			#elif line[]=='+':
			#all the translation code deoending upon operators
	print "section .data"
	for variable in variables:
		fp.write("%s:\n" % variable.replace("$",""))
		fp.write("\t.int\n")


def BasicBlocks(TAC,leaders):
	#break code into basic blocks
	basicBlocks= []
	variables = []
	for i in range(0,len(leaders)):
		tempBlock=[]
		tempBlock.append(TAC[leaders[i]-1])
		# while (i<(len(leaders)-1) and leaders[i+1]==leaders[i]):
		# 	i+=1
		if(i!=(len(leaders)-1)):
			for j in range(leaders[i]+1,leaders[i+1]):
				tempBlock.append(TAC[j-1])
		elif(i==(len(leaders)-1)):
			for j in range(leaders[i]+1,len(TAC)+1):
				tempBlock.append(TAC[j-1])
		basicBlocks.append(tempBlock)
		for line in tempBlock:
			for point in line:
				if(point[0]=='$' and point not in variables):
					variables.append(point)
	return basicBlocks,variables

def GenerateSymbolTable(basicBlocks,SymbolTable,variables):
	for block in basicBlocks:
		leader = block[0][0]
		SymbolTable[leader] = dict()
		nextTable = None
		for TACline in reversed(block):
			SymbolTable[leader][TACline[0]] = symbolTable(variables,TACline,nextTable)
			nextTable = SymbolTable[leader][TACline[0]]

# def GetReg(variable,SymbolTable,regmem):
# 	if(regmem.getLoc(variable)!=None):
# 		return regmem.getLoc(variable)
# 	elif regmem.emptyReg()!=None:
# 		return regmem.emptyReg()
	# elif

if __name__=="__main__":
	filename = sys.argv[1]
	sourcefile = open(filename)
	#print code
	generateAssCode(sourcefile)
