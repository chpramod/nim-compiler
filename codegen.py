#!/usr/bin/python

#this program will convert 3-addr code to x86 assembly code
import sys
import pprint

jumpLabels=["goto","ifgoto","call","label","ret"]

def generateAssCode(code):
	leaders=[]
	TAC = []
	with code as f:
		for line in f:
			line=line.rstrip('\n')
			splitLine=line.split(', ')
			#print splitLine[1]
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
					for lineIter in f:
						lineIter=lineIter.rstrip('\n')
						splitLineIter=lineIter.split(', ')
						if splitLineIter[1]=='label' and splitLineIter[2]==splitLine[2]:
							leaders.append(int(splitLineIter[0]))
					leaders.append(int(splitLine[0])+1)
			TAC.append(splitLine)
	leaders.sort()		                                
	pprint.pprint(TAC)
	pprint.pprint(leaders)
	processTAC(TAC, leaders)

def processTAC(TAC,leaders):
	basicBlocks=[]
	for i in range(0:len(leaders)-1):
		

if __name__=="__main__":
	filename = sys.argv[1]
	sourcefile = open(filename)
	#print code
	generateAssCode(sourcefile)
