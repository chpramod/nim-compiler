#!/usr/bin/python

#this program will convert 3-addr code to x86 assembly code
import sys


if __name__=="__main__": 
	filename = sys.argv[1]
	sourcefile = open(filename)
	code = sourcefile.read()