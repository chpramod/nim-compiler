#!/usr/bin/python

#this program will convert 3-addr code to x86 assembly code
import sys
import pprint

jumpLabels=["goto","ifgoto","call","label"]

def processTAC(TAC):


def generateAssCode(code):
	leaders=[]
	TAC = []
	with code as f:
		for line in f:
			line=line.rstrip('\n')
			splitLine=line.split(', ')
			print splitLine[1]
			if splitLine[0]=='1':
				leaders.append(splitLine[0])
			elif splitLine[1] in jumpLabels:
				leaders.append(splitLine[0])
			TAC.append(splitLine)
	pprint.pprint(TAC)
	processTAC(TAC)

if __name__=="__main__":
	filename = sys.argv[1]
	sourcefile = open(filename)
	#print code
	generateAssCode(sourcefile)
