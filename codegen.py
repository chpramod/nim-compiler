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

# {=+*-/%>><<ifgoto(leq,eq,le,geq,gr,neq) goto print call label ret aright aleft left_star right_star }

def generateAssCode(code):
	global register_list,variables
	fp = open("AssCode.s",'w')
	leaders=[]
	arrayDef=[]
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
				#print "inside"
				#print "%d" % int(splitLine[0])
				leaders.append(int(splitLine[0]))
				#print len(leaders)
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
	#print leaders
	leaders.sort(key=int)
	#print leaders
	extra=totalLines+1
	if extra in	leaders:
		#print "inside1"
		leaders.remove(extra)         #removes an entry which is added after reading last line
	if len(leaders) == 0:
			return 0
	#print leaders
	leaders=list(set(leaders))			#This line removes duplicates
	leaders.sort(key=int)
	#print leaders
	# pprint.pprint(leaders)
	# for k in range(1,len(leaders)-p):
	# 	print leaders[len(leaders)-k]
	# 	leaders.remove(leaders[len(leaders)-k])
	# pprint.pprint(TAC)
	#print TAC[0]
	#print len(leaders)
	basicBlocks,variables = BasicBlocks(TAC, leaders)
	regmem = regmemDescriptor(register_list,variables,fp)
	#pprint.pprint(basicBlocks)
	GenerateSymbolTable(basicBlocks,SymbolTable,variables)
	#pprint.pprint(SymbolTable)
	# for i in SymbolTable:
	# 	for j in SymbolTable[i]:
	# 		SymbolTable[i][j].printTable()
	# pprint.pprint(variables)

	#printing starts here
	fp.write(".section .text\n")
	fp.write("\t.global _start\n")
	leader_index=-1
	for basicBlock in basicBlocks:
		leader_index+=1
		if basicBlocks.index(basicBlock)==0:
			fp.write("_start:\n")
		elif basicBlock[0][1]=='label':
			fp.write("%s:\n" % basicBlock[0][2])
		else:
			fp.write("label%s:\n" % basicBlock[0][0])

		for line in basicBlock:
			regmem.protectRegs(line)
			regmem.setST(SymbolTable[str(leaders[leader_index])][line[0]])
			SymbolTable[str(leaders[leader_index])][line[0]].printTable()
			pprint(line)
			pprint(regmem.variableList)
			if line[1]=='=': #a=b[] #a[]=b #a[]=2
				if line[3].startswith('$'):
					if line[2].endswith("]"):                                                           #a[]=b
						regmem.freeReg('%eax')
						tempIndex=line[2].find('[')
						tempStr=line[2][1:tempIndex]
						fp.write("\tmovl $({0}), %eax\n".format(tempStr))
						tempStr=line[2][tempIndex+1:-1]
						fp.write("\tmovl %s, %d(%eax)\n" %(regmem.getRegister(line[3]),4*int(tempStr)))
					else:
						fp.write("\tmovl %s, %s\n" %(regmem.getRegister(line[3]),regmem.getRegister(line[2])))	#a=b
				else:
					if line[2].endswith("]"):                                                           #a[]=2
						regmem.freeReg('%eax')
						tempIndex=line[2].find('[')
						tempStr=line[2][1:tempIndex]
						fp.write("\tmovl $({0}), %eax\n".format(tempStr))
						tempStr=line[2][tempIndex+1:-1]
						fp.write("\tmovl ${0}, {1}(%eax)\n" .format(line[3],4*int(tempStr)))
					else:
						fp.write("\tmovl $%s, %s\n" %(line[3],regmem.getRegister(line[2])))	     			#a=2
			elif line[1]=='+':
				if (line[3].startswith('$') and line[4].startswith('$')):
					if (line[2]==line[3]):																	#a=a+b
						fp.write("\taddl %s, %s\n" %(regmem.getRegister(line[4]),regmem.getRegister(line[3])))
					elif (line[2]==line[4]):																#a=b+a
						fp.write("\taddl %s, %s\n" %(regmem.getRegister(line[3]),regmem.getRegister(line[4])))
					else:																					#c=a+b
						fp.write("\tmovl %s, %s\n" %(regmem.getRegister(line[3]),regmem.getRegister(line[2])))
						fp.write("\taddl %s, %s\n" %(regmem.getRegister(line[4]),regmem.getRegister(line[2])))
				elif (line[3].startswith('$')):
					if (line[2]==line[3]):																	#a=a+2
						fp.write("\taddl $%s, %s\n" %(line[4],regmem.getRegister(line[3])))
					else:																					#b=a+2
						fp.write("\tmovl %s, %s\n" %(regmem.getRegister(line[3]),regmem.getRegister(line[2])))
						fp.write("\taddl $%s, %s\n" %(line[4],regmem.getRegister(line[2])))
				elif (line[4].startswith('$')):
					if (line[2]==line[4]):																	#a=2+a
						fp.write("\taddl $%s, %s\n" %(line[3],regmem.getRegister(line[4])))
					else:																					#b=2+a
						fp.write("\tmovl %s, %s\n" %(regmem.getRegister(line[4]),regmem.getRegister(line[2])))
						fp.write("\taddl $%s, %s\n" %(line[3],regmem.getRegister(line[2])))
				else:                                       												#a=1+2
					fp.write("\tmovl $%s, %s\n" %(line[3],regmem.getRegister(line[2])))
					fp.write("\taddl $%s, %s\n" %(line[4],regmem.getRegister(line[2])))
			elif line[1]=='*':
				if (line[3].startswith('$') and line[4].startswith('$')):
					if (line[2]==line[3]):										#a=a*b
						fp.write("\timull %s, %s\n" %(regmem.getRegister(line[4]),regmem.getRegister(line[3])))
					elif (line[2]==line[4]):								#a=b*a
						fp.write("\timull %s, %s\n" %(regmem.getRegister(line[3]),regmem.getRegister(line[4])))
					else:											#c=a*b
						fp.write("\tmovl %s, %s\n" %(regmem.getRegister(line[3]),regmem.getRegister(line[2])))
						fp.write("\timull %s, %s\n" %(regmem.getRegister(line[4]),regmem.getRegister(line[2])))
				elif (line[3].startswith('$')):
					if (line[2]==line[3]):										#a=a*2
						fp.write("\timull $%s, %s\n" %(line[4],regmem.getRegister(line[3])))
					else:																					#b=a*2
						fp.write("\tmovl %s, %s\n" %(regmem.getRegister(line[3]),regmem.getRegister(line[2])))
						fp.write("\timull $%s, %s\n" %(line[4],regmem.getRegister(line[2])))
				elif (line[4].startswith('$')):
					if (line[2]==line[4]):																	#a=2*a
						fp.write("\timull $%s, %s\n" %(line[3],regmem.getRegister(line[4])))
					else:																					#b=2*a
						fp.write("\tmovl %s, %s\n" %(regmem.getRegister(line[4]),regmem.getRegister(line[2])))
						fp.write("\timull $%s, %s\n" %(line[3],regmem.getRegister(line[2])))
				else:                                       												#a=1*2
					fp.write("\tmovl $%s, %s\n" %(line[3],regmem.getRegister(line[2])))
					fp.write("\timull $%s, %s\n" %(line[4],regmem.getRegister(line[2])))
			elif line[1]=='-':
				#a=b-c a=a-c a=c-a a=b-2 a=a-2 a=2-b a=b-2 a=3-2
				print "in"
				if (line[3].startswith('$') and line[4].startswith('$')):
					if (line[2]==line[3]):
						#a=a-c
						fp.write("\tsubl %s, %s\n" %(regmem.getRegister(line[4]),regmem.getRegister(line[2])))
					elif (line[2]==line[4]):
					# 	#a=c-a
					 	fp.write("\tsubl %s, %s\n" %(regmem.getRegister(line[3]),regmem.getRegister(line[2])))
					 	fp.write("\tnegl %s\n" % regmem.getRegister(line[2]))
	 				else:
	 				# 	#a=b-c
	 				 	fp.write("\tmovl %s, %s\n" %(regmem.getRegister(line[3]),regmem.getRegister(line[2])))
	 				 	fp.write("\tsubl %s, %s\n" %(regmem.getRegister(line[4]),regmem.getRegister(line[2])))
	 			elif(line[3].startswith('$')):                                                              #a=a-2
	 				if (line[2]==line[3]):
	 					fp.write("\tsubl $%s, %s\n" %(line[4],regmem.getRegister(line[3])))
	 				else:        																			#a=b-2
	 					fp.write("\tmovl %s, %s\n" %(regmem.getRegister(line[3]),regmem.getRegister(line[2])))
	 					fp.write("\tsubl $%s, %s\n" %(line[4],regmem.getRegister(line[2])))
				elif (line[4].startswith('$')):
					if (line[2]==line[4]):																	#a=2-a
						fp.write("\tsubl $%s, %s\n" %(line[3],regmem.getRegister(line[4])))
						fp.write("\tnegl %s\n" % regmem.getRegister(line[2]))
					else:																					#a=2-b
						fp.write("\tmovl %s, %s\n" %(regmem.getRegister(line[4]),regmem.getRegister(line[2])))
						fp.write("\tsubl $%s, %s\n" %(line[3],regmem.getRegister(line[2])))
						fp.write("\tnegl %s\n" % regmem.getRegister(line[2]))
				else:                                       												#a=3-2
					fp.write("\tmovl $%s, %s\n" %(line[3],regmem.getRegister(line[2])))
					fp.write("\tsubl $%s, %s\n" %(line[4],regmem.getRegister(line[2])))
			elif line[1]=='/':
				if (line[3].startswith('$') and line[4].startswith('$')):
					if (line[2]==line[3]):																	#a=a/b
						regmem.freeReg('%edx',True)
						regmem.setReg(line[4],'%ebx')
						regmem.setReg(line[2],'%eax')
						fp.write("\tidivl %ebx\n")
					elif (line[2]==line[4]):
						regmem.freeReg('%eax')
						fp.write("\tmovl %s, %s\n" %(regmem.getRegister(line[3]),'%eax'))					#a=b/a
						regmem.freeReg('%eax')
						regmem.freeReg('%edx',True)
						regmem.setReg(line[4],'%ebx')
						fp.write("\tidivl %ebx\n")
						regmem.setVarReg('%eax',line[2])
					else:																					#c=a/b
						# fp.write("\tmovl %s, %s\n" %(regmem.getRegister(line[3]),regmem.getRegister(line[2])))
						regmem.freeReg('%edx',True)
						regmem.setReg(line[4],'%ebx')
						regmem.setReg(line[3],'%eax')
						regmem.freeReg('%eax')
						fp.write("\tidivl %ebx\n")
						regmem.setVarReg('%eax',line[2])
				elif (line[3].startswith('$')):
					if (line[2]==line[3]):																	#a=a/2
						regmem.freeReg('%edx',True)
						regmem.setReg(line[3],'%eax')
						regmem.freeReg('%ebx')
						fp.write("\tmovl $%s, %s\n" %(line[4],'%ebx'))
						fp.write("\tidivl %ebx\n")
					else:																					#b=a/2
						# fp.write("\tmovl %s, %s\n" %(regmem.getRegister(line[3]),regmem.getRegister(line[2])))
						regmem.freeReg('%edx',True)
						regmem.setReg(line[3],'%eax')
						regmem.freeReg('%ebx')
						fp.write("\tmovl $%s, %s\n" %(line[4],'%ebx'))
						regmem.freeReg('%eax')
						fp.write("\tidivl %ebx\n")
						regmem.setVarReg('%eax',line[2])
				elif (line[4].startswith('$')):
					if (line[2]==line[4]):																	#a=2/a
						regmem.freeReg('%eax')
						regmem.freeReg('%edx',True)
						fp.write("\tmovl $%s, %s\n" %(line[3],'%eax'))
						regmem.setReg(line[4],'%ebx')
						fp.write("\tidivl %ebx\n")
						regmem.setVarReg('%eax',line[2])
					else:																					#b=2/a
						regmem.freeReg('%eax')
						regmem.freeReg('%edx',True)
						fp.write("\tmovl $%s, %s\n" %(line[3],'%eax'))
						regmem.setReg(line[4],'%ebx')
						fp.write("\tidivl %ebx\n")
						regmem.setVarReg('%eax',line[2])
				else:                                       												#a=3/2
					regmem.freeReg('%eax')
					regmem.freeReg('%edx',True)
					fp.write("\tmovl $%s, %s\n" %(line[3],'%eax'))
					regmem.freeReg('%ebx')
					fp.write("\tmovl $%s, %s\n" %(line[4],'%ebx'))
					fp.write("\tidivl %s\n" %('%ebx'))
					regmem.setVarReg('%eax',line[2])
			elif line[1]=='mod':
				if (line[3].startswith('$') and line[4].startswith('$')):
					if (line[2]==line[3]):																	#a=a mod b
						regmem.freeReg('%edx',True)
						regmem.setReg(line[4],'%ebx')
						regmem.setReg(line[2],'%eax')
						fp.write("\tidivl %ebx\n")
						regmem.setVarReg('%edx',line[2])
					elif (line[2]==line[4]):
						regmem.freeReg('%eax')
						fp.write("\tmovl %s, %s\n" %(regmem.getRegister(line[3]),'%eax'))					#a=b mod a
						regmem.freeReg('%eax')
						regmem.freeReg('%edx',True)
						regmem.setReg(line[4],'%ebx')
						fp.write("\tidivl %ebx\n")
						regmem.setVarReg('%edx',line[2])
					else:																					#c=a mod b
						# fp.write("\tmovl %s, %s\n" %(regmem.getRegister(line[3]),regmem.getRegister(line[2])))
						regmem.freeReg('%edx',True)
						regmem.setReg(line[4],'%ebx')
						regmem.setReg(line[3],'%eax')
						regmem.freeReg('%eax')
						fp.write("\tidivl %ebx\n")
						regmem.setVarReg('%edx',line[2])
				elif (line[3].startswith('$')):
					if (line[2]==line[3]):																	#a=a mod 2
						regmem.freeReg('%edx',True)
						regmem.setReg(line[3],'%eax')
						regmem.freeReg('%ebx')
						fp.write("\tmovl $%s, %s\n" %(line[4],'%ebx'))
						fp.write("\tidivl %ebx\n")
						regmem.setVarReg('%edx',line[2])
					else:																					#b=a mod 2
						# fp.write("\tmovl %s, %s\n" %(regmem.getRegister(line[3]),regmem.getRegister(line[2])))
						regmem.freeReg('%edx',True)
						regmem.setReg(line[3],'%eax')
						regmem.freeReg('%ebx')
						fp.write("\tmovl $%s, %s\n" %(line[4],'%ebx'))
						regmem.freeReg('%eax')
						fp.write("\tidivl %ebx\n")
						regmem.setVarReg('%edx',line[2])
				elif (line[4].startswith('$')):
					if (line[2]==line[4]):																	#a=2 mod a
						regmem.freeReg('%eax')
						regmem.freeReg('%edx',True)
						fp.write("\tmovl $%s, %s\n" %(line[3],'%eax'))
						regmem.setReg(line[4],'%ebx')
						fp.write("\tidivl %ebx\n")
						regmem.setVarReg('%edx',line[2])
					else:																					#b=2 mod a
						regmem.freeReg('%eax')
						regmem.freeReg('%edx',True)
						fp.write("\tmovl $%s, %s\n" %(line[3],'%eax'))
						regmem.setReg(line[4],'%ebx')
						fp.write("\tidivl %ebx\n")
						regmem.setVarReg('%edx',line[2])
				else:                                       												#a=3 mod 2
					regmem.freeReg('%eax')
					regmem.freeReg('%edx',True)
					fp.write("\tmovl $%s, %s\n" %(line[3],'%eax'))
					regmem.freeReg('%ebx')
					fp.write("\tmovl $%s, %s\n" %(line[4],'%ebx'))
					fp.write("\tidivl %s\n" %('%ebx'))
					regmem.setVarReg('%edx',line[2])
			elif line[1]=='goto':																			#goto 2
				if (line[2].isdigit()):
					fp.write("\tjmp label%s\n"%(line[2]))
				else:
					fp.write("\tjmp %s\n"%(line[2]))
			elif line[1]=='ifgoto':																	#ifgoto(leq,eq,le,geq,ge,neq)
				if (line[2]=='leq'):
					if (line[3].startswith('$') and line[4].startswith('$')):					#a<=b				#ifgoto, leq, a, b, 2
						fp.write("\tcmpl %s, %s\n" %(regmem.getRegister(line[4]),regmem.getRegister(line[3])))
						if (line[5].isdigit()):
							fp.write("\tjle label%s\n"%(line[5]))
						else:
							fp.write("\tjle %s\n"%(line[5]))
					elif (line[3].startswith('$')):												#a<=2
						fp.write("\tcmpl $%s, %s\n" %(line[4],regmem.getRegister(line[3])))
						if (line[5].isdigit()):
							fp.write("\tjle label%s\n"%(line[5]))
						else:
							fp.write("\tjle %s\n"%(line[5]))
					elif (line[4].startswith('$')):												#2<=a
						fp.write("\tcmpl %s, $%s\n" %(regmem.getRegister(line[4]),line[3]))
						if (line[5].isdigit()):
							fp.write("\tjle label%s\n"%(line[5]))
						else:
							fp.write("\tjle %s\n"%(line[5]))
					else:																		#3<=2
						fp.write("\tcmpl $%s, $%s\n" %(line[4],line[3]))
						if (line[5].isdigit()):
							fp.write("\tjle label%s\n"%(line[5]))
						else:
							fp.write("\tjle %s\n"%(line[5]))
				if (line[2]=='geq'):
					if (line[3].startswith('$') and line[4].startswith('$')):					#a>=b				#ifgoto, geq, a, b, 2
						fp.write("\tcmpl %s, %s\n" %(regmem.getRegister(line[4]),regmem.getRegister(line[3])))
						if (line[5].isdigit()):
							fp.write("\tjge label%s\n"%(line[5]))
						else:
							fp.write("\tjge %s\n"%(line[5]))
					elif (line[3].startswith('$')):												#a>=2
						fp.write("\tcmpl $%s, %s\n" %(line[4],regmem.getRegister(line[3])))
						if (line[5].isdigit()):
							fp.write("\tjge label%s\n"%(line[5]))
						else:
							fp.write("\tjge %s\n"%(line[5]))
					elif (line[4].startswith('$')):												#2>=a
						fp.write("\tcmpl %s, $%s\n" %(regmem.getRegister(line[4]),line[3]))
						if (line[5].isdigit()):
							fp.write("\tjge label%s\n"%(line[5]))
						else:
							fp.write("\tjge %s\n"%(line[5]))
					else:																		#3>=2
						fp.write("\tcmpl $%s, $%s\n" %(line[4],line[3]))
						if (line[5].isdigit()):
							fp.write("\tjge label%s\n"%(line[5]))
						else:
							fp.write("\tjge %s\n"%(line[5]))
				elif (line[2]=='eq'):
					if (line[3].startswith('$') and line[4].startswith('$')):					#a==b
						fp.write("\tcmpl %s, %s\n" %(regmem.getRegister(line[4]),regmem.getRegister(line[3])))
						if (line[5].isdigit()):
							fp.write("\tje label%s\n"%(line[5]))
						else:
							fp.write("\tje %s\n"%(line[5]))
					elif (line[3].startswith('$')):												#a==2
						fp.write("\tcmpl $%s, %s\n" %(line[4],regmem.getRegister(line[3])))
						if (line[5].isdigit()):
							fp.write("\tje label%s\n"%(line[5]))
						else:
							fp.write("\tje %s\n"%(line[5]))
					elif (line[4].startswith('$')):												#2==a
						fp.write("\tcmpl %s, $%s\n" %(regmem.getRegister(line[4]),line[3]))
						if (line[5].isdigit()):
							fp.write("\tje label%s\n"%(line[5]))
						else:
							fp.write("\tje %s\n"%(line[5]))
					else:																		#3==2
						fp.write("\tcmpl $%s, $%s\n" %(line[4],line[3]))
						if (line[5].isdigit()):
							fp.write("\tje label%s\n"%(line[5]))
						else:
							fp.write("\tje %s\n"%(line[5]))
				elif (line[2]=='le'):
					if (line[3].startswith('$') and line[4].startswith('$')):					#a<b				#ifgoto, leq, a, b, 2
						fp.write("\tcmpl %s, %s\n" %(regmem.getRegister(line[4]),regmem.getRegister(line[3])))
						if (line[5].isdigit()):
							fp.write("\tjle label%s\n"%(line[5]))
						else:
							fp.write("\tjle %s\n"%(line[5]))
					elif (line[3].startswith('$')):												#a<2
						fp.write("\tcmpl $%s, %s\n" %(line[4],regmem.getRegister(line[3])))
						if (line[5].isdigit()):
							fp.write("\tjle label%s\n"%(line[5]))
						else:
							fp.write("\tjle %s\n"%(line[5]))
					elif (line[4].startswith('$')):												#2<a
						fp.write("\tcmpl %s, $%s\n" %(regmem.getRegister(line[4]),line[3]))
						if (line[5].isdigit()):
							fp.write("\tjle label%s\n"%(line[5]))
						else:
							fp.write("\tjle %s\n"%(line[5]))
					else:																		#3<2
						fp.write("\tcmpl $%s, $%s\n" %(line[4],line[3]))
						if (line[5].isdigit()):
							fp.write("\tjle label%s\n"%(line[5]))
						else:
							fp.write("\tjle %s\n"%(line[5]))
				elif (line[2]=='gr'):
					if (line[3].startswith('$') and line[4].startswith('$')):					#a>b				#ifgoto, geq, a, b, 2
						fp.write("\tcmpl %s, %s\n" %(regmem.getRegister(line[4]),regmem.getRegister(line[3])))
						if (line[5].isdigit()):
							fp.write("\tjg label%s\n"%(line[5]))
						else:
							fp.write("\tjg %s\n"%(line[5]))
					elif (line[3].startswith('$')):												#a>2
						fp.write("\tcmpl $%s, %s\n" %(line[4],regmem.getRegister(line[3])))
						if (line[5].isdigit()):
							fp.write("\tjg label%s\n"%(line[5]))
						else:
							fp.write("\tjg %s\n"%(line[5]))
					elif (line[4].startswith('$')):												#2>a
						fp.write("\tcmpl %s, $%s\n" %(regmem.getRegister(line[4]),line[3]))
						if (line[5].isdigit()):
							fp.write("\tjg label%s\n"%(line[5]))
						else:
							fp.write("\tjg %s\n"%(line[5]))
					else:																		#3>2
						fp.write("\tcmpl $%s, $%s\n" %(line[4],line[3]))
						if (line[5].isdigit()):
							fp.write("\tjg label%s\n"%(line[5]))
						else:
							fp.write("\tjg %s\n"%(line[5]))
				elif (line[2]=='neq'):
					if (line[3].startswith('$') and line[4].startswith('$')):					#a==b
						fp.write("\tcmpl %s, %s\n" %(regmem.getRegister(line[4]),regmem.getRegister(line[3])))
						if (line[5].isdigit()):
							fp.write("\tjne label%s\n"%(line[5]))
						else:
							fp.write("\tjne %s\n"%(line[5]))
					elif (line[3].startswith('$')):												#a==2
						fp.write("\tcmpl $%s, %s\n" %(line[4],regmem.getRegister(line[3])))
						if (line[5].isdigit()):
							fp.write("\tjne label%s\n"%(line[5]))
						else:
							fp.write("\tjne %s\n"%(line[5]))
					elif (line[4].startswith('$')):												#2==a
						fp.write("\tcmpl %s, $%s\n" %(regmem.getRegister(line[4]),line[3]))
						if (line[5].isdigit()):
							fp.write("\tjne label%s\n"%(line[5]))
						else:
							fp.write("\tjne %s\n"%(line[5]))
					else:																		#3==2
						fp.write("\tcmpl $%s, $%s\n" %(line[4],line[3]))
						if (line[5].isdigit()):
							fp.write("\tjne label%s\n"%(line[5]))
						else:
							fp.write("\tjne %s\n"%(line[5]))
			elif line[1]=='call':
				regmem.freeAll()
				fp.write("\tcall %s\n"%(line[2]))
				if len(line)==4:
					regmem.setVarReg('%eax',line[3])
			elif line[1]=='ret':
				if len(line)==3:
					regmem.freeReg('%eax')
					fp.write("\tmovl {0}, %eax\n" .format(regmem.getRegister(line[2])))
					regmem.freeReg('%eax')
				fp.write("\tret\n")
			elif line[1]=='print':
				if line[2].startswith('$'):
					# a=regmem.getRegister(line[2])                                                            #print a
					# print a
					regmem.freeAll()
					fp.write("\tpushl %s\n"%(line[2][1:]))
					fp.write("\tcall printIntNumber\n")
				else:																							#print 2
					regmem.freeAll()
					fp.write("\tpushl $%s\n"%(line[2]))
					fp.write("\tcall printIntNumber\n")
			elif line[1]=='scan':
					a=regmem.getRegister(line[2])                                                            #print a
					print a
					regmem.freeReg(a)
					#fp.write("\tmovl {0}, {1}\n" .format(a,line[2][1:]))
					fp.write("\tpushl {0}\n".format(line[2]))
					fp.write("\tpushl $formatstr\n\tcall scanf\n")
			elif line[1]=='array':
				arrayCurrent=[line[2],line[3]]
				arrayDef.append(arrayCurrent)
			elif line[1]=='end':
				fp.write("\tcall endlabel\n")
			elif line[1]=='incr':																#incr,a
				fp.write("\tincl %s\n"%(regmem.getRegister(line[2])))
			elif line[1]=='decr':																#decr,a
				fp.write("\tdecl %s\n"%(regmem.getRegister(line[2])))
			elif (line[1]=='shl' or line[1]=='shr'):
				if (line[3].startswith('$') and line[4].startswith('$')):
					if (line[2]==line[3]):											# a = a << b
						regmem.setReg(line[4],'%ecx')
						regmem.setReg(line[3],'%eax')
						fp.write("\t{0}l {1}, %eax\n".format(line[1],'%cl'))
					elif (line[2]==line[4]):										# a = b << a
						regTempb = regmem.getRegister(line[3])
						regTempa = regmem.getRegister(line[4])
						regmem.setReg('%ecx',line[4])
						regmem.freeReg(regTemp)
						fp.write("\t%sl %s, %s\n"%(line[1],regTempa,regTempb))
						regmem.setVarReg(regTempb,line[2])
					else:															# c = a << b
						fp.write("\tmovl %s, %s\n"%(regmem.getRegister(line[3]),regmem.getRegister(line[2])))
						fp.write("\t%sl %s, %s\n"%(line[1],regmem.getRegister(line[4]),regmem.getRegister(line[2])))
				elif(line[3].startswith('$')):
					if (line[2]==line[3]):											# a = a << 2
						fp.write("\t%sl %s, %s\n"%(line[1],line[4],regmem.getRegister(line[2])))
					else:															# a = b << 2
						fp.write("\tmovl %s, %s\n"%(regmem.getRegister(line[3]),regmem.getRegister(line[2])))
						fp.write("\t%sl %s, %s\n"%(line[1],line[4],regmem.getRegister(line[2])))
				elif(line[4].startswith('$')):
					if (line[2]==line[4]):											# a = 2 << a
						regmem.freeReg('%eax')
						regmem.setReg(line[2],'%ebx')
						fp.write("\tmovl $%s, %eax\n"%(line[3]))
						fp.write("\t%sl %ebx, %eax\n"%(line[1]))
						setVarReg('%eax',line[2])
					else:															# a = 2 << b
						fp.write("\tmovl $%s, %s\n"%(line[3],regmem.getRegister(line[2])))
						fp.write("\t%sl %s %s\n"%(line[1],regmem.getRegister(line[4]),regmem.getRegister(line[2])))
				else:																# a = 2 << 3
					fp.write("\tmovl $%s, %s\n"%(line[3],regmem.getRegister(line[2])))
					fp.write("\t%sl %s, %s\n"%(line[1],line[4],regmem.getRegister(line[2])))
			elif (line[1]=='and' or line[1]=='or' or line[1]=='xor'):			#bitwise operators
				if (line[3].startswith('$') and line[4].startswith('$')):
					if (line[2]==line[3]):											# a = a and b
						fp.write("\t%sl %s, %s\n"%(line[1],regmem.getRegister(line[4]),regmem.getRegister(line[2])))
					elif (line[2]==line[4]):										# a = b and a
						regTempb = regmem.getRegister(line[3])
						regTempa = regmem.getRegister(line[4])
						regmem.freeReg(regTemp)
						fp.write("\t%sl %s, %s\n"%(line[1],regTempa,regTempb))
						regmem.setVarReg(regTempb,line[2])
					else:															# c = a and b
						fp.write("\tmovl %s, %s\n"%(regmem.getRegister(line[3]),regmem.getRegister(line[2])))
						fp.write("\t%sl %s, %s\n"%(line[1],regmem.getRegister(line[4]),regmem.getRegister(line[2])))
				elif(line[3].startswith('$')):
					if (line[2]==line[3]):											# a = a and 2
						fp.write("\t%sl %s, %s\n"%(line[1],line[4],regmem.getRegister(line[2])))
					else:															# a = b and 2
						fp.write("\tmovl %s, %s\n"%(regmem.getRegister(line[3]),regmem.getRegister(line[2])))
						fp.write("\t%sl $%s, %s\n"%(line[1],line[4],regmem.getRegister(line[2])))
				elif(line[4].startswith('$')):
					if (line[2]==line[4]):											# a = 2 and a
						regmem.freeReg('%eax')
						regmem.setReg(line[2],'%ebx')
						fp.write("\tmovl $%s, %eax\n"%(line[3]))
						fp.write("\t%sl %ebx, %eax\n"%(line[1]))
						setVarReg('%eax',line[2])
					else:															# a = 2 and b
						fp.write("\tmovl $%s, %s\n"%(line[3],regmem.getRegister(line[2])))
						fp.write("\t%sl %s %s\n"%(line[1],regmem.getRegister(line[4]),regmem.getRegister(line[2])))
				else:																# a = 2 and 3
					fp.write("\tmovl $%s, %s\n"%(line[3],regmem.getRegister(line[2])))
					fp.write("\t%sl $%s, %s\n"%(line[1],line[4],regmem.getRegister(line[2])))
			elif line[1]=='not':													#(line,not,a,b)
				if (line[2].startswith('$') and line[3].startswith('$')):			# a = ~b
					fp.write("\tmovl %s, %s\n"%(regmem.getRegister(line[3]),regmem.getRegister(line[2])))
					fp.write("\tnotl %s\n"%(regmem.getRegister(line[2])))
				else:																# a = ~2
					fp.write("\tmovl $%s, %s\n"%(line[3],regmem.getRegister(line[2])))
					fp.write("\tnotl %s\n"%(regmem.getRegister(line[2])))
			regmem.freeRegister()
			#all the translation code deoending upon operators
	fp.write("\n#the print function for integers\n\
jmp EndPrintNum\n\
printIntNumber:\n\
	movl 4(%esp), %ecx\n\
    cmpl $0, %ecx\n\
    jge positive_part #if number is >=0\n\
    notl %ecx               #Other wise make positive : BIT wise NOT\n\
    inc %ecx                #Increment to take negative\n\
    movl %ecx, %edi         #Save the ecx value\n\
    \n\
    movl    $45, %eax   #print the - sign\n\
    pushl   %eax  # add '-' character to the stack to print\n\
    movl $4, %eax\n\
    movl $1, %ebx\n\
    movl %esp, %ecx\n\
    movl $1, %edx\n\
    int $0x80\n\
    popl %eax  #Remove the top from the stack\n\
    movl %edi, %ecx  #Restore %ecx back \n\
	\n\
	\n\
positive_part:\n\
    movl %ecx, %eax   #storing number in %eax and will act as quotient\n\
    movl %esp, %esi   #storing the initial position of the stack positive_part_printer in %esi register\n\
iter_labl:\n\
    cdq\n\
    movl $10, %ebx    # %ebx is the divisor\n\
    idivl %ebx        #divide number by 10.remainder in %edx\n\
    pushl %edx        #pushing the least significant digit into stack for later print\n\
    cmpl $0, %eax     #check if we have extracted all digits\n\
    jne iter_labl     #If not equal to zero,then we continue printing the digits\n\
    jmp print_num     #else if quotient=0, then jump to print_num\n\
    \n\
print_num:\n\
    popl %edx         #poping the topmost element as digit of our number pushed into the stack\n\
    addl $48, %edx    #converting ascii character\n\
    pushl %edx        #only to pop later\n\
    movl $4, %eax     #4 is print sys-call number\n\
    movl $1, %ebx     #1 for to stdout\n\
    movl %esp, %ecx   #number+50 refers to location where the digit is stored in memory \n\
    movl $1, %edx     #size of buffer=1 coz we r printn one digit\n\
    int $0x80         #execute\n\
    popl %edx         #Pop the digit on the top  \n\
    cmp %esp, %esi    #checking if all digits exhausted\n\
    jne print_num     #we jump back to print_num label to print rest of digits\n\
    ret  \n\
    EndPrintNum:\n")
	fp.write("\n\nendlabel:\n\
	movl $1, %eax\n\
	movl $0, %ebx\n\
	int $0x80\n")
	fp.write("\n\n\n.section .data\n")
	for arrays in arrayDef:
		fp.write("%s:\n" % arrays[0].replace("$",""))
		variables.remove(arrays[0])
		fp.write("\t.space %d\n"%(int(arrays[1])*4))
	for variable in variables:
		if variable.find('[')!=-1:
			variables.remove(variable)
		else:
			fp.write("%s:\n" % variable.replace("$",""))
			fp.write("\t.long 0\n")
	fp.write("formatstr:\n\t.ascii \"\%d\"\n")


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
			#print SymbolTable[leader][TACline[0]].table
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
