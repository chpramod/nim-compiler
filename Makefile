all :
	python parser.py grtngs.nim
	dot -Tps grtngs.dot -o tree
	evince tree &
	python preprocess.py testinput.txt>testinput1.txt
	python codegen.py testinput1.txt
	as -32 AssCode.s -o output.o
	ld output.o -o output -m elf_i386 -lc -dynamic-linker /lib/ld-linux.so.2
	./output
	@echo

allpree:
	python parser.py grtngs.nim
	# dot -Tps grtngs.dot -o tree
	# evince tree &
	python preprocess.py testinput.txt>testinput1.txt
	python codegen.py testinput1.txt
	as -32 AssCode.s -o output.o
	ld output.o -o output -m elf_i386 -lc -dynamic-linker /lib/ld-linux.so.2
	./output
	@echo

ass:
	python preprocess.py testinput.txt>testinput1.txt
	python codegen.py testinput1.txt
	as -32 AssCode.s -o output.o
	ld output.o -o output -m elf_i386 -lc -dynamic-linker /lib/ld-linux.so.2
	./output
	@echo
lla:
	python codegen.py test6.ir
	as -32 AssCode.s -o output.o
	ld output.o -o output -m elf_i386 -lc -dynamic-linker /lib/ld-linux.so.2
	./output
	@echo
parse:
	python parser.py grtngs.nim
	dot -Tps grtngs.dot -o tree
	evince tree &

assonly:
	as -32 AssCode.s -o output.o
	ld output.o -o output -m elf_i386 -lc -dynamic-linker /lib/ld-linux.so.2
	./output
	@echo
