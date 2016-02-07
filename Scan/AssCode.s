.section .text
	.global _start
_start:
	MOVL a, %edx
	movl $1, %edx
	MOVL b, %ecx
	movl $2, %ecx
	MOVL c, %esi
	movl $3, %esi
	MOVL d, %ebx
	movl $4, %ebx
	MOVL e, %edi
	movl $5, %edi
	MOVL f, %eax
	movl $6, %eax
	MOVL %eax, f
	MOVL g, %eax
	movl $7, %eax
	MOVL %eax, g
	MOVL h, %eax
	movl $8, %eax
	MOVL %eax, h
	MOVL x, %eax
	movl %edx, %eax
	imull %ecx, %eax
	pushl %edx
	MOVL %eax, x
	MOVL %edi, e
	MOVL %ebx, d
	MOVL %esi, c
	MOVL %ecx, b
	MOVL %edx, a
	call printIntNumber
	MOVL b, %edx
	pushl %edx
	MOVL %edx, b
	call printIntNumber
	MOVL c, %edx
	pushl %edx
	MOVL %edx, c
	call printIntNumber
	MOVL d, %edx
	pushl %edx
	MOVL %edx, d
	call printIntNumber
	MOVL e, %edx
	pushl %edx
	MOVL %edx, e
	call printIntNumber
	MOVL f, %edx
	pushl %edx
	MOVL %edx, f
	call printIntNumber
	MOVL g, %edx
	pushl %edx
	MOVL %edx, g
	call printIntNumber
	MOVL h, %edx
	pushl %edx
	MOVL %edx, h
	call printIntNumber
	MOVL x, %edx
	pushl %edx
	MOVL %edx, x
	call printIntNumber
	MOVL c, %edx
	incl %edx
	MOVL d, %ecx
	incl %ecx
	MOVL e, %esi
	incl %esi
	MOVL f, %ebx
	incl %ebx
	MOVL g, %edi
	incl %edi
	MOVL h, %eax
	incl %eax
	MOVL %eax, h
	MOVL b, %eax
	incl %eax
	MOVL %edi, g
	MOVL a, %edi
	pushl %edi
	MOVL %eax, b
	MOVL %edi, a
	MOVL %ebx, f
	MOVL %esi, e
	MOVL %ecx, d
	MOVL %edx, c
	call printIntNumber
	MOVL b, %edx
	pushl %edx
	MOVL %edx, b
	call printIntNumber
	MOVL c, %edx
	pushl %edx
	MOVL %edx, c
	call printIntNumber
	MOVL d, %edx
	pushl %edx
	MOVL %edx, d
	call printIntNumber
	MOVL e, %edx
	pushl %edx
	MOVL %edx, e
	call printIntNumber
	MOVL f, %edx
	pushl %edx
	MOVL %edx, f
	call printIntNumber
	MOVL g, %edx
	pushl %edx
	MOVL %edx, g
	call printIntNumber
	MOVL h, %edx
	pushl %edx
	MOVL %edx, h
	call printIntNumber
	MOVL x, %edx
	pushl %edx
	MOVL %edx, x
	call printIntNumber

#the print function for integers
jmp EndPrintNum
printIntNumber:
	movl 4(%esp), %ecx
    cmpl $0, %ecx
    jge positive_part #if number is >=0
    notl %ecx               #Other wise make positive : BIT wise NOT
    inc %ecx                #Increment to take negative
    movl %ecx, %edi         #Save the ecx value
    
    movl    $45, %eax   #print the - sign
    pushl   %eax  # add '-' character to the stack to print
    movl $4, %eax
    movl $1, %ebx
    movl %esp, %ecx
    movl $1, %edx
    int $0x80
    popl %eax  #Remove the top from the stack
    movl %edi, %ecx  #Restore %ecx back 
	
	
positive_part:
    movl %ecx, %eax   #storing number in %eax and will act as quotient
    movl %esp, %esi   #storing the initial position of the stack positive_part_printer in %esi register
iter_labl:
    cdq
    movl $10, %ebx    # %ebx is the divisor
    idivl %ebx        #divide number by 10.remainder in %edx
    pushl %edx        #pushing the least significant digit into stack for later print
    cmpl $0, %eax     #check if we have extracted all digits
    jne iter_labl     #If not equal to zero,then we continue printing the digits
    jmp print_num     #else if quotient=0, then jump to print_num
    
print_num:
    popl %edx         #poping the topmost element as digit of our number pushed into the stack
    addl $48, %edx    #converting ascii character
    pushl %edx        #only to pop later
    movl $4, %eax     #4 is print sys-call number
    movl $1, %ebx     #1 for to stdout
    movl %esp, %ecx   #number+50 refers to location where the digit is stored in memory 
    movl $1, %edx     #size of buffer=1 coz we r printn one digit
    int $0x80         #execute
    popl %edx         #Pop the digit on the top  
    cmp %esp, %esi    #checking if all digits exhausted
    jne print_num     #we jump back to print_num label to print rest of digits
    ret  
    EndPrintNum:


endlabel:
	movl $1, %eax
	movl $0, %ebx
	int $0x80



.section .data
a:
	.long 0
b:
	.long 0
c:
	.long 0
d:
	.long 0
e:
	.long 0
f:
	.long 0
g:
	.long 0
h:
	.long 0
x:
	.long 0
