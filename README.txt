Only these types of constructs are allowed in our three address code.

operations							Three address code
====================				==================

Assignment
----------
 a = b 								lineno, =, $a, $b
 a = 2								lineno, =, $a, 2

Arithmetic and Bitwise
----------------------
a = b op c  						lineno, op, $a, $b, $c
a = b op 2							lineno, op, $a, $b, 2
a = a op 2							lineno, op, $a, $a, 2
a = a op b							lineno, op, $a, $a, $b
a = b op a 							lineno, op, $a, $b, $a			
a = 2 op a							lineno, op, $a, 2, $a
a = 2 op b               			lineno, op, $a, 2, $b
a = 2 op 3							lineno, op, $a, 2, 3


The following operators are supported in our code generator

Operation				Operator           Representation in three address code
*********				*********		   ************************************
addition				   + 					+
subtraction				   -					-
multiplication			   *					*
division				   /					/
modulo				   	   %					mod
bitwise leftshift		   <<					shl
bitwise rightshift         >>                   shr
bitwise and                and                  and
bitwise or                 or                   or
bitwise xor                xor                  xor

Jump
------------
goto line number 5								lineno, goto, 5

Conditional Jump
-----------------
if (a relop b) goto line number 3         		lineno, ifgoto, relop, $a, $b, 3

    where relop can be the following:
    Operator  			 3 addr code
    ********			*************
       <=					leq
       >=					geq
       ==					eq
       <					le
       >					gr
       !=					neq


Print
--------------
print a variable "x"							lineno, print, $x

Scan 
--------------
scan an input variable "x"						lineno, scan, $x


Call a function
---------------
call function "foo"								lineno, call, foo

Increment and Decrement
-----------------------
a = a + 1										lineno, incr, $a
a = a - 1										lineno, decr, $a

Bitwise not, negative of number
-------------------------------

b = ~a 											lineno, not, $a, $b (OR)
b = -a												lineno, neg, $a, $b

Return 
-------
return call for a Function 						lineno, ret

End
-----

end of MAIN										lineno, end

NOTE:	Any function call in 3 addr code must be made after the 'end' statement

Array
-------



Points to note :
-----------------

1. The three address code must be in the exact format mentioned above, any extra spaces or characters will result in an error.

2. "lineno" in the above format is the line number of the three address code.

