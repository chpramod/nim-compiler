all:
	python preprocess.py testinput.txt>testinput1.txt
	python codegen.py testinput1.txt
	as -32 AssCode.s -o output.o
	ld output.o -o output -m elf_i386 -lc -dynamic-linker /lib/ld-linux.so.2
	./output