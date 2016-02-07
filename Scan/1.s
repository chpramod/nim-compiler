# PURPOSE:
#
# Print numbers on terminal

.section .data

number:
  .long 12345

.section .text

.globl _start

_start:
  xorl %esi, %esi
  movl number, %eax

loop: # eax stores quotient, edx stores remainder
  incl %esi
  movl $0, %edx
  movl $10, %ebx
  divl %ebx # quotient modulo 10
  addl $48, %edx # adding 48 to represtent the value as a ascii value
  pushl %edx # pushing the current least significant digit
  cmpl $0, %eax
  je _end
  jmp loop

_end:
  cmpl $0, %esi # to determine how mant times to runt he loop
  jz exit
  movl $4, %eax
  movl $1, %ebx
  movl %esp, %ecx # popping the current most significant digit
  movl $1, %edx
  int $0x80
  addl $4, %esp # incrementing the stact pointer to point to the next stack item
  decl %esi # decrementing the loop counter
  jmp _end
  
exit:
  movl $1, %eax
  movl $0, %ebx
  int $0x80
