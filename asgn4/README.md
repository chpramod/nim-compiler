Nim-compiler
===================================

Nim-compiler is written by making use of the PLY (Python Lex-Yacc) package.


##Instructions to run
To run, run the following command:

	./compile test/NAME_OF_TEST_FILE.rb

This will give a file NAME_OF_TEST_FILE.s in the root folder with the MIPS assembly code.

To simulate the MIPS code on SPIM simulator, use the following command:

	spim -file NAME_OF_TEST_FILE.s



##Language specifications:

#	##Basic data types##

	-	Int

	-	Bool (boolean `true` and `false`)



#	##Variable declaration and assignment##

	-	A variable has to be declared before using it.

		e.g.

			var x = 1
			var y: int = 5

	-	We ##do not## support dynamic typing. Once a variable has been assigned a type, it can't be assigned values of other types.  

		e.g.

			var x = 1
			x = true

		This will not work, as x is of type Int, a Bool to x is wrong.



#	##Arrays##

	-	Arrays have all elements of the same type, with the size of array being in the type information of that array.

		var a:array[7,int]
		This program creates an array `x` in memory, storing 7 integers.

			x = [1,2]
			x = [1,2,3]

		This is a not yet done.

	-	Although arrays cannot be passed to methods by reference.

#	##Arithmetic and Logical Operators##


	-	bitwise

	-	arithmetic

	-	boolean

	-	comparison

	-	assignment `+=, -=, *=, /=`

#	##Basic imperative constructs##

	-	#if-elif-else#

			if check-expr :
				body

			elif check-expr :
				body

			else :
				body



	-	#while#

			while check-expr :
				body



#	##Methods or Procs##

	-	Definition

			proc/method (argument list) : returntype =
				function body



		e.g.

		proc items(range: int) =
  		var i:bool=false
  		while i :
    		i+=1
    		echo i





#	##Output##

	-	'echo' is used to print on stdoutput

		e.g.

			a = 1
			echo a
