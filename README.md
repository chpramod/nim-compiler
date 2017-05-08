Nim-compiler
===================================

Nim-compiler is written by making use of the PLY (Python Lex-Yacc) package.


## Instructions to run
- Use makefile to run.
	make parse to parse
	make all to compile completely


## Language specifications:

### Basic data types

	-	Int
	-	Bool (boolean `true` and `false`)
	-   char define as, var a:char = 'a'
    -   string  define as, var a:string = "abc"

### Variable declaration and assignment

	-	A variable has to be declared before using it.
		e.g.
			var x = 1
			var y: int = 5
	-	We **do not** support dynamic typing. Once a variable has been assigned a type, it can't be assigned values of other types.  
		e.g.
			var x = 1
			x = true
		This will not work, as x is of type Int, a Bool to x is wrong.
	- "let" can be used to create constants
	 		e.g.
			  let a = 5
				now,
				a = 6 is not allowed.
				Value of a is fixed as 5
### Arrays
	-	Arrays have all elements of the same type, with the size of array being in the type information of that array.
		var a:array[7,int]
		This program creates an array `x` in memory, storing 7 integers.
			x = [1,2]
			x = [1,2,3]
		This is a not yet done.
	-	Although arrays cannot be passed to methods by reference.

### Arithmetic and Logical Operators
	-	bitwise
	-	arithmetic
	-	boolean
	-	comparison
	-	assignment `+=, -=, *=, /=`

### Basic imperative constructs
	-	if-elif-else
			if check-expr :
				body
			elif check-expr :
				body
			else :
				body
	-	while
			while check-expr :
				body
    -   break and continue 
        break is used to break the loop
		contine is used  to go to start of loop without running the remaining code

### Methods or Procs
	-	Definition
			proc/method (argument list) : returntype =
				function body
		e.g.
		proc items(range: int) =
  		var i:bool=false
  		while i :
    		i+=1
    		echo i

### Output
	- 'echo' is used to print on stdoutput
	- a list of arguments can be printed as
	- arguments can be int, string, char and bool
		e.g.
            a = 1
			echo a
	- a list of arguments can be printed as
				echo a,"xyz \n", 1, 'g'

### Input
- scan, scanchar, scanstr are used to input int, char and strings respectively

### Our features
- Checks if some variable contains garbage value. We  assign a 'hasVal' to every variable which is 0 if  it contains garbage else 1.
- Type checking is done. Shows error if there is any type mismatch.
