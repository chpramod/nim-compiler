#!/usr/bin/python

#this program will convert 3-addr code to x86 assembly code
import sys


def generateAssCode(code):
	jumpLabels=["goto","ifgoto","goto","call","label","ret"]
	label=[]
	with code as f:
		for line in f:
			line=line.rstrip('\n')
			splitLine=line.split(', ')
			print splitLine[0]
			if splitLine[0]=='1':
				label.append(splitLine[0])
			elif splitLine[1] in jumpLabels:
				label.append(splitLine[0])
	#leaders=getLeaders(code)


#def getleaders(code):



if __name__=="__main__": 
	filename = sys.argv[1]
	sourcefile = open(filename)
	#print code
	generateAssCode(sourcefile)
