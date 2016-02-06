all:
	python codegen.py testinput.txt
	as -32 AssCode.s -o output.o
	ld -m elf_i386 output.o -o output
	./output