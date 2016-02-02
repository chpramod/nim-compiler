#!/usr/bin/python

#this program will convert 3-addr code to x86 assembly code
import sys
import pprint

jumpLabels=["goto","ifgoto","call","label","ret"]

def generateAssCode(code):
	leaders=[]
	TAC = []
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
	leaders.remove(totalLines+1)         #removes an entry which is added after reading last line 
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
	pprint.pprint(leaders)
	# for k in range(1,len(leaders)-p):
	# 	print leaders[len(leaders)-k]
	# 	leaders.remove(leaders[len(leaders)-k])                               
	pprint.pprint(TAC)
	processTAC(TAC, leaders)

def processTAC(TAC,leaders):
	#break code into basic blocks	
	basicBlocks=[]
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
	pprint.pprint(basicBlocks)
		


if __name__=="__main__":
	filename = sys.argv[1]
	sourcefile = open(filename)
	#print code
	generateAssCode(sourcefile)
